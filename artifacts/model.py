"""Offline arithmetic for the SIMD relaunch compensation report (standard library only).

Every number printed here is quoted in artifacts/report.md. The script asserts the
values the report relies on, so a wrong edit to either side fails loudly.

Assumptions (also stated in the report):
- New supply S = 1,000,000,000 (same as old supply; the brief does not give the new supply,
  but every result below is a percentage of supply, so the absolute value does not matter).
- The pool is a plain constant-product pool x*y=k holding P new tokens against some amount
  of IMD. A concentrated-liquidity (Uniswap v4 style) range could make impact either better
  or worse than this; no range or reserve data was supplied.
- Price impact of selling s tokens into a pool of P tokens: new_price/old_price = (P/(P+s))^2.
  This ratio does not depend on how much IMD is in the pool.
- Fees (2%) and arbitrage/new buys are ignored: this is a stress test, not a forecast.
"""

S = 1_000_000_000
SWARM = 0.10
OLD_HELD = 830_000_000          # brief: ~830M held outside the v4 pool at block 26213125
MIGRATED = 201_151_260          # notice + brief: SIMD sent to the migration wallet


def price_ratio(pool, sold):
    return (pool / (pool + sold)) ** 2


def pct(x):
    return f"{x * 100:.1f}%"


checks = []


def check(name, got, want, tol=0.0015):
    ok = abs(got - want) <= tol
    checks.append((name, ok))
    print(f"[{'ok' if ok else 'FAIL'}] {name}: {got:.4f} (report says {want})")


print("== Hard limits ==")
options = {
    # name: (compensation share, pool share, unlocked share of the airdrop within 72h)
    "1 migration-only 10%": (0.10, 0.80, 1.00),
    "2 1:1 snapshot 80%": (0.80, 0.10, 1.00),
    "3 split 20%": (0.20, 0.70, 1.00),
    "4 split 30% / 30d": (0.30, 0.60, 3 / 30),
    "5 = 4 + RH buyers": (0.30, 0.60, 3 / 30),
    "H recommended hybrid": (0.25, 0.65, None),
}
for name, (c, p, _) in options.items():
    assert abs(SWARM + c + p - 1) < 1e-9 and p >= 0.10 and c <= 0.80, name
    print(f"{name}: swarm 10% + comp {pct(c)} + pool {pct(p)} = 100%")

print("\n== Coverage in token units (new tokens per old token) ==")
check("opt2 coverage 800M/830M", 0.80 * S / OLD_HELD, 0.964)
check("opt1 coverage 100M/201.15M", 0.10 * S / MIGRATED, 0.497)
check("opt3 coverage 200M/830M", 0.20 * S / OLD_HELD, 0.241)
check("opt4 coverage 300M/830M", 0.30 * S / OLD_HELD, 0.361)
check("old supply in pool at snapshot", 1 - OLD_HELD / S, 0.17)

print("\n== 72h sell stress: share of each option's airdrop sold, price after (fraction of start) ==")
for name, (c, p, unlocked) in options.items():
    if unlocked is None:
        continue
    pool = p * S
    liquid = c * S * unlocked
    row = []
    for f in (0.25, 0.50, 1.00):
        row.append(f"{int(f*100)}% sold -> {pct(price_ratio(pool, liquid * f))}")
    print(f"{name}: liquid {liquid/1e6:.0f}M into {pool/1e6:.0f}M pool | " + " | ".join(row))

check("opt2 25% sold", price_ratio(0.10 * S, 0.80 * S * 0.25), 0.111)
check("opt2 50% sold", price_ratio(0.10 * S, 0.80 * S * 0.50), 0.040)
check("opt2 10% sold", price_ratio(0.10 * S, 0.80 * S * 0.10), 0.309)
check("opt3 50% sold", price_ratio(0.70 * S, 0.20 * S * 0.50), 0.766)
check("opt3 100% sold", price_ratio(0.70 * S, 0.20 * S), 0.605)
check("opt4 100% of unlocked sold", price_ratio(0.60 * S, 0.30 * S * 0.1), 0.907)
check("opt4 worst case: no vesting, 50% sold", price_ratio(0.60 * S, 0.15 * S), 0.640)
check("opt1 50% sold", price_ratio(0.80 * S, 0.05 * S), 0.886)

