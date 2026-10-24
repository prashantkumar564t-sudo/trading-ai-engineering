# Agent Instructions and Guidelines

Welcome to the **Trading AI Engineering Framework**. This document provides essential workspace-level rules and directives for AI agents operating in this repository.

---

## Core Directives

1. **Framework Scope**: This repository is a reusable engineering framework for research and market-data tooling, **not** an automated trading bot, execution engine, or signal service.
2. **Understand Before Implementing**: Inspect relevant project structure and files before making changes. Understand the full requirement and invariants, and choose the smallest sufficient solution.
3. **Mandatory Reference Documents**: All work must strictly align with the project's foundational guidelines:
   - [docs/principles.md](docs/principles.md): Core engineering and quantitative research principles.
   - [docs/verification.md](docs/verification.md): Practical verification checklist and evidence reporting standard.
   - [.agents/rules/engineering-standards.md](.agents/rules/engineering-standards.md): Binding engineering and operational standards.
4. **Lightweight Python Discipline**: Prioritize the Python standard library. Add third-party dependencies only when their explicit benefits decisively justify the installation, maintenance, and compatibility costs.
5. **Platform Compatibility & Termux**: For components targeting Android Termux, verify compatibility separately on genuine hardware/environments. Successful Windows execution alone is insufficient to claim Termux support.
6. **Integrity of Evidence**: Never fabricate market data, measurements, test results, or claims of success. Report exact commands executed and classify any unperformed checks explicitly as `UNTESTED`.
7. **Live Execution Air-Gap**: Never implement, arm, or activate live order execution without explicit, separate user authorization. All trading logic defaults to dry-run or simulation mode.
8. **Change Discipline**: Keep changes focused strictly on the requested task. Do not overwrite unrelated work, install packages, make network requests, alter global configuration, or create Git commits unless explicitly authorized.
9. **No Hallucinated Requirements**: When an important requirement is underspecified or ambiguous, ask for clarification instead of silently making assumptions or inventing requirements.
10. **Concise Operational Guidance**: Keep workspace rules concise and auditable. Consult the detailed rules in [.agents/rules/engineering-standards.md](.agents/rules/engineering-standards.md) rather than duplicating them here.
