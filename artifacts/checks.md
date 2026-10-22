# Checks and limits

## What was checked
- `python3 artifacts/model.py` (standard library only, no network): 30 arithmetic checks covering hard-limit splits, coverage ratios, constant-product price impact, the hybrid's 72h unlock, the anti-sniper average, option 7 fee math (including the pre-dump loss value) and worked examples of the tranche A cutoff and tranche B credit rules. All passed on 2026-10-22, exit 0.
- Score-table totals in `report.md` were recomputed from the cells, and all 15 rows match.
- The team's public pages were fetched on 2026-10-22 around 19:30 UTC and saved as text in `evidence/`. See `evidence/SOURCES.md`.

## What was NOT checked
- **No independent chain reads.** The 614 holders, the ~830M snapshot figure, the 201,151,260 migrated amount and the ETH/IMD amounts come from the brief and the team's notice. They are stated on-chain-verifiable, but this review did not verify them.
- Whether block 26213125 is before or after the migration transfers (inference I1). It does not change tranche B coverage (~20.7%, report §5.4), but it was not read on chain.
- The block numbers of E (0xE132's last SIMD sale) and B2 (just before its first sale). The plan defines them by those on-chain events; they were not looked up.
- The 62 vs 63 wallet discrepancy between the brief and the team's own pages.
- The Merkle root `0xe842…6347`: it was not rebuilt.
- The Robinhood rug ledger, the new token supply, the IMD pool seed, the factory's actual configurable splits, and any deployed contract.
- The pool math is a simplified constant-product stress test. Concentrated liquidity, fees, arbitrage and buy flow are ignored.

Scores are judgments. This is a recommendation, not an audit, a deployed contract or a refund promise.