print("\n== Recommended hybrid H (25% compensation, 65% pool) ==")
A = 0.12 * S                      # tranche A: migration victims
B = 0.13 * S                      # tranche B: other snapshot holders
B_BASE = OLD_HELD - MIGRATED      # inference: migrators are inside the 830M snapshot
a72 = A * 0.25 + A * 0.75 * 3 / 30
b72 = B * 3 / 30
pool = 0.65 * S
check("H tranche A coverage 120M/201.15M", A / MIGRATED, 0.597)
check("H tranche B coverage 130M/628.8M", B / B_BASE, 0.207)
check("H unlocked by 72h (M tokens)", (a72 + b72) / 1e6, 52.0, tol=0.01)
check("H all unlocked sold", price_ratio(pool, a72 + b72), 0.857)
check("H half unlocked sold", price_ratio(pool, (a72 + b72) / 2), 0.925)

print("\n== Anti-sniper tax and option 7 fee math ==")
# Tax falls linearly 50% -> 0.75% over 30 min; average tax with buys spread evenly:
avg_tax = (0.50 + 0.0075) / 2
extra = avg_tax - 0.0075
check("average extra tax in window", extra, 0.246)
# Option 7: only the holders' 40% of the 0.75% hook fee could fund it -> 0.30% of volume.
share = 0.0075 * 0.40
check("vault holder share of volume", share, 0.003, tol=1e-9)
# 3.4 ETH is what the thief realised after slippage, not the holders' loss. Back out the ETH
# reserve y from proceeds = y*s/(P+s) with P = tokens in the pool at the snapshot (17% of supply),
# then value the dumped tokens at the pre-dump marginal price y/P.
P_OLD = S - OLD_HELD
proceeds = 3.4
y = proceeds * (P_OLD + MIGRATED) / MIGRATED
loss = MIGRATED * y / P_OLD
check("implied pool ETH reserve before dump", y, 6.27, tol=0.01)
check("pre-dump value of migrated SIMD (ETH)", loss, 7.42, tol=0.01)
check("volume (ETH) to repay pre-dump value", loss / share, 2474, tol=2)
check("volume (ETH) to repay 3.4 ETH lower bound", 3.4 / share, 1133.3, tol=0.5)
check("volume (ETH) to repay pre-dump value + 1.6 ETH IMD", (loss + 1.6) / share, 3008, tol=1)

print("\n== Tranche rules (worked examples from the report) ==")


def tranche_b_credit(bal_snap, bal_b2, sent_by_b2, credited_a):
    return max(0, min(bal_snap, bal_b2 + sent_by_b2) - credited_a)


# Partial migrator: 100 at snapshot, 40 migrated before B2, 60 held at B2 -> 60 (not 20).
check("B credit, partial migrator", tranche_b_credit(100, 60, 40, 40), 60, tol=0)
# Migrated after B2 (still inside window E): 100 held at B2, 40 sent later -> 60.
check("B credit, migrated after B2", tranche_b_credit(100, 100, 0, 40), 60, tol=0)
# Non-migrator who moved/sold after B2 keeps full credit (balance@B2 is pre-dump).
check("B credit, holder who moved after B2", tranche_b_credit(1_000_000, 1_000_000, 0, 0), 1_000_000, tol=0)
# Late sender (after block E) is not credited in A, so stays in B at the B rate.
late = 50_000_000
check("late sender gets B only (M tokens)", late * B / B_BASE / 1e6, 10.34, tol=0.01)
check("if late senders were admitted, A coverage would fall to", A / (MIGRATED + late), 0.478)

failed = [n for n, ok in checks if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
raise SystemExit(1 if failed else 0)
