# Trading AI Engineering Framework

A reusable, lightweight, and disciplined AI-assisted engineering framework for developing reliable, verifiable software projects, specifically targeted toward future quantitative trading research and market-data applications.

> **Important**: This repository is **not** a trading bot, automated execution system, or financial signal service. It contains no trading strategies, data collectors, broker integrations, or order execution logic. Its sole purpose is to establish engineering principles, reusable agent skills, verification standards, and reproducible workflows.

---

## Purpose and Scope

When building quantitative trading and financial data software, software reliability and disciplined verification are paramount. Flawed assumptions, unverified data feeds, look-ahead bias, and hidden dependencies can lead to severe system failures.

This framework defines a systematic baseline for:
- Establishing strict engineering standards and testing checklists.
- Providing modular agent skills and rules for AI-assisted development.
- Ensuring projects run reliably across varied development environments with minimal dependencies.
- Enforcing verifiable, evidence-based development rather than speculative implementation.

---

## Development Workflow

All development within this framework adheres to a structured, iterative cycle:

1. **Discuss Requirements**: Clarify and document objectives, boundaries, and performance constraints before writing code.
2. **Plan**: Produce an explicit, phased plan separating facts, assumptions, and unresolved questions.
3. **Implement**: Construct simple, maintainable solutions adhering to strict architectural boundaries. Avoid unnecessary third-party dependencies.
4. **Test & Verify**: Run offline, automated tests and inspect actual outputs. Never assume or hallucinate successful execution.
5. **Inspect Evidence**: Review test reports, resource usage, and edge case coverage against the verification checklist.
6. **Improve Incrementally**: Refactor and extend functionality based on verified evidence and feedback.

---

## Verified Environments

### 1. Primary Workstation (Windows 11)
Directly verified on the primary development workstation:
- **Operating System**: Microsoft Windows 11 Pro (64-bit, Version `10.0.26200`)
- **Python**: `3.14.3` (64-bit)
- **Package Manager**: `pip 25.3`
- **Testing Framework**: `pytest 9.1.1`
- **Version Control**: `git version 2.53.0.windows.2`
- **Node.js**: `v24.14.1`

### 2. Mobile / Edge Node (Android 15 / Termux)
Directly verified on genuine Android hardware:
- **Test Date**: Unrecorded
- **Tested Commit**: `a86040ae1e73b017b069de996f902e8cdc379d63`
- **Operating System**: Android 15 (Termux environment, 64-bit)
- **Python**: `3.14.6` (64-bit)
- **Testing Framework**: `pytest 9.1.1`
- **Automated Tests**: 41 passed (`python -m pytest tests/ -v`)
- **Verification Orchestrator**: `PASSED` (`python scripts/verify.py`)
- **Working Tree**: Clean
- **CI Status**: GitHub Actions Run verified successful on commit `a86040a`
- **Scope & Limitations**: Baseline offline tests and verification orchestration confirmed on this environment. Does not constitute universal Android compatibility across differing vendors, Android versions, or hardware architectures, nor runtime resource/battery profiling.

---

## Verified Facts vs. Future Compatibility Goals

To uphold engineering integrity, we explicitly distinguish between verified facts and future goals:

- **Verified Facts**:
  - Windows 11 development environment with Python 3.14, Git, and pytest is active and verified.
  - Android 15 Termux mobile node execution with Python 3.14.6, Git, and pytest 9.1.1 is verified on commit `a86040a` (41 tests passed; verification audit passed).
  - GitHub Actions CI workflow is operational and passing on `master`.
  - Minimal repository structure, documentation baseline, and offline sanity test suite have been established.
- **Future Compatibility Goals & Untested Capabilities**:
  - **Broad Mobile & Edge Validation**: While baseline tests pass on Android 15 Termux, long-running process resilience, daemon execution, battery/memory consumption profiling, and other Android versions or architectures remain untested.
  - **Modular Skills & Rules**: Custom agent skills (e.g., market data verifier, backtest auditor) are planned for implementation in subsequent phases.
