# Ecosystem Audit

Live dashboard: **https://ttrng3.github.io/Omni-Audit/**

**This repo is the source of truth.** A cloud routine writes `data/` and GitHub
Pages serves it. `docs/audit-refresh.md` is the runbook and outranks the routine
prompt and any stored memory.

    schedule → cloud routine → source → GitHub → Pages

**The Pages URL is the only link.** A Cowork preview artifact of this page exists
and is refreshed after each publish, but its URL is never written here or in any
document — see "One address, one preview" in `docs/audit-refresh.md`.
