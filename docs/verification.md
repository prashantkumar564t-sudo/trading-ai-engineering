# Verification Checklist and Procedures

This document provides a practical, standard verification procedure to be applied across all development iterations within this framework. Every modification or feature addition must be audited against this checklist before being considered complete.

---

## 1. Requirement Coverage
- [ ] Confirm that all explicit user requirements and acceptance criteria have been addressed.
- [ ] Ensure no unrequested scope, speculative abstractions, or placeholder files were introduced.
- [ ] Verify that existing constraints and invariants were respected.

## 2. Code and Configuration Inspection
- [ ] Verify that file paths are platform-agnostic (using `pathlib` or POSIX-compliant paths).
- [ ] Confirm file encodings are UTF-8 with standard newline handling (`LF` preferred).
- [ ] Ensure code is formatted cleanly, commented where rationale is non-obvious, and adheres to standard idioms.
- [ ] Inspect configuration files to ensure no hardcoded paths or environment-specific assumptions exist.

## 3. Automated Tests
- [ ] Run the automated test suite locally via `pytest`.
- [ ] Ensure all tests run deterministically and independently of test execution order.
- [ ] Confirm tests do not leave lingering temporary files or side effects on the filesystem.

## 4. Deterministic Test Fixtures
- [ ] Use explicit, static mock fixtures (CSV, JSON, or in-memory data structures) for tests.
- [ ] Avoid dynamic timestamps, random data generators without fixed seeds, or non-deterministic test states.
- [ ] Verify that math, fee calculations, and data transformations produce exact, repeatable values against known reference fixtures.

## 5. Failure Handling and Edge Cases
- [ ] Test boundaries and degenerate inputs: empty files, zero values, missing fields, malformed lines.
- [ ] Verify that exceptions are caught, logged, or propagated cleanly without cryptic crashes.
- [ ] Confirm error messages provide clear diagnostic context to the user.

## 6. Dependency and Security Review
- [ ] Ensure no third-party package was added without explicit justification and discussion.
- [ ] Verify that no API keys, credentials, tokens, or private secrets exist in code, tests, or committed fixtures.
- [ ] Check `.gitignore` to ensure secret files (`.env`), caches, and local configurations are excluded.

## 7. Actual Resource Measurements (When Relevant)
- [ ] Measure execution time for data-intensive loops or test suites.
- [ ] Measure memory usage and disk growth when handling tabular or time-series data.
- [ ] Verify that file handles and network sockets are closed deterministically (e.g., using context managers).

## 8. Cross-Platform Testing (Available Platforms Only)
- [ ] Execute tests and scripts on currently verified, available platforms (e.g., Windows 11 host).
- [ ] Mark untested platforms explicitly (e.g., Android Termux, Linux container) as "Untested" until genuine access is available.
- [ ] Never claim a platform check passed without empirical execution logs from that environment.

## 9. Separation of Offline Tests from Live-System Validation
- [ ] Guarantee that automated test suites are strictly offline: zero outbound HTTP requests, WebSocket connections, or broker calls.
- [ ] Ensure network mocks or dry-run assertions prevent accidental live network traffic during testing passes.
- [ ] Require separate, explicit operational steps for any network-connected or live-system integration verification.

## 10. Status Reporting Standard
All verification reports must categorize every check into one of the following statuses:
- **PASSED**: Directly verified with successful command execution and output.
- **FAILED**: Executed and encountered an error or assertion mismatch (include exact error output).
- **SKIPPED**: Not applicable to the current scope (state rationale).
- **UNTESTED**: Applicable but not executed due to missing hardware, environment, or tooling.
