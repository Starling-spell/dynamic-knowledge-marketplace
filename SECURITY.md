# Security and review scope

The contract checks **fidelity of a proposed document transformation**, not the truth of source documents. Anyone may register a source commitment or propose an output; consumers must evaluate source reliability separately.

## Trust boundaries

1. A source registration is merely a URL/hash commitment. It is not fetched or endorsed at registration.
2. During `apply_transform`, leader and validators each fetch complete public source and output bodies. Exact full-byte hashes and HTTP statuses are decision-bearing.
3. The complete `coverage`, `grounding`, `meaning_preserved`, and `category_fit` vector must match exactly. `FAIL` rejects; `UNKNOWN`, unavailable, oversize, invalid UTF-8, or hash mismatch is inconclusive.
4. Only `PUBLISHED` creates a reusable derivative. The raw output remains at its external URL; if that publisher later changes it, future transformations fail the stored hash check.

## Known limits

An attacker can control both public input and output pages and obtain a faithfully transformed but false document. This protocol makes no authenticity or truth claim. Transient source changes can make leader and validators disagree, preventing finalization; use immutable URLs. The hostname check is a syntactic SSRF guard, not a DNS pinning system. StudioNet proofs demonstrate consensus execution on illustrative public artifacts, not real-world water-safety guidance.

No funds, licenses, or legal title are transferred. No certificate can be consumed. Large documents are intentionally rejected, not silently summarized.
