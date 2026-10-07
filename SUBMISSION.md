# Submission draft — not ready for submission until live verification

**Project name:** ReproBond

**One-liner:** Evidence-authenticated scientific replication bounties with GenLayer methodology judgment and deterministic rewards.

**Description:** ReproBond lets sponsors fund and lock a scientific replication protocol, including methodology, allowed deviations, report requirements and a public original document fingerprint. Sponsor authorization binds each replication evidence package to its intended researcher. GenLayer validators independently retrieve and authenticate commit-pinned public evidence, assess methodological comparability and classify results as REPLICATED, FAILED_TO_REPLICATE, INVALID_REPLICATION or INCONCLUSIVE. Positive and negative valid replications qualify equally for the first-valid-attempt reward. Deterministic rules control native funding, optional refundable bonds, submission ordering, evidence caps, deadlines, withdrawal credits and timeout refunds. Inputs, authenticated manifests and decision hashes remain auditable on-chain once deployed. No website, external wallet connection, backend or database is required.

**Suggested tags:** AI & Agents; Verifiable Inference; Science / DeSci if available (confirm exact portal choices).

**Canonical repository:** https://github.com/haris4587/ReproBond

**Contract address:** `0x3388D50Be10c907e55382C798783DB4012fE4aA2`.

**Explorer:** https://explorer-studio.genlayer.com/address/0x3388D50Be10c907e55382C798783DB4012fE4aA2

**Deployment transaction:** `0x6c5520e612d5b641ec7bb6b71f479ca3d6ae26611a7257e35dec1e4dcab069ec` — FINALIZED / SUCCESS, Normal (Full Consensus), five validators.

**Live bounty transactions:** absent; automatic approval review blocked the payable creation step.

**Source commit:** `de0670da4f5b36769e5698157be9a5aa060da2a7` — published on canonical main, deployed source readback byte-identical.

**Canonical source SHA-256:** `614795a209d50e4e6d8abb716d474f56e6439bb0ea9121d8b43346dced452668`.

**Local verification:** 58 SDK-backed tests passed; official GenVM lint, validation and SDK typecheck passed.

**Live verification:** Full Consensus deployment verified; funded bounty, qualitative adjudication, reward credits and payout delivery remain pending. Not ready for final submission.

**Evidence:** local test log, GenVM check log and synthetic original/positive/negative reports in `evidence/`. Public commit-pinned fixture URLs are published at the source commit. `scripts/prepare_demo.py` produces their exact inputs.

**Why GenLayer is central:** scientific methodology comparison requires qualitative interpretation of locked protocol and evidence; validators independently reproduce that judgment. Reward recipients and accounting are deterministic and cannot be selected by the LLM.

**Prepared files:**

- `contracts/reprobond.py`
- `tests/test_reprobond.py`
- `evidence/fixtures/original.md`
- `evidence/fixtures/negative-replication.md`
- `evidence/fixtures/positive-replication.md`
- `evidence/local-tests.txt`
- `evidence/genvm-validation.txt`
- `scripts/prepare_demo.py`
- `.github/workflows/check.yml`
- `.gitignore`
- `requirements-dev.txt`
- `README.md`, `SECURITY.md`, `DEPLOYMENT.md`, `EVIDENCE.md`, `SUBMISSION.md`

**Publication status:** Implementation and fixtures published to canonical main following explicit user approval. Deployment receipt, exact source readback and pending demo inputs are recorded in evidence/. Screenshots are supplied in the conversation because GitHub binary upload failed. See DEPLOYMENT.md for the automatic approval review blocker and exact handoff.
