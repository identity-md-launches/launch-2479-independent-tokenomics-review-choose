# SIMD relaunch compensation review

Read the [final report](artifacts/report.md). It compares all seven poll choices, recommends an exact allocation and eligibility policy, models selling pressure, and provides a five-line community summary.

The five-stage record is preserved under `artifacts/`: the first analysis, its adversarial review, a separately written second analysis, its adversarial review, and the final verdict. The final verdict supersedes provisional proposals. Public numeric evidence and a source manifest are in [artifacts/evidence/](artifacts/evidence/).

Run the offline arithmetic and consistency check with Python 3 (standard library only):

```sh
python3 artifacts/model.py
```

The review checked Ethereum historical balances and incident transfers, not every allegation or deployed relaunch contract. The Robinhood loss ledger, actual opening IMD backing/range and final deployment inputs remain unverified. Scores are judgments; pool calculations are explicitly simplified stresses. This is a written recommendation, not a deployed contract, final beneficiary root, cash-refund promise or independent security certification. See [checks and limits](artifacts/checks.md).
