# GOLDEN_STD.md - Universal Development & AI Agent Contract

**Specification Version:** `1.3.2`

**Last Updated:** `2026-09-10`

**Standard Identifier:** `STD-AGY-DEV-CONTRACT-V1.3.2`

**Central Canonical Repository:** `https://github.com/playloud679/dev_standards`

---

## 0. Modular Development & Module Documentation

Software MUST be developed as cohesive modules with clear responsibilities and explicit interfaces. A module is a logical unit of behavior, implemented by one source file or a coherent group of files; it is not necessarily a single class or function.

For every module:

- Define its responsibility, public interface, dependencies, and boundaries. Keep unrelated responsibilities separate and avoid circular dependencies.
- Adequately comment the source: include a short module-level description and document public APIs, non-obvious decisions, invariants, and edge cases as needed. Follow §6; comments must explain intent rather than repeat instructions.
- Maintain a dedicated Markdown document, by default `docs/modules/<module-path>.md`. Record the source files it covers and link to it from the module-level source comment or docstring.
- Register the module, its source paths, and its dedicated document in `docs/INDEX.md`. Existing documentation paths are acceptable when this mapping is explicit and unambiguous.
- Apply the Documentation Contract (§2) after every patch affecting the module. Code comments and the dedicated document are complementary obligations.

Prefer boundaries that match the project's behavior and architecture; avoid arbitrary file-size limits or splitting code into modules without a clear responsibility. When patching existing code, apply these requirements to the affected modules without refactoring unrelated areas.

---

> [!IMPORTANT]
> ### Sync & Version Check Rule for AI Coding Assistants
> At the start of a new major task or repository setup, the agent should check whether a newer version of `GOLDEN_STD.md` exists in the canonical repository:
> ```bash
> curl -s https://raw.githubusercontent.com/playloud679/dev_standards/refs/heads/main/VERSION
> ```
> If a newer version is available and compatible with the project, propose synchronizing via:
> ```bash
> curl -s https://raw.githubusercontent.com/playloud679/dev_standards/refs/heads/main/GOLDEN_STD.md -o GOLDEN_STD.md
> ```

---

> [!WARNING]
> ### Universal Context & Conflict-Resolution Disclaimer
> `GOLDEN_STD.md` defines universal engineering standards, safety invariants, and quality rules across software, embedded systems, and audio/acoustic engineering.
>
> **AI Agent Operating Directive**:
> 1. You must ALWAYS verify whether any general rule in this document conflicts with the specific intent, domain constraints, or explicit instructions of the active user request.
> 2. **Precedence Hierarchy**:
>    - **Priority 1**: Explicit user instructions in the active conversation.
>    - **Priority 2**: Project-specific requirements, domain physics, or explicit local architecture.
>    - **Priority 3**: `GOLDEN_STD.md` universal engineering rules.
> 3. If a general guideline contradicts a specific user goal (e.g. rapid prototype vs strict production gating, experimental algorithm vs classic invariant), **the user request and project intent take precedence**.
> 4. In case of ambiguity, decide reasonably in the user's best interest or briefly ask for clarification rather than stubbornly applying a conflicting general rule.

---

### Specification Revision History

