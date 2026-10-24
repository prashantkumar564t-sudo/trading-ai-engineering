# Engineering Principles

This document articulates the foundational engineering principles governing all code, documentation, and agent workflows within this framework and any future applications derived from it.

---

### 1. Understand Requirements Before Implementation
Never begin writing code on assumptions or incomplete problem statements. Clarify inputs, expected outputs, failure states, and performance constraints first. When requirements are ambiguous, ask questions and document boundaries before designing solutions.

### 2. Prefer the Simplest Design That Reliably Meets Requirements
Avoid speculative architecture, premature optimization, and over-engineered abstractions. The best solution is often straightforward, readable, and easy to maintain and verify.

### 3. Avoid Unnecessary Dependencies and Abstractions
Rely on the Python Standard Library first. Every added dependency brings security vulnerabilities, version conflicts, installation friction, and cross-platform incompatibilities (particularly across desktop, server, and lightweight mobile environments like Android Termux).

### 4. Preserve Existing Working Behavior
Do not break established functionality, regression suites, or configuration files unless a modification is explicitly requested and reasoned through. Refactoring must be accompanied by regression verification.

### 5. Never Invent Test Results, API Behavior, Market Data, or Measurements
Integrity of evidence is non-negotiable:
- Never hallucinate API endpoints or response formats.
- Never generate synthetic data and present it as genuine market history.
- Never claim a test passed or a metric was achieved without actual, verifiable command output.

### 6. Distinguish Assumptions, Recommendations, Verified Facts, and Unresolved Questions
In all engineering communications, reports, and code comments:
- **Verified Facts**: Empirical data backed by executed commands and source references.
- **Assumptions**: Working premises that require future validation.
- **Recommendations**: Proposed approaches subject to review and confirmation.
- **Unresolved Questions**: Unknowns that must be answered before progress can continue.

### 7. Measure Resource Consumption When Limitations Matter
For systems with constrained memory, CPU, or disk footprints (such as laptops or mobile environments), measure runtime performance and storage growth directly with profiling tools rather than guessing.

### 8. Keep Project-Specific Requirements Separate from General Engineering Rules
Maintain a clean separation between reusable, general engineering standards (e.g., error handling, file safety, clean test design) and domain-specific rules (e.g., exchange data formatting, trading order protocols).

### 9. Require Explicit Authorization Before Live Trading Order Execution
Live order execution presents financial risk. All execution code must default to dry-run or mock mode. Live order submission logic must never be implemented or armed without separate, explicit, and unambiguous user authorization.

### 10. Treat Backtest Results as Historical Evidence, Not Guarantees of Future Profitability
Backtests are simulations subject to limitations: slippage, fee structures, liquidity constraints, look-ahead bias, and overfitting. Historical performance must be critically audited and treated solely as evidence of past behavior under specific model assumptions.
