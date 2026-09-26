# DynamicKnowledgeMarketplace

A content-addressed exchange for **document transformations**, not an agent reputation system, truth oracle, graph editor, certificate marketplace, or payment escrow. Participants register public source commitments and propose a `MERGE`, `RESTRUCTURE`, or `EXTRACT` output. The contract itself fetches every input and the proposed output before any derivative asset enters the exchange.

"Marketplace" here means a shared, permissionless venue for reusable knowledge artifacts. There are no payments, ownership transfers, or claims of factual authority.

## Why GenLayer

Deterministic code can check IDs, SHA-256, lineage, and byte limits. It cannot decide whether a rewritten document has preserved a warning, inverted a condition, invented a statement, or covered both inputs of a merge. GenLayer leader and validators independently fetch the complete public texts and derive the same four-field semantic vector:

- `coverage`: operation-specific content coverage;
- `grounding`: no material assertion unsupported by the inputs;
- `meaning_preserved`: no reversed conditions, warnings, negations, or conclusions.
- `category_fit`: the output actually fits its published content category.

Consensus requires exact equality of HTTP statuses, full-response hashes, hash matches, completeness flags, and all four semantic decisions. No confidence tolerance can hide a `FAIL` or `UNKNOWN`. A bad, unavailable, truncated, or hash-mismatched artifact cannot be published.

## Architecture and state

```text
Public HTTPS input(s) + SHA-256 commitments    Public HTTPS proposed output + SHA-256
                    \                          /
                     permissionless transformation proposal
                                      |
                            GenVM independently fetches
                                      |
                     exact validator report comparison
                                      |
                PUBLISHED / REJECTED / INCONCLUSIVE
                                      |
                 immutable derivative asset only on PUBLISHED
```

Inputs are immutable `SOURCE_COMMITMENT` or prior `TRANSFORMED` assets. A proposal is bound to one space, existing input IDs, operation, output ID/URL/hash, and optional extraction focus. The output is a separately hosted public artifact. Successful outputs become new reusable inputs, forming an append-only derivation pipeline with maximum depth four. There is no mutable graph root or generic node/relation API; outputs are full fetched documents. A registered source is **not** verified until a transformation refetches it. A derived asset is not a certificate that its content is true.

Every proposal resolves once. On success, the contract stores a new asset and increases the derived count. On rejection or inconclusive acquisition, no asset is published. The record root binds the complete fetched-evidence report, operation, provenance, and state. Concurrent proposals targeting the same output ID cannot overwrite the first published asset; the loser terminates as `OUTPUT_TAKEN`.

## API

`create_space`, `publish_source`, `propose_transform`, `apply_transform`, `get_space`, `get_asset`, `get_transform`, `get_record`.

`MERGE` requires two distinct inputs and preserves both; `RESTRUCTURE` preserves all material information of one input; `EXTRACT` includes the important information relevant to a bounded focus. In each case, new unsupported assertions or meaning inversion fail. This is transformation fidelity, **not** external fact verification.

## Security boundaries

- HTTPS domain names only; localhost, IP literals, credentials in URL, and fragment URLs are rejected. Public documents are treated as data, never prompt instructions.
- Full raw-response SHA-256 must match each commitment. Complete UTF-8 document bodies are limited to 8,000 bytes each; no clipped excerpt can pass.
- Transform and output IDs are unique within a space; space IDs namespace assets and proposals. Immutable lineage and bounded depth prevent replay, substitution, and recursive cycles.
- Each validator independently reacquires and interprets the actual input and output bodies. A malformed semantic response becomes `UNKNOWN`, never approval.
- The exchange does not establish truth, legal rights, scientific quality, publisher independence, or safe operational practice. See [SECURITY.md](SECURITY.md).

## Verify and deploy

```powershell
python -m pip install genvm-linter genlayer-test pytest
genvm-lint check contracts/DynamicKnowledgeMarketplace.py
pytest tests/direct -q
genlayer network set studionet
genlayer deploy --contract contracts/DynamicKnowledgeMarketplace.py
genlayer receipt <deployment-tx> --status FINALIZED
genlayer code <contract-address>
```

The pinned GenVM runner is on the first contract line. Direct tests exercise state guards and mocked acquisition/LLM results; they do not exercise independent validators. See [PROOF_MATRIX.md](PROOF_MATRIX.md) for test intent and [LIVE_PROOFS.md](LIVE_PROOFS.md) for finalized StudioNet results.
