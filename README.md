# Ecosystem Audit

Live dashboard: **https://ttrng3.github.io/Omni-Audit/**

**This repo is the source of truth.** A cloud routine writes `data/` and GitHub
Pages serves it. `docs/audit-refresh.md` is the runbook and outranks the routine
prompt and any stored memory.

    schedule → cloud routine → source → GitHub → Pages

**GitHub Pages is the only published surface** — there is no claude.ai artifact
copy, by Ty's ruling of 2026-09-23. See "One surface, on purpose" in `docs/audit-refresh.md`.
