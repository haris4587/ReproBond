# Deployment and live verification

Stable Studionet, chain **61999**, Studio built-in accounts only. All write transactions used **Normal (Full Consensus)** with Simulation Mode unchecked. No external wallet or website is required.

## Exact source binding

- Published deployment source/fixture commit: `de0670da4f5b36769e5698157be9a5aa060da2a7`.
- Source: `contracts/reprobond.py`, 17,323 bytes.
- SHA-256: `614795a209d50e4e6d8abb716d474f56e6439bb0ea9121d8b43346dced452668`.
- Contract: `0x3388D50Be10c907e55382C798783DB4012fE4aA2`.
- [Contract explorer](https://explorer-studio.genlayer.com/address/0x3388D50Be10c907e55382C798783DB4012fE4aA2).
- Explorer Code readback: `evidence/deployed-source.py`; byte-for-byte identical to the canonical published source.
- GenVM v0.2.16 with the stable Studio template's pinned SDK runner. Local checks pass against these exact source bytes.

Subsequent commits contain evidence/documentation only; source and fixtures remain byte-identical to the deployment commit. The final evidence commit is available in GitHub main history and is reported separately from the source commit in the completion response.

## Finalized transactions

| Step | Public transaction | Verified result |
| --- | --- | --- |
| deployment | [receipt](https://explorer-studio.genlayer.com/tx/0x6c5520e612d5b641ec7bb6b71f479ca3d6ae26611a7257e35dec1e4dcab069ec) | FINALIZED / SUCCESS |
| create_bounty | [receipt](https://explorer-studio.genlayer.com/tx/0xb4236730cec819139cc05b7a8c36ae5732e661fe62db897470416d0ccbd3b68e) | FINALIZED / SUCCESS |
| authorize_package | [receipt](https://explorer-studio.genlayer.com/tx/0xfff5c2e9c8806ffe9aee47f58bb42307f6616844754c58b55fa1dc73a2e09b18) | FINALIZED / SUCCESS |
| submit | [receipt](https://explorer-studio.genlayer.com/tx/0xe38de343ca9a7b314154dc148be8534a275831f0315a64220942503f778b8d86) | FINALIZED / SUCCESS |
| adjudicate_next | [receipt](https://explorer-studio.genlayer.com/tx/0x5c883f2ff150cb72d3c8f33d2828e4b336318695fe092ec9cc2b74c497a4d40e) | FINALIZED / SUCCESS |
| withdraw | [receipt](https://explorer-studio.genlayer.com/tx/0xea648c87d629ab5042a7ee5b366fc1e93cb432f0f9f322dc66f33693b358caf7) | FINALIZED / SUCCESS |
| payout | [receipt](https://explorer-studio.genlayer.com/tx/0x7555160b48454abf86b2b328fe34a3b1cf7006f962d06675698f3e32a88de972) | FINALIZED / 1 GEN Send |

The user performed the final create_bounty click after an automatic approval review handoff. That attempt succeeded; all remaining steps were completed through Studio. The initial fractional input 0.01 failed before submission because Studio requires an integer. Input 1 was confirmed as **1 GEN = 10^18 wei** by finalized state and the payout receipt. No outstanding handoff remains.

## Live synthetic negative replication

Sponsor: `0x416F700cC2c738D76E8Cd759d6293b98B820B0A0`, faucet-funded with 10 simulated GEN. Created bounty **0** with 1 GEN, deadline `1791399000` (2026-10-07 18:50 UTC), bond 0, evidence limit 1. A separate built-in researcher `0x5fadd4bfe32A7aF03a405670fD4655EdaF2c67E3` started at 0 GEN, received an irrevocable authorization for the exact negative-report manifest and submitted it with zero bond.

Both the original and replication bytes were independently authenticated. Full Consensus finalized **FAILED_TO_REPLICATE**, methodology **90/100**, evidence quality **85/100**, no material deviations. The synthetic mean period of 2.30 s falls outside 1.90–2.10 s while following the locked methodology. Bounty became **AWARDED**, winner submission 0; credit became 10^18 wei. Adjudication showed three Agree votes, one Disagree and one idle validator cancelled after quorum; do not claim unanimity.

Decision hash: `e013e95075c3c06de585b363d17a03f11885151e945fcce75cb11517e4e54122`. Terms, package and decision hashes were independently recomputed and matched.

The researcher withdrew directly. Withdrawal finalized SUCCESS, output 10^18 wei. Its separate **Send** child transaction finalized for 1 GEN to the researcher. The explorer independently confirmed recipient balance **1 GEN**, contract balance **0 GEN**, and finalized credit readback **0 wei**.

Final accounting (wei): deposited **10^18**, escrow **0**, credits **0**, withdrawn **10^18**. Conservation holds. Withdrawal emission and delivery were both observed; these remain distinct stages in the contract's accounting.

## Scope and reproduction

This demonstrates public synthetic educational evidence under terms explicitly accepting synthetic reports. It does not verify a real paper, researcher identity or laboratory experiment. GEN balances are simulated in Studio; this is not mainnet funding. [Official transfer documentation](https://docs.genlayer.com/developers/intelligent-contracts/features/value-transfers) describes Studio's balance model.

Run `python scripts/prepare_demo.py de0670da4f5b36769e5698157be9a5aa060da2a7` to generate commit-pinned fixture inputs with a fresh deadline. Use the supported integer Studio GEN input and verify its actual value in finalized state. Follow create → authorize distinct researcher → submit exact manifest/bond → adjudicate → read finalized award/credit → withdraw → inspect child transfer and recipient balance. Never commit private keys or session credentials.
