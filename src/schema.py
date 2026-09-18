"""Quantity catalog and column detection for AquaScan reports.

Every column present in an AquaScan CSV report is mapped to a :class:`Quantity`
describing its human label, unit of measure, default scale and UI category.
Columns that are not in the catalog but hold numeric values are still ingested
as generic quantities so that no measurement is silently dropped.

Module documentation: ``docs/modules/schema.md``.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

# UI grouping order. Generic auto-detected columns land in "Other".
CATEGORY_ORDER = [
    "Water Quality",
    "Waves",
    "Position & Orientation",
    "Device & Telemetry",
    "Other",
]


@dataclass(frozen=True)
class Quantity:
    """A plottable measurement column.

    Attributes:
        key: Raw CSV column name.
        label: Human-readable display name.
        unit: Unit of measure shown on the axis (empty when dimensionless).
        scale: Default multiplier applied to raw values for display.
        category: UI grouping key.
        description: Short explanation for tooltips and docs.
    """

    key: str
    label: str
    unit: str
    scale: float
    category: str
    description: str = ""


# Catalog of known AquaScan report columns. Keys are the exact CSV headers.
QUANTITY_SCHEMA: dict[str, Quantity] = {
    "Reboots": Quantity("Reboots", "Reboot Counter", "#", 1.0, "Device & Telemetry",
                        "Cumulative device reboot counter."),
    "Latitude": Quantity("Latitude", "Latitude", "°", 1.0, "Position & Orientation",
                         "Decimal degrees; also merged from the companion location report."),
    "Longitude": Quantity("Longitude", "Longitude", "°", 1.0, "Position & Orientation",
                          "Decimal degrees; also merged from the companion location report."),
    "Vbatt": Quantity("Vbatt", "Battery Voltage", "V", 0.001, "Device & Telemetry",
                      "Raw millivolts converted to volts."),
    "Case_Temp": Quantity("Case_Temp", "Case Temperature", "°C", 1.0, "Device & Telemetry",
                          "Enclosure temperature."),
    "Humidity": Quantity("Humidity", "Humidity", "%RH", 1.0, "Device & Telemetry",
                         "Relative humidity inside the enclosure."),
    "Temp_H2O": Quantity("Temp_H2O", "Water Temperature", "°C", 1.0, "Water Quality",
                         "Main water temperature."),
    "Turbidity NTU": Quantity("Turbidity NTU", "Turbidity", "NTU", 1.0, "Water Quality",
                              "Nephelometric turbidity."),
    "Azimut": Quantity("Azimut", "Azimuth", "°", 1.0, "Position & Orientation",
                       "Device/sensor azimuth heading."),
    "DO2": Quantity("DO2", "Dissolved Oxygen", "mg/L", 1.0, "Water Quality",
                    "Dissolved oxygen concentration."),
    "Altezza Onda": Quantity("Altezza Onda", "Wave Height", "m", 1.0, "Waves",
                             "Wave height."),
    "Periodo Onda": Quantity("Periodo Onda", "Wave Period", "s", 1.0, "Waves",
                             "Wave period."),
    "OTA_en": Quantity("OTA_en", "OTA Enabled", "flag", 1.0, "Device & Telemetry",
                       "Over-the-air update enabled flag (0/1)."),
    "rssi": Quantity("rssi", "RSSI", "dBm", 1.0, "Device & Telemetry",
                     "Received signal strength."),
    "round_trip": Quantity("round_trip", "Round Trip Time", "ms", 1.0, "Device & Telemetry",
                           "Network round-trip latency."),
    "Temp_H2O_O2": Quantity("Temp_H2O_O2", "Water Temp (O₂ sensor)", "°C", 1.0, "Water Quality",
                            "Water temperature from the dissolved-oxygen probe."),
    "O2_saturation": Quantity("O2_saturation", "O₂ Saturation", "%", 1.0, "Water Quality",
                              "Dissolved oxygen saturation."),
    "cycle_time": Quantity("cycle_time", "Cycle Time", "s", 1.0, "Device & Telemetry",
                           "Sampling cycle duration."),
    "water_level": Quantity("water_level", "Water Level", "m", 1.0, "Water Quality",
                            "Water column level."),
    "Conducibility": Quantity("Conducibility", "Conductivity", "µS/cm", 1.0, "Water Quality",
                              "Electrical conductivity."),
    "Azimut_offset": Quantity("Azimut_offset", "Azimuth Offset", "°", 1.0, "Position & Orientation",
                              "Azimuth calibration offset."),
    "Conducibility_CWT": Quantity("Conducibility_CWT", "Conductivity (CWT)", "µS/cm", 1.0, "Water Quality",
                                  "Conductivity after CWT processing."),
    "Temp_H2O_CWT": Quantity("Temp_H2O_CWT", "Water Temp (CWT)", "°C", 1.0, "Water Quality",
                             "Water temperature after CWT processing."),
    "ph_CWT": Quantity("ph_CWT", "pH (CWT)", "pH", 1.0, "Water Quality",
                       "pH after CWT processing."),
    "Redox_CWT": Quantity("Redox_CWT", "Redox / ORP (CWT)", "mV", 1.0, "Water Quality",
                          "Redox potential after CWT processing."),
    "Spec_Weight": Quantity("Spec_Weight", "Specific Weight", "kg/m³", 1.0, "Water Quality",
                            "Specific weight / density."),
    "Free_chlorine": Quantity("Free_chlorine", "Free Chlorine", "mg/L", 1.0, "Water Quality",
                              "Free chlorine concentration."),
}


def quantity_for(column: str) -> Quantity | None:
    """Return the catalog entry for a column, or ``None`` when unknown."""
    return QUANTITY_SCHEMA.get(column)


def _is_numeric_column(series: pd.Series) -> bool:
    """Return True when a column holds numeric values (even as strings)."""
    if pd.api.types.is_numeric_dtype(series):
        return True
    coerced = pd.to_numeric(series, errors="coerce")
    return coerced.notna().any()


def detect_quantities(df: pd.DataFrame) -> list[Quantity]:
    """Return the plottable quantities present in ``df``.

    Known columns use the catalog; other numeric columns are auto-detected as
    generic quantities so nothing is dropped. ``Time`` is never a quantity.
    """
    quantities: list[Quantity] = []
    for column in df.columns:
        if column == "Time":
            continue
        known = QUANTITY_SCHEMA.get(column)
        if known is not None:
            quantities.append(known)
        elif _is_numeric_column(df[column]):
            quantities.append(
                Quantity(column, column, "", 1.0, "Other", "Auto-detected numeric column.")
            )
    return quantities


def group_quantities(quantities: list[Quantity]) -> dict[str, list[Quantity]]:
    """Group quantities by category, preserving insertion order."""
    grouped: dict[str, list[Quantity]] = {}
    for q in quantities:
        grouped.setdefault(q.category, []).append(q)
    return grouped


def display_label(q: Quantity) -> str:
    """Human label including unit, e.g. ``Turbidity (NTU)``."""
    if q.unit:
        return f"{q.label} ({q.unit})"
    return q.label
