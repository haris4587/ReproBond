# Deployment

Target: stable Studionet, chain 61999, https://studio.genlayer.com/api, built-in Studio accounts only.

Source uses GenVM v0.2.16 and the runner advertised by the stable Studio template. Current generic SDK documentation includes release-candidate APIs; do not change the pinned runner without validating network support.

## Status

Canonical source and fixture commit (local, not pushed): `57f16921191fd9d1f49ea8fed64b01f820134356`.
Source SHA-256: `614795a209d50e4e6d8abb716d474f56e6439bb0ea9121d8b43346dced452668`.
Deployment transaction/address: not deployed.
Full Consensus live test: not yet executed.
Publication is blocked: automatic approval review rejected the attempted push to canonical main because the attached brief was not treated as trusted end-user authorization for publication. GitHub was read back and still contains only the initialization README, commit `1c0b30eb1e7f65f9c343b7367b425cac70ae9e1c`. The implementation was not pushed. No deployment or live consensus claim is made. Publish the source after explicit user approval, then perform the procedure below and update records from finalized receipts.

Source remains byte-identical in subsequent documentation commits. The source commit identifies immutable contract/fixture contents; an evidence-only commit can record deployment without claiming to be the earlier source commit.

## Procedure

1. Run all tests and GenVM checks against `contracts/reprobond.py`.
2. Commit/push the exact source and public fixtures to canonical main.
3. Calculate the source SHA-256, import the exact file into Studio and deploy using Full Consensus.
4. Use `scripts/prepare_demo.py SOURCE_COMMIT` to generate locked fixture arguments.
5. Use faucet GEN and a built-in sponsor account to create a funded bounty. Authorize a distinct built-in researcher address; researcher submits exact evidence and optional bond.
6. Adjudicate with Full Consensus. Verify finalized success, outcome, decision hash, credits and conservation from finalized state.
7. Withdraw from the credited researcher; inspect finalized transfer and balance separately from credit assignment.
8. Save receipts, source comparison, state and screenshots. Push evidence-only documentation commit; its source bytes must equal the deployment commit.

No private keys or Studio session credentials may be committed.
