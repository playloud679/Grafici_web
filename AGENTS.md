# Agent Instructions for AI Coding Assistants

## Rule 0: Modular development, comments, and dedicated documentation

Develop software as cohesive modules with clear responsibilities, explicit
interfaces, and documented dependencies. A logical module may span multiple
source files. Adequately comment each module: describe its purpose, document
public APIs and non-obvious invariants, and link to its dedicated Markdown
document.

Each module MUST have a dedicated `docs/modules/<module-path>.md` and an entry
in `docs/INDEX.md` mapping its source files to that document. Follow existing
documentation paths when this mapping is explicit. Create missing documents and
index entries for affected modules.

After every source patch, review affected module documents and code comments,
including dependent modules whose contracts changed. Update missing or
inaccurate information in the same change; leave already accurate docs
unchanged and report the review. Update the index and references for added,
renamed, split, or removed modules. Keep reusable validation commands,
scenarios, and invariants in module docs; record individual run outcomes and
skipped checks with reasons in the patch report or PR. Verify documentation
links and identify reviewed or updated module docs in the final handoff.
Follow `GOLDEN_STD.md` §0 and §2 for the full contract.

## Rule 1: Validation proportional to impact and delivery stage

After every meaningful change to source or UI, run the smallest relevant check:

```bash
python -m py_compile app.py src/*.py
python -m unittest discover -s tests -v
```

Focused tests can suffice for isolated local patches, commits, branch pushes,
draft PRs, and handoffs. Expand to affected suites for shared logic and to the
full suite when impact is broad or uncertain. Require the full active suite
before integration or application release; CI results for the same final code
state may satisfy this requirement. For test-only changes, run modified tests
and affected fixtures, expanding for shared infrastructure. Report commands,
outcomes, scope, and pending integration checks in the patch report or PR.
Follow `GOLDEN_STD.md` §7.

For documentation-only patches, including accompanying version metadata with no
executable impact, follow `GOLDEN_STD.md` §7: run `git diff --check`, verify
changed links and mappings, check instruction and version consistency, and run
configured documentation lint/build checks. The application suite is not
required; report this reason and the actual documentation checks performed.
Mixed patches follow the code validation rules.

## Rule 2: Mandatory version bump and project lifecycle

Every application patch requires a version bump and changelog update before
final handoff or commit. This includes application/firmware source and changes
to dependencies or build/runtime configuration affecting the delivered
application. Changes limited to documentation, tests, or both do not require a
bump; mixed patches containing application changes do. For application patches,
synchronize existing package metadata, badges, and UI versions. A bump applies
to the coherent patch, not each file save; subsequent application change
commits must advance the version again. Commit, tag, push, and release actions
require user authorization, as described in `GOLDEN_STD.md` §8.

## Project specifics

- **Lifecycle stage:** Alpha (`0.x.y`). This is an experimental, actively
  evolving tool; the `1.0.0` major version is locked until a documented exit
  from Alpha.
- **Integration target:** `main`.
- **Applicable addendum:** `addenda/STREAMLIT_SAAS.md` (Streamlit & SaaS).
- **Entry point:** `app.py` (Streamlit).

## Universal Engineering Standard

This project adheres to `GOLDEN_STD.md`. If `GOLDEN_STD.md` is missing or
outdated, synchronize it from `playloud679/dev_standards`.

Use a branch dedicated to the task and continue an existing task branch when
appropriate. Do not develop directly on `main`.