| Version | Date | Author / Context | Changes / Additions |
|---|---|---|---|
| `1.3.2` | 2026-09-10 | Core Engineering | Required documentation review with edits only when needed, separated test procedures from run outcomes, scaled validation to impact and delivery stage, adopted project-defined branching, and moved domain details into addenda. |
| `1.3.1` | 2026-09-08 | Core Engineering | Required version bumps for application patches only, exempted documentation/test-only changes, assigned lifecycle state to each project, and added documentation-only validation rules. |
| `1.3.0` | 2026-09-08 | Core Engineering | Added initial modular development contract (§0), explicit module-to-doc mapping and post-patch obligations (§2), and aligned module comments, done criteria, and agent template. |
| `1.2.1` | 2026-08-30 | Core Engineering | Added Project Lifecycle & Versioning Stages (§8): Alpha stage (`0.x.y`, current active), Beta stage, and locked Major `1.0.0+` release strictly upon exit from Beta. |
| `1.2.0` | 2026-08-30 | Core Engineering | Added Mandatory Version Bump Rule (§8): Every modification, bug fix, or feature committed MUST increment the release version with tags, changelog, and UI alignment. |
| `1.1.0` | 2026-08-30 | Core Engineering | Added central sync instructions, conflict resolution disclaimer, UI key isolation (§3), Streamlit headless `AppTest` validation (§7), release tagging workflow (§8), Conventional Commits convention (§10), and Audio DSP & Acoustic Test Benches Addendum (§14). |
| `1.0.0` | 2026-08-30 | Core Engineering | Initial baseline specification: branching strategy, documentation contract, token-efficient reading, change scope, tiered testing, error handling, and embedded firmware addendum. |

---

## 1. Branching

Do not develop directly on the default branch.

Use a branch dedicated to the change, following the project's naming convention. The project defines its integration target (for example `main`, `develop`, or `dev`) in `AGENTS.md` or `README.md`; this standard does not require a `dev` branch.

Default flow:

1. Identify the project's integration target and start a dedicated branch from the appropriate base, or continue the existing branch for the same task.
2. Implement the scoped patch and run the checks required by §7.
3. Commit and push the change branch when requested or already authorized.
4. Open a draft PR targeting the project's integration branch when requested.
5. Complete integration checks and merge after review when authorized.

Before staging or committing:

```bash
git status -sb
git diff --stat
git diff --check
```

Stage explicit files only. Do not use broad staging (`git add .` or `git add -A`) when the worktree contains unrelated or untracked files.

---

## 2. Documentation Contract

Documentation must stay in sync with source.

When modifying a source module, review the matching documentation. Update it in the same change only when needed to keep it accurate and useful:

| Changed file | Required documentation |
|---|---|
| `src/foo.py` | `docs/modules/foo.md` |
| `src/services/bar.ts` | `docs/modules/services/bar.md` |
| `src/drivers/bar.cpp` and `src/drivers/bar.h` (one logical module) | `docs/modules/drivers/bar.md` |
| user-visible UI behavior | `USER_GUIDE.md` and/or `docs/INDEX.md` |
| release/version behavior | `CHANGELOG.md`, `VERSION`, package metadata |

Use the module-to-doc mapping established in §0. If a matching doc or `docs/INDEX.md` does not exist, create it. Preserve source-relative paths by default to avoid collisions between modules with the same basename. A module spanning multiple source files has one dedicated document listing all covered files.

Docs should explain public APIs, invariants, assumptions, edge cases, failure modes, and the tests protecting the behavior. Future agents should be able to read docs before source to save tokens.

### Post-Patch Documentation Obligations

Before handing off any patch affecting source:

1. Identify all affected modules, including dependent modules whose contracts changed, and locate their dedicated `.md` files through `docs/INDEX.md`.
2. Verify that each affected module document matches the resulting behavior, interfaces, dependencies, constraints, and relevant implementation rationale. Update inaccurate or missing information in the same change. If the document is already correct, leave it unchanged and report that it was reviewed; do not add filler solely to produce a documentation diff.
3. Review and update module descriptions, API documentation, inline comments, and source-to-doc pointers where needed.
4. For added, renamed, split, or removed modules, update the source-to-doc mapping, references, and index; remove or explicitly archive obsolete module documents.
5. Keep reusable validation commands, test scenarios, and protected invariants in the module document. Record individual run outcomes, pass counts, and checks not run (with reasons) in the patch report or PR, not in module docs. Update user guides and release documentation when affected.
6. Verify that source-to-doc links and index entries resolve. In the final handoff, identify affected modules and documentation updated or reviewed without changes.

---

## 3. Source-to-UI Contract

If backend behavior changes, update every dependent UI and caller.

Checklist:

