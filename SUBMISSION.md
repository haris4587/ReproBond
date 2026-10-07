# ReproBond submission package

**Project name:** ReproBond

**One-liner:** Evidence-authenticated scientific replication bounties with GenLayer methodology judgment and deterministic rewards.

**Description:** ReproBond lets sponsors fund and lock a scientific replication protocol, including methodology, allowed deviations, report requirements and a public original document fingerprint. Sponsor authorization binds each replication evidence package to its intended researcher. GenLayer validators independently retrieve and authenticate commit-pinned public evidence, assess methodological comparability and classify results as REPLICATED, FAILED_TO_REPLICATE, INVALID_REPLICATION or INCONCLUSIVE. Positive and negative valid replications qualify equally for the first-valid-attempt reward. Deterministic rules control native funding, optional refundable bonds, submission ordering, evidence caps, deadlines, withdrawal credits and timeout refunds. Inputs, authenticated manifests and decision hashes remain auditable on-chain once deployed. No website, external wallet connection, backend or database is required.

**Suggested tags:** AI & Agents; Verifiable Inference; Science / DeSci if available (confirm exact portal choices).

**Canonical repository:** https://github.com/haris4587/ReproBond

**Contract address:** `0x3388D50Be10c907e55382C798783DB4012fE4aA2`.

**Explorer:** https://explorer-studio.genlayer.com/address/0x3388D50Be10c907e55382C798783DB4012fE4aA2

**Deployment transaction:** `0x6c5520e612d5b641ec7bb6b71f479ca3d6ae26611a7257e35dec1e4dcab069ec` — FINALIZED / SUCCESS, Normal (Full Consensus), five validators.

**Live bounty transactions:** all finalized; see the transaction table in [DEPLOYMENT.md](DEPLOYMENT.md) and [evidence/live-verification.json](evidence/live-verification.json).

**Source commit:** `de0670da4f5b36769e5698157be9a5aa060da2a7` — published on canonical main, deployed source readback byte-identical.

**Canonical source SHA-256:** `614795a209d50e4e6d8abb716d474f56e6439bb0ea9121d8b43346dced452668`.

**Local verification:** 58 SDK-backed tests passed; official GenVM lint, validation and SDK typecheck passed.

**Live verification:** Completed Full Consensus funded bounty → signer-bound evidence → authenticated submission → FAILED_TO_REPLICATE (90 methodology, 85 quality) → AWARDED → finalized withdrawal → finalized 1 GEN child transfer. Recipient balance 1 GEN, remaining credit 0, contract balance 0; all accounting conserved. Synthetic educational reports and simulated Studio GEN.

**Evidence:** local test log, GenVM check log and synthetic original/positive/negative reports in `evidence/`. Public commit-pinned fixture URLs are published at the source commit. `scripts/prepare_demo.py` produces their exact inputs.

**Why GenLayer is central:** scientific methodology comparison requires qualitative interpretation of locked protocol and evidence; validators independently reproduce that judgment. Reward recipients and accounting are deterministic and cannot be selected by the LLM.

**Final files pushed:**

- `.github/workflows/check.yml`
- `.gitignore`
- `DEPLOYMENT.md`
- `EVIDENCE.md`
- `README.md`
- `SECURITY.md`
- `SUBMISSION.md`
- `contracts/reprobond.py`
- `evidence/adjudication-finalized.jpg`
- `evidence/adjudication-receipt.txt`
- `evidence/authorization-receipt.txt`
- `evidence/create-bounty-receipt.txt`
- `evidence/credit-after-withdrawal.txt`
- `evidence/credit-before-withdrawal.txt`
- `evidence/demo-handoff.jpg`
- `evidence/demo-inputs.json`
- `evidence/deployed-source.py`
- `evidence/deployment-finalized.jpg`
- `evidence/deployment-receipt.txt`
- `evidence/finalized-accounting.json`
- `evidence/finalized-accounting.txt`
- `evidence/finalized-bounty.json`
- `evidence/fixtures/negative-replication.md`
- `evidence/fixtures/original.md`
- `evidence/fixtures/positive-replication.md`
- `evidence/genvm-validation.txt`
- `evidence/hash-verification.json`
- `evidence/live-verification.json`
- `evidence/local-tests.txt`
- `evidence/payout-finalized.jpg`
- `evidence/payout-receipt.txt`
- `evidence/recipient-balance.txt`
- `evidence/submission-receipt.txt`
- `evidence/withdrawal-receipt.txt`
- `requirements-dev.txt`
- `scripts/prepare_demo.py`
- `tests/test_reprobond.py`

**Publication status:** Implementation and fixtures published to canonical main following explicit user approval. Deployment and live receipts, exact source readback, final state, hash verification and screenshots are published in evidence/. No outstanding browser handoff remains.

## Copy-ready contribution notes (under 1,000 characters)

ReproBond is a scientific replication bounty Intelligent Contract. Sponsors fund and lock the hypothesis, methodology, deviations and evidence requirements. Researcher-bound manifests prevent copied evidence from claiming another researcher’s reward. Validators independently re-fetch commit-pinned public evidence, authenticate SHA-256/length exactly, and reproduce qualitative methodology review. REPLICATED and FAILED_TO_REPLICATE qualify equally; invalid/inconclusive work earns no reward. Deterministic rules enforce ordering, deadlines, bonds, credits, one-time withdrawal and timeout refunds. 58 SDK-backed tests and official GenVM checks pass. Live Studio Full Consensus verified a synthetic negative replication (methodology 90, quality 85), a funded 1 GEN award, finalized withdrawal and child transfer, recipient balance 1 GEN, and zero remaining credit/escrow. Exact deployed source matches GitHub. Studio GEN is simulated; fixtures are educational, not real laboratory evidence.
