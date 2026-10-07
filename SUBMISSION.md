# Submission draft — not ready for submission until live verification

**Project name:** ReproBond

**One-liner:** Evidence-authenticated scientific replication bounties with GenLayer methodology judgment and deterministic rewards.

**Description:** ReproBond lets sponsors fund and lock a scientific replication protocol, including methodology, allowed deviations, report requirements and a public original document fingerprint. Sponsor authorization binds each replication evidence package to its intended researcher. GenLayer validators independently retrieve and authenticate commit-pinned public evidence, assess methodological comparability and classify results as REPLICATED, FAILED_TO_REPLICATE, INVALID_REPLICATION or INCONCLUSIVE. Positive and negative valid replications qualify equally for the first-valid-attempt reward. Deterministic rules control native funding, optional refundable bonds, submission ordering, evidence caps, deadlines, withdrawal credits and timeout refunds. Inputs, authenticated manifests and decision hashes remain auditable on-chain once deployed. No website, external wallet connection, backend or database is required.

**Suggested tags:** AI & Agents; Verifiable Inference; Science / DeSci if available (confirm exact portal choices).

**Canonical repository:** https://github.com/haris4587/ReproBond

**Contract address / Explorer / deployment transaction / live transactions:** unavailable — deployment and live test not performed.

**Source commit:** `57f16921191fd9d1f49ea8fed64b01f820134356` locally; not pushed, not deployed.

**Canonical source SHA-256:** `614795a209d50e4e6d8abb716d474f56e6439bb0ea9121d8b43346dced452668`.

**Local verification:** 58 SDK-backed tests passed; official GenVM lint, validation and SDK typecheck passed.

**Live verification:** pending; do not claim Full Consensus or payout delivery.

**Evidence:** local test log, GenVM check log and synthetic original/positive/negative reports in `evidence/`. Public commit-pinned fixture URLs become available only after the source commit is pushed. `scripts/prepare_demo.py` produces their exact inputs.

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

**Publication status:** Only the initialization README was confirmed on GitHub. Automatic approval review rejected publishing the implementation to default main because the uploaded brief was not recognized as trusted publication authorization. Explicit user approval is required before retrying the push. No alternative publication path has been used.