- New function/module: add caller or UI integration.
- Changed function signature: update all call sites and tests.
- Changed behavior: update user-facing text if users need to understand it.
- New parameter: hide it unless it is relevant for the active mode.
- Disabled component: hide its parameters instead of leaving confusing controls.
- Generated output: update previews, labels, downloads, and tests.

UI rule:

```text
Include selected     -> relevant parameters visible
Include not selected -> related parameters hidden
```

Keep persistent application state separate from transient UI actions to avoid collisions. Framework-specific patterns belong in the [Streamlit & SaaS addendum](addenda/STREAMLIT_SAAS.md).

Primary/base controls must not be hidden in an `Advanced` section. Use `Advanced` only for rare, dangerous, or expert-only controls.

---

## 4. Token-Efficient Reading

Do not read the whole repo unless needed.

Preferred order:

1. Read `GOLDEN_STD.md`, `AGENTS.md`, `README.md`, and `docs/INDEX.md`.
2. Use `rg` to locate relevant symbols.
3. Read matching docs before source.
4. Read only the source slices needed.
5. Read focused tests around the behavior.
6. Expand scope only when evidence requires it.

Preferred commands:

```bash
rg "symbol_or_text"
rg --files
sed -n '120,220p' file.py
git diff -- file.py
```

Avoid dumping large files into context.

---

## 5. Change Scope

Keep edits narrow.

Do:

- fix the requested behavior
- update directly related tests and docs
- preserve existing style
- use existing helpers and patterns

Do not:

- refactor unrelated code
- rename unrelated things
- reformat whole files
- delete user work
- modify generated or temporary files unless explicitly required

If the worktree is dirty, assume unknown changes are user-owned.

Never run destructive commands such as `git reset --hard`, `git checkout -- .`, or broad `rm -rf` unless explicitly requested and confirmed.

---

## 6. Code Comments

Every module must be adequately commented as required by §0. Keep comments concise and useful; comment density is not a quality metric. Include a module-level description and a pointer to the dedicated Markdown document, and document public API inputs, outputs, and failure behavior where these are not already clear from the language's declarations.

Use comments to explain:

- why a non-obvious choice exists
- invariants that future edits must preserve
- geometry, state, API, or UI contracts
- workarounds for library behavior
- edge cases that tests protect

Avoid comments that merely restate the code.

Good:

```python
# Adapter owns driver-side geometry; keep throat flange UI status-only
# while preserving generation defaults for the assembly path.
_ft_sp = _ta_flange_sp
```

Bad:

```python
# Set _ft_sp equal to _ta_flange_sp.
_ft_sp = _ta_flange_sp
```

If the explanation needs more than a few lines, put the full reasoning in the matching doc file and leave only a short pointer in code.

---

## 7. Testing

Use tiered tests.

During focused development and minor patches, run the smallest relevant checks:

```bash
python -m py_compile path/to/file.py
python tests/test_specific.py --match "relevant behavior"
```

Select validation by impact and delivery stage:

- For an isolated local patch, run focused tests covering the changed behavior and its immediate callers. These can be sufficient for a local commit, branch push, draft PR, or handoff.
- For shared logic, public interfaces, dependencies, build/runtime configuration, or other broad changes, run the affected suites and expand to the full active suite when the impact crosses subsystem boundaries or cannot be confidently bounded.
- Before integration into the project's integration branch or an application release, require the full active suite on the final code state. CI results for that same state may satisfy this requirement; rerun affected checks if the code or merge result changes.
- For test-only patches, run the modified tests and affected fixtures; broaden checks for shared test infrastructure. The application version remains unchanged under §8.

Use the project's configured commands (for example `make test`, `pytest`, `npm test`, or `cargo test`). A local handoff does not imply integration or release readiness. Report the selected scope and any remaining integration checks. Do not repeat a successful suite without new changes, failures, or unresolved concerns.

For documentation-only patches, including accompanying version strings, badges, and changelog entries that do not affect executable behavior, the application suite is not required. Instead:

