# Deployment

Target: stable Studionet, chain 61999, https://studio.genlayer.com/api, built-in Studio accounts only.

Source uses GenVM v0.2.16 and the runner advertised by the stable Studio template. Current generic SDK documentation includes release-candidate APIs; do not change the pinned runner without validating network support.

## Status

Canonical published source and fixture commit: `de0670da4f5b36769e5698157be9a5aa060da2a7`.
Source SHA-256: `614795a209d50e4e6d8abb716d474f56e6439bb0ea9121d8b43346dced452668`.
Contract: `0x3388D50Be10c907e55382C798783DB4012fE4aA2`.
Sponsor built-in Studio account: `0x416F700cC2c738D76E8Cd759d6293b98B820B0A0`.
Deployment: [finalized receipt](https://explorer-studio.genlayer.com/tx/0x6c5520e612d5b641ec7bb6b71f479ca3d6ae26611a7257e35dec1e4dcab069ec).
Explorer: [contract](https://explorer-studio.genlayer.com/address/0x3388D50Be10c907e55382C798783DB4012fE4aA2).

Deployment was executed in Normal (Full Consensus) mode. Explorer readback shows FINALIZED, GenVM SUCCESS, consensus Accepted, five initial validators, rotation count zero. Explorer Code readback was saved as `evidence/deployed-source.py` and compared byte-for-byte with the published source: identical, 17,323 bytes. Finalized accounting is all zero; no funded bounty exists yet.

## Remaining live verification blocker

The built-in faucet credited the sponsor 10 simulated GEN. The prepared fractional input `0.01` failed in Studio before transaction submission with: `The number 0.01 cannot be converted to a BigInt because it is not an integer`. Automatic approval review then rejected the integer retry as a changed consequential payable amount despite the user's broad approval and official documentation confirming simulated Studio balances. No alternate transaction path was used. The form is prepared with integer value input `1`, bond `0`, source limit `1`, synthetic fixture terms, and deadline `1791399000` (2026-10-07 18:50 UTC). Actual value units must be checked from the receipt: the UI label is GEN, but its integer conversion requires verification.

The user must perform the final Send Transaction click in the prepared browser. If the deadline has passed, replace it with Unix seconds at least 60 seconds and at most 90 days ahead. Then verify finalized creation, authorize a distinct built-in researcher, submit, adjudicate in Full Consensus, and verify credit, withdrawal emission and actual recipient delivery. No live verdict, funded escrow, reward or payout is claimed. Studio's documentation says balances are simulated and that no EVM layer or ghost contracts exist there; external payout behavior must be observed, not inferred from local SDK tests.

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
