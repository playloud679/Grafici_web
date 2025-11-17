// Configurazione colori
const colors = {
    primary: '#6366f1',
    secondary: '#8b5cf6',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
    info: '#3b82f6',
    purple: '#a855f7',
    pink: '#ec4899'
};

// Configurazione globale per tutti i grafici
Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif";
Chart.defaults.color = '#6b7280';

// Grafico 1: Vendite Mensili (Line Chart)
const salesCtx = document.getElementById('salesChart').getContext('2d');
const salesChart = new Chart(salesCtx, {
    type: 'line',
    data: {
        labels: ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic'],
        datasets: [{
            label: 'Vendite 2024',
            data: [12500, 19800, 15600, 25400, 22300, 28900, 32100, 29500, 35200, 38600, 42300, 45890],
            borderColor: colors.primary,
            backgroundColor: colors.primary + '20',
            tension: 0.4,
            fill: true,
            pointRadius: 5,
            pointHoverRadius: 7
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                display: true,
                position: 'top'
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(context) {
                        return context.dataset.label + ': €' + context.parsed.y.toLocaleString();
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return '€' + value.toLocaleString();
                    }
                }
            }
        }
    }
});

// Grafico 2: Distribuzione Utenti (Doughnut Chart)
const usersCtx = document.getElementById('usersChart').getContext('2d');
const usersChart = new Chart(usersCtx, {
    type: 'doughnut',
    data: {
        labels: ['Desktop', 'Mobile', 'Tablet'],
        datasets: [{
            data: [45, 42, 13],
            backgroundColor: [
                colors.primary,
                colors.secondary,
                colors.info
            ],
            borderWidth: 0
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                position: 'bottom'
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return context.label + ': ' + context.parsed + '%';
                    }
                }
            }
        }
    }
});

// Grafico 3: Andamento Traffico (Area Chart)
const trafficCtx = document.getElementById('trafficChart').getContext('2d');
const trafficChart = new Chart(trafficCtx, {
    type: 'line',
    data: {
        labels: ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom'],
        datasets: [
            {
                label: 'Visitatori',
                data: [1200, 1900, 1500, 2100, 2400, 1800, 1300],
                borderColor: colors.success,
                backgroundColor: colors.success + '30',
                fill: true,
                tension: 0.4
            },
            {
                label: 'Visualizzazioni',
                data: [2400, 3100, 2800, 3600, 4200, 3200, 2500],
                borderColor: colors.info,
                backgroundColor: colors.info + '30',
                fill: true,
                tension: 0.4
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                position: 'top'
            },
            tooltip: {
                mode: 'index',
                intersect: false
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Grafico 4: Performance Prodotti (Bar Chart)
const productsCtx = document.getElementById('productsChart').getContext('2d');
const productsChart = new Chart(productsCtx, {
    type: 'bar',
    data: {
        labels: ['Prodotto A', 'Prodotto B', 'Prodotto C', 'Prodotto D', 'Prodotto E'],
        datasets: [{
            label: 'Vendite',
            data: [450, 380, 520, 290, 410],
            backgroundColor: [
                colors.primary,
                colors.secondary,
                colors.success,
                colors.warning,
                colors.danger
            ],
            borderRadius: 8,
            borderSkipped: false
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return 'Vendite: ' + context.parsed.y + ' unità';
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Animazione dei numeri nelle card statistiche (opzionale)
function animateValue(id, start, end, duration) {
    const obj = document.querySelector(id);
    if (!obj) return;

    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        obj.textContent = Math.round(current).toLocaleString();
    }, 16);
}

// Esegui animazioni al caricamento della pagina
window.addEventListener('load', () => {
    console.log('Dashboard caricata con successo!');
});
