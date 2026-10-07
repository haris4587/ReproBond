# Evidence index

- `evidence/fixtures/original.md`: synthetic educational reference experiment.
- `evidence/fixtures/negative-replication.md`: comparable synthetic negative attempt.
- `evidence/fixtures/positive-replication.md`: comparable synthetic positive attempt.
- `evidence/local-tests.txt`: complete local test result.
- `evidence/genvm-validation.txt`: official lint, SDK validation and typecheck result.
- `evidence/deployment-receipt.txt`: explorer's finalized deployment receipt and execution details.
- `evidence/deployment-finalized.jpg`: finalized deployment screenshot.
- `evidence/deployed-source.py`: full byte-identical deployed source readback.
- `evidence/demo-inputs.json`: exact executed demo inputs and source commit.
- `evidence/create-bounty-receipt.txt`, `authorization-receipt.txt`, `submission-receipt.txt`: finalized successful funding, binding and submission.
- `evidence/adjudication-receipt.txt`, `adjudication-finalized.jpg`: finalized negative replication verdict and validator votes.
- `evidence/finalized-bounty.json`: AWARDED state, scores, manifest, terms and decision hash.
- `evidence/hash-verification.json`: independent recomputation of terms/package/decision hashes.
- `evidence/credit-before-withdrawal.txt`, `credit-after-withdrawal.txt`: finalized 1 GEN credit before withdrawal and zero afterward.
- `evidence/withdrawal-receipt.txt`: finalized successful withdrawal emission.
- `evidence/payout-receipt.txt`, `payout-finalized.jpg`: separate finalized 1 GEN transfer to researcher.
- `evidence/recipient-balance.txt`: explorer confirms recipient balance 1 GEN.
- `evidence/finalized-accounting.json`: final conservation, zero escrow/credits, 1 GEN withdrawn.
- `evidence/live-verification.json`: machine-readable deployment, transactions, source binding and final results.
- `evidence/demo-handoff.jpg`, `finalized-accounting.txt`: historical pre-demo records, superseded by final records above.
- Canonical source SHA-256: `614795a209d50e4e6d8abb716d474f56e6439bb0ea9121d8b43346dced452668`.
- Published source/fixture commit: `de0670da4f5b36769e5698157be9a5aa060da2a7`.
- Local verification: **58 tests passed**, official lint and SDK validation passed, SDK typecheck passed.
- Deployment: **FINALIZED / SUCCESS**, Normal Full Consensus, five initial validators.
- Live bounty/adjudication/withdrawal/payout: **all finalized**. Negative replication rewarded; 1 simulated GEN delivered to the researcher and verified in explorer balance.

The demonstrator tests scientific comparison of synthetic data under explicit synthetic terms. It is not verification of a real paper, laboratory experiment or researcher's identity.

Official references inspected on 2026-10-07:

- https://docs.genlayer.com/developers/intelligent-contracts/features/value-transfers
- https://docs.genlayer.com/developers/intelligent-contracts/features/transaction-context
- https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle
- https://docs.genlayer.com/api-references/genlayer-linter
- https://docs.genlayer.com/developers/networks
- https://sdk.genlayer.com/main/_static/ai/api.txt (latest includes RC APIs)

The installed v0.2.16 SDK source confirms `Response.status`, `exec_prompt(response_format='json')`, transaction-pinned `datetime.now`, custom `run_nondet_unsafe` and EVM-interface `emit_transfer`. Its actual source and the current Studio template take precedence over stale tutorial snippets using `status_code`.
