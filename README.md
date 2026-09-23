# Ecosystem Audit

Live dashboard: **https://ttrng3.github.io/Omni-Audit/**

**This repo is the source of truth.** A cloud routine writes `data/`, GitHub
Pages serves it, and a claude.ai artifact is mirrored afterwards — never the
other way round. `docs/audit-refresh.md` is the runbook and outranks the routine prompt and any
stored memory.

    schedule → cloud routine → source → GitHub → Pages → artifact mirrored after

See "Artifact mirror" in `docs/audit-refresh.md` for the ordering and the blank-page trap.
