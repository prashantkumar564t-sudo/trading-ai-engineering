# Engineering Standards and Operational Rules

This document establishes the binding engineering standards and operational rules for AI agents and human contributors working within this framework and across derived research and market-data projects.

---

## 1. Understand Before Implementing

- **Inspect Context First**: Inspect the existing directory structure, configuration, and relevant code files before proposing or making changes. Never assume file layouts or conventions.
- **Clarify Requirements and Invariants**: Fully understand the requirement, acceptance criteria, and operational constraints before writing code.
- **Propose Implementation Plans**: For non-trivial or material changes, present a concise, structured implementation plan and obtain alignment before proceeding.
- **Minimal Sufficient Solution**: Prefer the smallest, cleanest solution that completely satisfies the requirements. Avoid speculative features or unrequested scope.
- **No Hallucinated Requirements**: When a critical requirement is underspecified or ambiguous, ask for clarification. Never invent requirements or silent assumptions.

---

## 2. Lightweight Python Engineering

- **Standard Library First**: Prioritize Python's standard library (`pathlib`, `json`, `csv`, `sqlite3`, `dataclasses`, `typing`, `math`, `urllib`, etc.) whenever it is sufficient.
- **Strict Dependency Discipline**: Add third-party packages only when their explicit benefits decisively outweigh installation complexity, maintenance burden, memory overhead, and cross-platform installation friction.
- **No Heavy Libraries by Default**: Do not introduce `pandas`, `numpy`, `scipy`, or heavy quantitative frameworks unless explicitly requested and justified by performance requirements.
- **Pragmatic Utility**: Do not rebuild complex, error-prone cryptographic, networking, or parsing primitives from scratch without clear reason.
- **Clean and Simple Design**: Avoid unnecessary abstractions, speculative inheritance hierarchies, excessive configuration layers, and premature optimizations.

---

## 3. Platform Compatibility (Windows & Android Termux)

- **Dual-Environment Awareness**: Treat Windows (local workstation development) and Android Termux (lightweight deployment/alert node) as distinct environments with differing architectures, file paths, and resource constraints.
- **Termux-First Design**: Design scripts and modules intended for mobile deployment to be portable, POSIX-compliant, and resource-conscious.
- **Verify Rather Than Assume**: Check actual platform compatibility empirically. Never assume a package or command functions identically across operating systems.
- **Explicit Identification**: Clearly identify platform-specific commands, file path separators, terminal tools, and environment variables.
- **Honest Platform Claims**: Never claim Termux compatibility based solely on successful Windows execution. Mark unverified platforms as `UNTESTED`.
- **Workload Partitioning**: Utilize workstation/laptop compute for intensive analysis and modeling; keep mobile-side Termux workloads lightweight, fault-tolerant, and low on battery/memory consumption.

---

## 4. Data Integrity, File Safety, and Error Handling

- **Strict Input Validation**: Validate external data, market feeds, and configuration files. Handle malformed lines, missing fields, stale values, and schema variations explicitly.
- **No Silent Failures**: Never suppress exceptions silently or return misleading default values. Propagate or log errors with actionable diagnostic context.
- **Traceable Transformations**: Preserve raw source data whenever feasible and ensure all data transformations, normalizations, and calculations are reproducible and auditable.
- **Atomic and Safe Writes**: Where file persistence is required, write to a temporary file first and atomically rename/replace it to prevent partially written or corrupt files during crashes or interruptions.
- **Fault Recovery and Restartability**: Design long-running data or state processes to handle interrupted operations, duplicate messages, and clean restart without data loss.
- **Zero Data Fabrication**: Never fabricate market data, test outputs, execution receipts, or external API responses.

---

## 5. Security and Trading Boundaries

- **Zero Credential Exposure**: Never hardcode passwords, API keys, secret tokens, or private certificates in code, tests, logs, or commit histories.
- **Strict Isolation of Boundaries**: Maintain strict architectural separation between market-data ingestion, quantitative research, backtesting simulation, and live execution.
- **Live Execution Air-Gap**: Never implement, arm, or activate live order execution without explicit, separate user authorization. All trading logic defaults to dry-run or mock mode.
- **Realistic Research Auditing**: Never characterize a strategy as profitable without verifiable empirical evidence, realistic transaction costs, slippage models, liquidity constraints, and proper out-of-sample evaluation.
- **Backtests as Historical Estimates**: Treat backtest results as historical estimates under bounded assumptions, never as guarantees of future performance.

---

## 6. Testing, Measurement, and Verification

- **Automated Test Coverage**: Provide automated unit and regression tests for all functional changes where practical.
- **Edge and Failure Cases**: Test boundaries, zero-division hazards, missing inputs, and network/file failure paths, not merely the happy path.
- **Deterministic and Offline Tests**: Build deterministic local tests using static fixtures. Automated test suites must run strictly offline without external service dependencies.
- **Evidence-Based Reporting**: Report exact commands executed, exit codes, and output summaries. Never claim a test passed without running it.
- **Accurate Status Categorization**: Categorize all verification items explicitly as `PASSED`, `FAILED`, `SKIPPED`, or `UNTESTED`.
- **Resource Profiling**: Measure runtime duration, peak memory (RSS), CPU utilization, and disk storage growth when evaluating performance-critical or resource-constrained components.

---

## 7. Change Discipline and Git Practices

- **Inspect Repository State**: Run `git status` before beginning work when Git is present to understand the baseline working tree.
- **Focused Scope**: Restrict changes strictly to the task at hand. Do not modify or refactor unrelated files.
- **Protect User Work**: Never overwrite, revert, or clobber working functionality or files created by the user.
- **No Unauthorized Operations**: Do not install packages, execute arbitrary network requests, alter global configurations, or create Git commits unless explicitly instructed.
- **Transparent Accounting**: Conclude each task with an accurate list of files created/modified, limitations encountered, and remaining open questions.

---

## 8. Documentation and Communication

- **Truth in Documentation**: Ensure documentation, code comments, and runbooks accurately reflect current code behavior and verified reality.
- **Reproducible Procedures**: Include exact, copy-pasteable command lines, prerequisites, and expected outputs in runbooks.
- **Explicit Limitations**: Clearly state known environmental constraints, missing features, and pending validations.
- **Rigorous Taxonomy**: Clearly separate verified facts, working assumptions, recommendations, and unresolved questions in all engineering communications.
