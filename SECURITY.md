# Security model

## Deterministic enforcement

- Native payable funding and exact optional bonds, u256 accounting, one-time credits/withdrawals.
- Locked terms on creation; no extension, administration, replacement, terms edit or upgrade entry point.
- Sender-bound sponsor authorization with a unique immutable package owner. Another sender cannot submit even identical evidence. Same content hash cannot be reauthorized with another URL or manifest inside a bounty. Sponsor authorization is permissioned and must reflect intended authorship; a malicious sponsor can misattribute unbound work. This is not cryptographic proof of authorship. Independent bounties are independent grants; cross-bounty use requires fresh sponsor authorization.
- At most eight preauthorized packages and submissions. Only the earliest unresolved submission can be adjudicated; first valid completed replication wins. Negative results qualify equally. Bonds are always refundable, including invalid/inconclusive or abandoned submissions.
- No new submissions at deadline; adjudication allowed through exact grace boundary; expiry allowed strictly after it when work is pending. With no pending work expiry is allowed strictly after submission deadline. No AI dependency in recovery.
- Award/refund are terminal for the bounty. Pending losing submissions keep their original records and get bonds returned; they are not fictitiously adjudicated.
- Decision hashes bind deployment domain, bounty, researcher, package, exact terms and full accepted verdict. History is append-only, reads bounded to 50 events.

## Evidence boundary

- Narrow allowlist admits only raw.githubusercontent.com with an exact 40-character lowercase hex commit and canonical ASCII path. No ports, userinfo, query, fragment, percent escapes, dot/empty path segments, localhost, IP literals or mutable branch paths.
- Reject duplicate URLs and body hashes. One to four reports, each 1..24000 bytes, plus original source. UTF-8 only. Response must be status 200, expected byte length and SHA-256.
- SDK fetches response before the contract can check its length; the cap bounds accepted data and prompts, not remote transport bandwidth or SDK-level resource consumption. GenVM resource limits remain necessary. SDK redirect policy is outside contract control; any redirected body still must match committed exact bytes. The strict authority allowlist limits entry points.
- Exact consensus for authenticated receipts; independent re-fetch again for each qualitative review. Changed/inaccessible sources cannot qualify. Transient disagreement can make a transaction undetermined; the fixed expiry recovers funds regardless.
- Every source and natural-language term is untrusted input. Explicit prompt policy forbids embedded instructions, new sources or code execution. No LLM decision can bypass deterministic eligibility, sender, time or accounting checks. Prompt injection robustness remains probabilistic; hashes do not make prose trustworthy.
- Canonical hashing uses ASCII JSON, sorted keys and compact separators. Input SHA must be lowercase 64-hex; lengths integer (booleans rejected). Zero reward and zero researcher rejected.

## Settlement boundary

Withdrawals emit the official SDK external value-only message to the credited sender. Contract credits clear before emission and runtime transaction rollback protects synchronous execution failures. EOA-direct requirement avoids beneficiary substitution and caller-selected destinations. Sender must equal transaction origin, but this comparison alone is not an on-chain proof of account code absence. Do not authorize smart-contract recipients whose receive path can fail.

External message delivery is platform-managed and must be verified from finalized receipts and recipient balance. `withdrawn` records emission, not an independently observed delivery acknowledgement. The SDK documentation warns that failed child delivery may not return funds automatically. ReproBond does not claim universal recovery from chain/platform failure or recipient rejection. It guarantees deterministic credit recovery for protocol deadlines and AI/evidence failure, under supported recipient transfer semantics. Never deploy for production custody without auditing platform delivery/retry behavior.

Studio simulates GEN. A successful Studio payout proves sandbox accounting and supported transfer execution, not a mainnet financial transaction.

## Verification

Run the entire repository test suite and official GenVM lint/validation/typecheck. The mock transfer test inspects the real SDK payload, not a handmade transfer function. Live consensus and delivery require separate public receipts. Report vulnerabilities privately to the repository owner before publishing exploit details; no external audit or production-readiness claim is made.