- Run `git diff --check`.
- Verify changed local links, anchors, and module-to-doc mappings where applicable.
- Check consistency of instructions, cross-references, versions, and changelog entries.
- Run the project's documentation lint/build checks when configured.

If a patch also affects executable behavior, apply the code validation requirements above. Classify by impact, not file extension; a documentation file containing changed executable examples may require relevant code checks. Changes to firmware hardware assumptions also follow §13.

Report exact validation commands and outcomes, including why the application suite was not run for a documentation-only patch. Do not claim a test passed unless it was actually run.

---

## 8. Versioning & Mandatory Bump per Application Patch

> [!IMPORTANT]
> ### Mandatory Version Bump Rule
> **EVERY application patch MUST increment the release version. Changes limited to documentation, tests, or both do not require a version bump.**
> Application patches include application or firmware source changes, refactoring, bug fixes, UX changes, features, and changes to dependencies or build/runtime configuration that affect the delivered application. Mixed patches containing application changes require a bump even when they also update docs or tests.
> For application patches, the bump is mandatory before final handoff, commit, or deployment and does not require a separate user request. A patch is a coherent change, not each intermediate file save; every subsequent application change commit must advance the version again. Every deployed application state must have a monotonically increasing, unambiguous release version.
>
> 1. **Patch (`0.y.Z+1` / `x.y.Z+1`)**: Bug fixes, calculation corrections, UX tweaks, refactoring, and other minor application patches.
> 2. **Minor (`0.Y+1.0` / `x.Y+1.0`)**: New features, new workflows/tabs, hardware integrations, cloud sync additions.
> 3. **Major (`1.0.0` / `X+1.0.0`)**: Transition from Beta to Production General Availability (GA), or subsequent breaking changes in GA.

### Project Lifecycle & Versioning Stages:

Each project declares its own current lifecycle stage in `README.md` or `AGENTS.md`, together with its release criteria. This universal standard does not prescribe a current stage. Preserve the project's declared stage and version series; adopting this standard must not reset an existing version to `0.x.y`. If the stage is undocumented, preserve the existing version series and report the missing declaration without assuming Alpha or promoting the project to GA.

- **Alpha Stage (`0.x.y`)**:
  - Rapid evolution, active experimentation, UI refinement, and foundational mechanics.
  - All version bumps are strictly within `0.x.y` (e.g. `0.4.1`, `0.5.0`, `0.12.32`).
  - Major version `1.0.0` is strictly locked and prohibited during Alpha.
- **Beta Stage (`0.x.y` / feature-complete)**:
  - Architecture stabilized, full feature set implemented, undergoing real-world validation, user testing, and hardening.
- **Production / General Availability (`1.0.0+`)**:
  - Major release `1.0.0` is cut ONLY upon formal exit from Beta once production stability and specification completeness are certified.
  - Subsequent `X+1.0.0` bumps are reserved exclusively for breaking architectural changes in GA.

For EVERY application patch:

1. Update `VERSION` (single-line SemVer string).
2. Update package metadata where present (`pyproject.toml`, `package.json`, or `Cargo.toml`).
3. Update `CHANGELOG.md` with date, summary, actual validation outcomes, and pass counts when tests ran. Record checks not run and why instead of inventing pass counts.
4. Update visible badges and versions in `README.md` and UI where present.

When a release is requested or already authorized, create an annotated Git tag (`git tag -a vX.Y.Z -m "Release vX.Y.Z: summary"`) and push the authorized branch and release tag. The mandatory local bump does not itself authorize a commit, tag, push, or release.

Changelog format:

```markdown
## x.y.z (YYYY-MM-DD)

- **Area**: concise description of what changed and why.
- **Docs/Test**: mention updated docs, tests, and version files.
```

### Specification (`GOLDEN_STD.md`) Versioning:
The specification version tracks published editions of this standard independently of application releases. Documentation-only and test-only patches, including edits to this standard, do not require a version bump. When publishing a new specification edition, synchronize its header `Specification Version`, identifier, revision history, `VERSION`, README badge, and changelog.

