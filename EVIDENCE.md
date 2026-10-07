# Evidence index

- `evidence/fixtures/original.md`: synthetic educational reference experiment.
- `evidence/fixtures/negative-replication.md`: comparable synthetic negative attempt.
- `evidence/fixtures/positive-replication.md`: comparable synthetic positive attempt.
- `evidence/local-tests.txt`: complete local test result.
- `evidence/genvm-validation.txt`: official lint, SDK validation and typecheck result.
- Deployment/live receipts: absent; not yet executed.
- Canonical source SHA-256: `614795a209d50e4e6d8abb716d474f56e6439bb0ea9121d8b43346dced452668`.
- Local source/fixture commit: `57f16921191fd9d1f49ea8fed64b01f820134356` (not pushed).
- Local verification: **58 tests passed**, official lint and SDK validation passed, SDK typecheck passed.
- GitHub readback confirmed only the initialization README after automatic approval review rejected the implementation push.

The demonstrator tests scientific comparison of synthetic data under explicit synthetic terms. It is not verification of a real paper, laboratory experiment or researcher's identity.

Official references inspected on 2026-10-07:

- https://docs.genlayer.com/developers/intelligent-contracts/features/value-transfers
- https://docs.genlayer.com/developers/intelligent-contracts/features/transaction-context
- https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle
- https://docs.genlayer.com/api-references/genlayer-linter
- https://docs.genlayer.com/developers/networks
- https://sdk.genlayer.com/main/_static/ai/api.txt (latest includes RC APIs)

The installed v0.2.16 SDK source confirms `Response.status`, `exec_prompt(response_format='json')`, transaction-pinned `datetime.now`, custom `run_nondet_unsafe` and EVM-interface `emit_transfer`. Its actual source and the current Studio template take precedence over stale tutorial snippets using `status_code`.
