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

## Verified Development Environment

The following environment baseline has been directly verified on the primary development workstation:

- **Operating System**: Microsoft Windows 11 Pro (64-bit, Version `10.0.26200`)
- **Python**: `3.14.3` (64-bit)
- **Package Manager**: `pip 25.3`
- **Testing Framework**: `pytest 9.1.1`
- **Version Control**: `git version 2.53.0.windows.2`
- **Node.js**: `v24.14.1`

---

## Verified Facts vs. Future Compatibility Goals

To uphold engineering integrity, we explicitly distinguish between verified facts and future goals:

- **Verified Facts**:
  - Windows 11 local development environment with Python 3.14, Git, and pytest is active and verified.
  - Minimal repository structure, documentation baseline, and offline sanity test suite have been established.
- **Future Compatibility Goals**:
  - **Android Termux Portability**: The framework is intentionally designed to favor pure Python and standard library utilities to maximize portability for lightweight devices and Android Termux. However, Termux execution has **not** yet been tested or verified on a live device.
  - **Modular Skills & Rules**: Custom agent skills (e.g., market data verifier, backtest auditor) are planned for implementation in subsequent phases.