---

## 9. Error Handling

Do not hide failures.

When generation or transformation can fail:

- validate inputs before expensive work
- show a clear user-facing error
- preserve technical detail in logs or tests
- add a regression test for known failures

Generated outputs must satisfy the project's documented structural, semantic, and domain invariants. Validate completeness and expected content, and avoid silent fallbacks that change semantics. Domain-specific checks belong in the applicable addendum.

---

## 10. Commit and PR

Before commit:

```bash
git status -sb
git diff --check
```

Before commit, push, PR, release, or handoff, complete the checks appropriate to impact and delivery stage under §7. Full-suite integration checks may run in CI on the final code state before merge.

Stage only intended files:

```bash
git add file1 file2 docs/file.md tests/test_file.py
```

Commit with a terse concrete message using Conventional Commits:

```bash
git commit -m "feat(ui): add dual Le metrics display"
```

Conventional commit prefixes:
- `feat:` new user-facing functionality
- `fix:` bug fix
- `docs:` documentation updates
- `test:` test suite updates
- `refactor:` code restructuring without external behavior change
- `release:` version release and metadata synchronization

Push:

```bash
git push -u origin HEAD
```

PR body:

```markdown
## Summary

- What changed.
- Why it changed.
- User or developer impact.

## Validation

- Commands run.
- Test results.

## Notes

- Known limitations.
- Anything not run.
```

Default PR state is draft unless the user explicitly asks otherwise.

---

## 11. Agent Operating Rules

The agent should:

- explain briefly what it is doing while working
- implement when the request is clear
- ask only when blocked or ambiguity is risky
- prefer existing project patterns over new abstractions
- use structured APIs instead of fragile string manipulation when reasonable
- use `apply_patch` or `replace_file_content` for manual edits
- never overwrite unrelated changes
- never stop at analysis when asked to complete work

---

## 12. Done Definition

A task is done only when:

- requested behavior is implemented
- relevant docs are reviewed and updated where needed; unchanged docs are confirmed accurate
- affected modules have adequate source comments, dedicated `.md` documentation, and current mappings in `docs/INDEX.md`; §2 post-patch obligations are complete
- checks appropriate to impact and delivery stage pass as required by §7; full-suite checks pass before integration or release, and any pending integration checks are reported at local handoff
- documentation-only patches pass the documentation checks in §7; the reason for not running the application suite is reported
- version/changelog and existing version metadata are updated for application patches as required by §8; documentation-only and test-only patches do not require a version bump
- commit is created when requested
- push/PR is done when requested
- remaining risks are explicitly stated

---

## 13. Embedded Firmware Addendum

For firmware, board-support packages, device drivers, and hardware-facing applications, apply the [Embedded Firmware & IoT Standard](addenda/EMBEDDED_FIRMWARE.md). It contains hardware documentation, safety, build, upload, timing, protocol, storage, and validation requirements.

---

## 14. Audio DSP & Acoustic Test Benches Addendum

For acoustic simulators, impedance analyzers, audio test benches, and loudspeaker DSP, apply the [Audio DSP & Acoustics Standard](addenda/AUDIO_DSP_ACOUSTICS.md). It contains physical invariants, resonance extraction, and audio acquisition requirements.

---

## 15. Selecting and Synchronizing Addenda

For Streamlit dashboards and SaaS web applications, apply the [Streamlit & SaaS Standard](addenda/STREAMLIT_SAAS.md).

Declare applicable addenda in the project's `AGENTS.md` or `README.md` and read them before relevant work. Keep their relative `addenda/` paths when copying the standard into a project.

The one-file download and `scripts/sync_standards.py` synchronize only `GOLDEN_STD.md`. Copy applicable addenda separately from the same canonical revision, preserving their paths, and review them for local compatibility. A missing required addendum must be retrieved before domain-specific work; the core document is not a substitute for it.
