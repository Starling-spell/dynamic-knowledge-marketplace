# Proof matrix

| Case | Expected state | Published output? | Evidence |
| --- | --- | --- | --- |
| Two complete hashed inputs, faithful combined output, exact PASS vector | `PUBLISHED` | Yes | Direct test and StudioNet |
| Output reverses a source warning, exact FAIL vector | `REJECTED` | No | Direct test and StudioNet |
| Output bytes differ from the committed SHA-256 | `INCONCLUSIVE` | No | Direct test |
| Any semantic criterion is UNKNOWN | `INCONCLUSIVE` | No | Direct test |
| Cross-space input reference | Revert | No | Direct test |
| Same output ID or repeated application | Revert/terminal | No additional asset | Direct test |
| Local/private IP URL or malformed hash | Revert | No | Direct test |

Direct tests mock leader-side web and LLM behavior. Only finalized live calls demonstrate validator consensus. The example documents are fictional process text; the contract judges document transformation fidelity, not whether the process is correct.
