# ReproBond

**Evidence-authenticated scientific replication bounties with GenLayer methodology judgment and deterministic rewards.**

A sponsor locks an experiment's hypothesis, exact protocol, methodology, deviations, report requirements, original document fingerprint, reward and deadline. Researchers submit public replication reports. GenLayer independently retrieves the committed documents and judges whether the work is comparable and what the result means. A scientifically valid **negative replication earns exactly the same reward as a positive one**.

This is an Intelligent Contract repository. Use GenLayer Studio's built-in accounts; there is no website, wallet-connect, backend, authentication or database.

## Why GenLayer

Hashes can authenticate bytes, but cannot determine whether methodological deviations invalidate a replication. GenLayer validators independently fetch the original and replication evidence, apply the locked protocol, reproduce the qualitative review and reach consensus. Deterministic Python controls permissions, custody, deadlines, submission ordering, credits and settlement. The LLM cannot select recipients, transfer funds or change terms.

## Lifecycle and workflow

1. `create_bounty(terms_json, deadline, bond, source_limit)` with positive GEN value locks all terms immediately. Deadline is Unix seconds, 60 seconds to 90 days ahead; adjudication grace is fixed at 24 hours. Values are integer wei.
2. Sponsor calls `authorize_package(bounty_id, researcher, evidence_json)` to irrevocably bind a package to one researcher. This is a permissioned sponsor authorization step, not an unrestricted research registry. Authenticate researcher ownership off-chain before authorizing. A package or any of its exact content hashes cannot be rebound inside that bounty.
3. Bound researcher calls payable `submit` before the deadline with exactly the required bond. Public evidence is fetched and SHA-256/length authenticated through exact consensus. Replays and copying from another address are rejected before fetching.
4. Anyone calls `adjudicate_next`. Only the earliest unadjudicated submission can be examined. Both `REPLICATED` and `FAILED_TO_REPLICATE` qualify if methodology >=80, quality >=70 and no material deviations. `INVALID_REPLICATION` and `INCONCLUSIVE` receive no reward. All bonds are returned without slashing.
5. First qualifying submission changes `OPEN` to `AWARDED`, assigns its reward as withdrawable credit, and returns every outstanding bond. Subsequent adjudications/submissions are rejected. If no work qualifies, anyone can `expire` after the deadline (or deadline +24h when work remains pending), changing `OPEN` to `REFUNDED` and crediting the sponsor and outstanding researchers. An inconclusive decision is terminal for that submission, not indefinitely retried.
6. Each credited account calls `withdraw` directly. It clears that account's credit once and emits the supported external transfer message. **AWARDED/REFUNDED mean credit assigned; withdrawal emission and recipient delivery must be verified separately.**

Stored inputs and verdicts are append-only; each bounty mutation adds a timestamped state hash to history. No terms editor, owner override, deadline extension or upgrade method exists.

## Evidence and judgment

`terms_json` has precisely these fields: `title`, `paper` (fingerprint object), `hypothesis`, `protocol`, `methodology`, `allowed_deviations`, `disallowed_deviations`, `report_fields`, `minimum_evidence`. Text fields are 1..2000 characters; total terms <=12000 characters.

`evidence_json` is a JSON array of 1..source_limit fingerprints:

```json
[{"url":"https://raw.githubusercontent.com/OWNER/REPO/40_LOWERCASE_HEX_COMMIT/path/report.md","sha256":"64_lowercase_hex_characters","bytes":793}]
```

The URL example is a template, not a valid transaction argument. Run `scripts/prepare_demo.py COMMIT` to obtain exact fixture inputs. Each body must be UTF-8, <=24000 bytes. Only canonical commit-pinned raw GitHub HTTPS sources are admitted in v1; Zenodo/OSF/PDF adapters are intentionally outside the supported evidence format. Up to four replication sources and eight packages/submissions per bounty. The original fingerprint is authenticated on creation and rechecked at adjudication.

Exact consensus authenticates status/length/SHA-256 receipts. Each qualitative leader and validator **retrieves and authenticates the sources again**, not merely a stored leader description. The custom validator independently reproduces the review, requires the exact outcome, tolerates scores by at most 10 points, applies the same eligibility gates and compares reasoning/deviations/citations through semantic review. Strict JSON validation prohibits unknown keys, non-integer scores, unlocked citations and rewards for uncertainty. Authentication failure yields an explicit `INCONCLUSIVE` receipt with no reward. LLM/schema/consensus failures revert; deterministic expiry remains available.

A verdict stores outcome, methodology score, deviations, citations, evidence quality, reasoning, authenticated manifest and policy version. `decision_hash` is SHA-256 of canonical JSON binding chain ID, contract address, bounty ID, immutable terms hash, submission ID, researcher, package hash and full accepted result.

## Trust and security

Evidence fingerprints authenticate a document, not its real-world truth, author identity or ethical compliance. Sponsor authorization binds the reward beneficiary; it cannot prove research authorship and assumes the sponsor nominates the intended researcher. Private blinded experiments and identity verification are external responsibilities. See [SECURITY.md](SECURITY.md) for boundaries and adversarial cases.

## Tests and verification

Python 3.12, official GenLayer Test direct runner, GenVM v0.2.16, SDK runner matching the stable Studio template:

```bash
pip install -r requirements-dev.txt
python -m pytest -q
genvm-lint check contracts/reprobond.py
genvm-lint typecheck contracts/reprobond.py
```

Tests execute the real SDK-backed contract/storage with mocked web and LLM inputs. Independent validator callbacks are exercised with forged outcomes and changed evidence. Transfer assertions capture the SDK's actual `EthSend` payload; they do **not** prove recipient delivery. These tests cover all outcomes, funding, authorization, copying/rebinding, deadlines/grace, hash/length/inaccessibility, URL/evidence bounds, ordering, one-time settlement, withdrawal permissions, decision hashes, history, refunds and accounting conservation.

Conservation: `deposited = escrow + credits + withdrawn` (withdrawn denotes emitted transfer amount). CI runs the same tests/lint/typecheck. Local results: [evidence/local-tests.txt](evidence/local-tests.txt), [evidence/genvm-validation.txt](evidence/genvm-validation.txt).

## Deployment and evidence

See [DEPLOYMENT.md](DEPLOYMENT.md) and [EVIDENCE.md](EVIDENCE.md) for exact commit/source binding, transaction records and honest live verification status. Fixture reports are synthetic educational data and must not be presented as real laboratory research.

Deployment verified: [contract explorer](https://explorer-studio.genlayer.com/address/0x3388D50Be10c907e55382C798783DB4012fE4aA2), Normal Full Consensus, FINALIZED / SUCCESS. Source commit `de0670da4f5b36769e5698157be9a5aa060da2a7` matches complete deployed Code readback byte-for-byte. A live 1 GEN synthetic bounty finalized **FAILED_TO_REPLICATE** (methodology 90, quality 85), awarded the separate researcher, and completed withdrawal plus a finalized 1 GEN child transfer. Recipient explorer balance is 1 GEN; remaining credit and contract balance are zero. See DEPLOYMENT.md and evidence/ for every receipt and final state. This is simulated Studio GEN and synthetic educational evidence.
