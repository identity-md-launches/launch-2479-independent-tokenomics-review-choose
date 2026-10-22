# SIMD relaunch: which compensation plan? An independent tokenomics review

Written 2026-10-22. For SIMD/IMD holders; no technical background needed. Formulas are in boxes you can skip.

**How to read the labels**
- **[F] Fact:** stated in the brief, or on the team's public pages, saved in [evidence/](evidence/) ([notice](evidence/notice.txt), [migration page](evidence/migrate.txt)).
- **[C] Calculation:** reproduced by `python3 artifacts/model.py` (30 checks, all pass).
- **[I] Inference:** my reasoning from facts. It could be wrong.
- **[J] Judgment:** a score or opinion.
- **[?] Open question:** something this review could not confirm.

**What this review did not do:** I did not query Ethereum or Robinhood Chain myself. Holder counts, balances and the 201,151,260 figure come from the brief and the team's public notice, not from my own chain reads. See [checks.md](checks.md).

---

## 0. The facts everything depends on

| # | Fact | Source |
|---|---|---|
| F1 | Old supply 1,000,000,000 SIMD on Ethereum | brief |
| F2 | 201,151,260 SIMD was sent to migration wallet `0xE132be23CE6255930556a45406075E62fb6340C0` and all of it was sold on Oct 17 2026, 18:31–19:18 UTC, for about 3.4 ETH. The same wallet also sold 736 IMD (~1.6 ETH), took 2,331 IMD from the jobs vault, and sent 2,361 IMD to `0xf5C0…E3A4` | brief, [notice](evidence/notice.txt) |
| F3 | **Number of wallets: the brief and the notice's plan section say 62. The notice's on-chain section and the migration page say 63.** | [notice](evidence/notice.txt), [migrate](evidence/migrate.txt) |
| F4 | Snapshot at block 26213125: 614 holders, ~830M SIMD outside the pool (~83%) | brief |
| F5 | On the migration page, "credited" means what a wallet sent, **capped at its balance at the snapshot block 26213125** | [migrate](evidence/migrate.txt) |
| F6 | Hard limits: 10% to the swarm, pool at least 10%, so compensation is at most 80%. LP is locked forever | brief |
| F7 | Fees: 2% per trade. Of that, 0.75% goes to a vault (holders 40%, swarm 25.72%, dev 17.14%, marketing 17.14%) and 1.25% to the factory. Anti-sniper tax on buys falls from 50% to 0.75% over 30 min, and the extra goes to compensation | brief |
| F8 | The team's current published plan is option 1: 80% pool, 10% Compensation Vault, a Merkle root of the 62 wallets already published (`0xe842…6347`) | [notice](evidence/notice.txt) |
| F9 | The team publicly says the Robinhood "Super IMD" token (0x19E4…39F6) "is not supported by SIMD" | [migrate](evidence/migrate.txt) |
| F10 | The dev has no cash to refund, and we must not assume new money | brief |

**I1 (important).** F5 suggests the snapshot was taken *before* the migration transfers. If so, the ~830M snapshot balance already includes the 201M the 62/63 migrators sent. Options 3–5 ("migration wallets + snapshot holders") would then **count those people twice** unless the contract removes the duplicate. Everything below assumes the snapshot is pre-migration. **[?]** Confirm this by reading the balances at block 26213125.

**I2.** "Made whole" can be measured in two ways. In token units, old tokens get new tokens 1:1. In money, the 201M SIMD fetched only ~3.4 ETH when dumped (F2), but that is the thief's proceeds after slippage, not the holders' loss. Valued at the pre-dump price, under the constant-product model below with ~170M tokens in the pool (F4), the same tokens were worth about **7.4 ETH** [C]. No option can give back money in ETH, because there is no cash (F10). Every option pays in *new tokens*, and their value depends on the new price. So any plan that crashes the new price is not really compensation.

---

## Stage 1: First analyst, full analysis

### 1.1 Assumptions for the pool math
- The new supply is 1,000,000,000 tokens. The brief does not give it, but every result is a percentage of supply, so the exact number does not matter.
- The pool behaves like a plain constant-product pool (x·y = k). The Uniswap-v4-style factory may use concentrated ranges; without the actual range and reserve state, impact could be either better or worse than this simple model.
- Fees, arbitrage and new buyers are ignored. This is a stress test, not a forecast.

> **Price drop formula.** If someone sells *s* tokens into a pool that holds *P* tokens, the price afterwards is **(P / (P + s))²** times the starting price. The IMD side cancels out of this ratio.

### 1.2 72-hour sell-pressure model for options 2–5 (option 1 for comparison) [C]

"Liquid" means airdropped tokens that can be sold within 72h. The last three columns show the price after selling, as a share of the launch price.

| Option | Pool | Liquid by 72h | 25% of liquid sold | 50% sold | 100% sold |
|---|---|---|---|---|---|
| 1 (10%, 62 wallets) | 800M | 100M | 94.0% | 88.6% | 79.0% |
| **2 (80% 1:1)** | **100M** | **800M** | **11.1% (−89%)** | **4.0% (−96%)** | 1.2% |
| 3 (20%, unlocked) | 700M | 200M | 87.1% | 76.6% | 60.5% |
| 4 (30%, 30-day linear) | 600M | 30M (3/30 of 300M) | 97.5% | 95.2% | 90.7% |
| 5 (4 + Robinhood buyers) | 600M | 30M, split among more people | same as 4 | same as 4 | same as 4 |

Option 2 in plain terms: old holders own 8× more tokens than the pool. If even **10%** of the airdrop is sold, the price falls to **31%** of launch [C]. Lost holders would receive a token that is ~96% down within hours, and the last sellers would get almost nothing. On paper it is "1:1", but in value it is not.

### 1.3 Stage 1 scores (1 = bad, 10 = good) [J]

| Option | Fairness to losers | New buyers come | 72h sell pressure (10 = low) | Price/liquidity health | Trust rebuilt | Ease of verification | **Total /60** |
|---|---|---|---|---|---|---|---|
| 1 Migration only, 10% | 5 | 7 | 8 | 9 | 4 | 10 | **43** |
| 2 1:1, 80% | 7 | 1 | 1 | 1 | 6 | 7 | **23** |
| 3 Split 20% | 6 | 6 | 5 | 6 | 6 | 6 | **35** |
| 4 Split 30%, 30d | 7 | 6 | 8 | 7 | 7 | 6 | **41** |
| 5 = 4 + Robinhood buyers | 7 | 5 | 8 | 7 | 6 | 3 | **36** |
| 6 24h whitelist only | 1 | 4 | 9 | 8 | 1 | 7 | **30** |
| 7 Future fee airdrops | 3 | 7 | 10 | 9 | 2 | 6 | **37** |

### 1.4 Abuse vectors and the contract rule that blocks each one

| Vector | Options hit | Rule that blocks it |
|---|---|---|
| Buying the dead old token after the crash to farm the airdrop | 2–5 | Snapshot entitlement uses only balances at the fixed historical block 26213125, so buying now changes nothing there. **But a migration tranche keyed on transfers to 0xE132 is open to this:** anyone could send dead SIMD to 0xE132 today and be counted as a theft victim. Block it by counting only transfers mined up to block E, the thief's last sale (see §5.2). |
| Wallets that sold before the dump claim for tokens they no longer lost | 2–5 | `credit = min(balance@26213125, balance@B2)`, where B2 is the last block before the dump started (§5.2 gives the exact form for migrators). Selling or moving *after* B2 keeps the claim, because that holder already took the loss. Migration senders are credited what they sent (F5). |
| Sybil splitting | 2–5 | Pro-rata to a historical balance: splitting after the snapshot gives nothing, and splitting before it does not change the total. Do **not** add a per-wallet minimum payout or a per-wallet bonus, because those reward splitting. |
| Double counting migrators (I1) | 3–5 | Snapshot credit = `balance@26213125 − amountSentToMigrationWallet`, combined with the B2 rule exactly as in §5.2 so the migrated amount is removed once, not twice. The migrated amount is paid only from the migration tranche. |
| Pool, router, vault, attacker or team wallets included | 2–5 | Exclude the v4 pool manager, `0xE132…40C0`, `0xf5C0…E3A4`, vault and burn addresses, and any contract without a key, from the Merkle list. Publish the exclusion list. |
| Bots on the whitelist | 6 | Whitelist = snapshot addresses only, with a per-wallet buy cap proportional to the snapshot balance. EOA-only checks are not reliable, so rely on the list and the cap. |
| Snipers at launch | all | The existing anti-sniper tax (50% → 0.75% over 30 min). Keep it. |
| Fake Robinhood buyers (wash buys before the rug) | 5 | Count only buys before the rug block, net of sells, and cap each at its net ETH spent. **This depends on a rug ledger nobody has published [?].** |
| Recipient dumps at launch | 2, 3 | Linear vesting, with a claim contract that releases `total × elapsed / 30 days`. |

### 1.5 Stage 1 pick
Hybrid: **option 4 (30% over 30 days) with the migration victims ranked first**. Keep option 1's anti-sniper buyback for the 62 wallets.

---

## Stage 2: Adversarial review of stage 1

1. **Wrong-headcount risk.** Stage 1 repeats "62 wallets", but the team's own pages say 63 (F3). A Merkle root with one wallet missing is permanent. *Must fix: reconcile 62 vs 63 before any root is final.*
2. **Double counting was flagged but not costed.** Option 4's "30% over 830M" understates what migrators get *and* overstates what others get if migrators also receive a separate tranche. Stage 1 never gave per-group coverage numbers.
3. **The stress test does not describe the deployed liquidity curve.** A v4 position's range can change local depth in either direction; no position data was supplied. Stage 1's 6 for option 3's pool health is therefore only a judgment under the stated CPMM assumption, not a fact about the launch pool. Under the model, selling all of option 3's airdrop drops marginal price by about 39.5%.
4. **Bias toward the status quo.** Option 1 scored 10 for verification, partly because its Merkle root is already published. But that root is for a plan holders already distrust. "Easy to verify" is not the same as "trusted".
5. **Option 7 was dismissed without math.** Only the holders' 40% of 0.75% could fund it, so 0.30% of volume. The ~3.4 ETH realized from the dumped SIMD is a lower bound on the loss; at the pre-dump price the migrators' 201.15M was worth ~7.4 ETH (I2). Repaying that needs ~**2,474 ETH** of trading volume [C]; even the 3.4 ETH lower bound needs ~1,133 ETH. Adding the 1.6 ETH of IMD sold makes it ~3,008 ETH. Stated that way, option 7 is clearly a non-answer for a small token. Stage 1 still gave it 37, a higher total than option 3 or 5.
6. **The anti-sniper tax is oversold.** It averages ~24.6% extra tax over the window [C], but a 50% tax mostly *stops* buys, and the brief says buyers are the same community. Expect little revenue. Do not count it as compensation in any coverage figure.
7. **Missed risk:** recipients cannot sell if there is no buyer. With the IMD community as the main buyers (brief), new money may simply not come. Every sell-pressure number assumes nobody is buying.
8. **Missed risk:** the 30-day linear vest is short. By day 30 the full 30% is liquid against a 600M pool. Selling half of it (150M) still means a −36% drop [C].

---

## Stage 3: Second analyst, independent second opinion

I re-scored from scratch through two lenses and fixed stage 2's points: 63 vs 62 is unresolved, the duplicate is removed, option 7 is costed, and the tax is excluded from coverage.

**Coverage in token units for each group [C]** (assuming I1 is right: migrators' 201.15M is inside the 830M):
- Option 1: migrators get 100M for 201.15M, about **49.7%**. Others get **0%**.
- Option 2: everyone gets about **96.4%**, but the value collapses (see §1.2).
- Option 3: 200M over 830M, about **24.1%** each.
- Option 4: 300M over 830M, about **36.1%** each.

### 3.1 (a) A holder who LOST [J]
Their questions: *Do I get something back? Is it worth anything? Can the team change it?*

| Option | Gets back (token units) | Real value survives? | Trustworthy? | Score /10 |
|---|---|---|---|---|
| 1 | Migrators 50%, others 0 | yes | Merkle root already public | 3 (migrator 8, snapshot holder 1; weighted by tokens 2.7, by headcount 1.7) |
| 2 | 96% | no: −89% if a quarter is sold | yes | 3 |
| 3 | 24% | partly | yes | 5 |
| 4 | 36%, vested | mostly | yes | 7 |
| 5 | 36% minus a Robinhood dilution of unknown size | mostly | ledger unverifiable | 5 |
| 6 | 0, just a chance to buy | n/a | n/a | 1 |
| 7 | "Later", no date | unknown | promise only | 2 |

### 3.2 (b) A NEW buyer who never held SIMD [J]
Their questions: *How big is the overhang? How deep is the pool? Will I be exit liquidity?*

| Option | Overhang vs pool | Score /10 |
|---|---|---|
| 1 | 10% vs 80% | 9 |
| 2 | 80% vs 10%, so they are exit liquidity | 1 |
| 3 | 20% unlocked vs 70% | 5 |
| 4 | 30% vested vs 60% | 7 |
| 5 | same as 4, more recipients | 6 |
| 6 | no overhang, but no story either | 6 |
| 7 | none | 8 |

### 3.3 Where I disagree with stage 1
- **Option 1 is overrated (43, ranked first).** It gives *nothing* to the other ~550 snapshot holders. They held through a crash caused by the dump of migrated tokens. They are the IMD community the relaunch needs as buyers (brief). Its trust score should not be 4 with a total of 43: for most people it is "you get nothing".
- **Option 7 is overrated (37).** It needs ~2,474 ETH of volume to cover the ~7.4 ETH pre-dump value of the migrated tokens (Stage 2 #5).
- **Stage 1's hybrid misses the duplicate fix.** My version is below.

### 3.4 Stage 3 proposal
Two tranches, 25% in total: **A = 12% for migration victims, B = 13% for other snapshot holders net of migrated amounts**, with 60-day vesting. Pool 65%.

---

## Stage 4: Adversarial review of stage 3

1. **The 60-day vest hurts the most-wronged people.** The migrators were robbed outright and have waited already. A 60-day lock for them is a second penalty. *Fix: give tranche A a partial unlock at launch.*
2. **"Nothing for snapshot holders" is not purely the dev's fault.** Ordinary holders lost to a market crash. Migrators lost to theft. Treating them as equal claimants (option 3/4 style) is unfair to migrators. Stage 3 is right to rank migrators first, but it never justified 12/13.
   *Rationale added in the final verdict: migrators get about 3× the per-token coverage of others, because their loss was theft.*
3. **The new-buyer lens is generous to option 6.** A whitelist with no airdrop still leaves an 83%-of-supply community that is angry. That is a reputational overhang even with no token overhang.
4. **Dropping option 7 entirely is wasteful.** Post-vesting, part of the dev/marketing vault share could top up victims at no cost to buyers. *But* the brief says not to assume dev money, and dev/marketing are the dev's operating budget. Make it voluntary and say so; do not promise it.
5. **Unverified inputs.** Stage 3's 628.8M figure for tranche B relies on I1. If the snapshot is *post*-migration, the base is 830M and tranche B coverage drops to 15.7% (130M / 830M). *(Rejected in the final verdict, §5.4: this case is inconsistent with the stated facts.)*
6. **The Robinhood buyers are dismissed without a path.** They were also rugged. "Not our contract" (F9) is a fact, but they are the same community. They deserve at least an explicit answer, not silence.

---

## Stage 5: Final verdict

### 5.1 Final scores [J]
Each cell blends both analysts and both reviews. "Lost" is (a), "New" is (b).

| Option | Fairness to losers | New buyers come | 72h sell pressure (10 = low) | Price/liquidity health | Trust rebuilt | Verification | **Total /60** |
|---|---|---|---|---|---|---|---|
| 1 Migration only 10% | 3 | 8 | 8 | 9 | 3 | 9 | **40** |
| 2 1:1 80% | 4 | 1 | 1 | 1 | 4 | 7 | **18** |
| 3 Split 20% | 5 | 6 | 5 | 5 | 5 | 6 | **32** |
| 4 Split 30%, 30d | 6 | 6 | 8 | 7 | 7 | 6 | **40** |
| 5 = 4 + Robinhood buyers | 6 | 5 | 8 | 7 | 5 | 2 | **33** |
| 6 Whitelist only | 1 | 5 | 9 | 8 | 1 | 7 | **31** |
| 7 Future fee airdrops | 2 | 7 | 10 | 9 | 2 | 6 | **36** |
| **H Recommended hybrid** | **7** | **7** | **8** | **7** | **8** | **6** | **43** |

Option 2's fairness score is 4, not 7. Getting 96% of a token that is down ~90% is not fairness [C §1.2].

### 5.2 Recommended plan (hybrid H), ready to write into a contract

**Supply split (fits the hard limits) [C]:** Swarm **10%**, Pool **65%** (LP locked forever by the factory), Compensation **25%**.

**Tranche A, migration victims: 12% of supply (120,000,000 tokens)**
- Eligible: every wallet that sent SIMD to `0xE132be23CE6255930556a45406075E62fb6340C0` in a transfer mined **from the migration-open block up to and including block E**, where **E = the block of 0xE132's last SIMD sale (Oct 17 2026, 19:18 UTC per F2)**. Transfers after E are ignored: they were never sold by the thief, and the old token now trades near zero, so counting them would let any holder "upgrade" from tranche B to tranche A by sending dead SIMD today. Credit = amount sent in that window, capped at its balance at block 26213125 (the team's existing rule, F5).
- E is defined by an on-chain event, not a guess; the root-building script must look it up, print it, and publish it next to the root. **[?]** Its exact number was not read for this review.
- Sanity check written into the script: total tranche A credit must not exceed 201,151,260 (the amount the notice says was sold). If it does, the root is not published.
- Pro-rata on credited amount. Coverage is about **59.7%** in token units if the total credited is 201,151,260 [C].
- **25% unlocked at launch, 75% linear over 30 days.**
- Plus **100% of the anti-sniper tax buyback**, pushed pro-rata after the 30-minute window (this mechanism already exists in the published design, F8).
- Blocker: the 62/63 wallet count must be reconciled and the list republished before the root is frozen.

**Tranche B, other snapshot holders: 13% of supply (130,000,000 tokens)**
- **B2 = the last block before 0xE132's first SIMD sale (Oct 17 2026, just before 18:31 UTC, F2).** That is the moment the theft started hitting the price. Anyone still holding then took the loss, so selling at the crashed price, moving to a new wallet, or being drained *after* B2 does not reduce the claim.
- Effective holding = `min(balance@26213125, balance@B2 + sentToMigrationWalletBy@B2)`. Tranche B credit = `effective holding − creditedMigrationAmount`, floored at 0. Adding back what was already sent to 0xE132 by B2 makes sure migrated tokens are removed exactly once. Example: 100 at snapshot, 40 migrated, 60 still held at B2 → min(100, 60 + 40) − 40 = **60**.
- **Known cost of this rule (stated plainly):** a wallet whose SIMD left it between the snapshot block and B2 (sold, moved to another wallet of the same owner, or drained) gets credit only for what it still held at B2. Fix for self-moves: during the 48h challenge window, a holder may sign a message from both wallets proving the move; the script then credits the receiving wallet, still capped at the original snapshot balance. Pre-dump sales get nothing, because that holder did not suffer the dump.
- Excluded: Uniswap v4 pool/PoolManager, `0xE132…40C0`, `0xf5C0…E3A4`, vault and burn addresses, team wallets, and CEX/bridge contracts. Publish the list.
- Pro-rata. Coverage is about **20.7%** (130M / 628.85M) [C], and slightly higher after exclusions and the B2 rule shrink the base. The 15.7% alternative raised in Stage 4 #5 does not exist: the 830M "outside the pool" can only be a pre-dump figure, and in either pre-dump case the base is 830M − 201.15M (see §5.4).
- **Linear over 30 days from launch, no cliff.**

**For both tranches:**
- One Merkle root per tranche, immutable, built by a published script from public chain data so anyone can rebuild it.
- Claim-based (pull). Unclaimed tokens after **180 days** go to the holders' share of the SIMD vault, never to the team.
- No per-wallet minimums or bonuses, because they would reward sybil splitting.
- The vault may distribute anti-sniper buyback tokens to tranche A only from realized receipts after the 30-minute window. Base A+B grants total exactly 25% of supply. Buyback distributions are capped at a further 55% of supply, so total compensation distributions cannot exceed the 80% hard limit; amounts above that cap are burned. Buybacks must stop before the pool's token reserve drops below 10% of supply. The contract must not mint to satisfy a buyback promise, and the tax amount is not included in advertised coverage until collected.

**Robinhood "Super IMD" buyers:** no token allocation at launch. The ledger is unverified, and the team publicly disowned that contract (F9). Publish a clear written answer, and keep an open offer for a future vote *if* a verifiable pre-rug buy ledger is produced.

**Optional, no promise:** after day 30, the dev and marketing vault shares *may* voluntarily top up tranche A. Do not announce it as a commitment (F10).

**72h stress for H [C]:** about 52M tokens are claimable by 72h (A: 30M + 9M, B: 13M) against a 650M pool. If all of it is sold, the price falls to ~85.7% of launch. If half is sold, it falls to ~92.5%. At day 30, if half the full 250M is sold, the price falls to ~(650/775)² ≈ 70%. That is the real tail risk.

### 5.3 Top 3 risks and how to reduce them
1. **A wrong or unverifiable recipient list (62 vs 63, snapshot timing).** A frozen bad root is permanent.
   *Reduce:* publish the root-building script and CSV, give a 48h public challenge window before deploy, and reconcile the 63rd wallet explicitly. Publish blocks E and B2 with the root so nobody can be added by a late transfer.
2. **Buyers do not show up, so vested tokens are dumped into an empty book.**
   *Reduce:* no cliff (smooth flow instead of a single unlock day), a pool at 65% of supply, and launch messaging aimed at the existing IMD community. No longer-vest bonus: it could only be funded from unclaimed tokens, which are unknown until day 180, and it would break the fixed 25% cap and the no-bonus rule.
3. **Perceived unfairness: "only 21%" for snapshot holders and nothing for Robinhood buyers.** If this sours the crowd, it kills demand.
   *Reduce:* be explicit that 1:1 was modeled and would have dropped the price ~90%, show the math, and publish this report.

### 5.4 Where the analysts disagreed, and who was right
| Issue | Stage 1 | Stage 3 | Verdict |
|---|---|---|---|
| Is option 1 the best? | Ranked it first (43) | Rejected: it ignores ~550 holders | **Stage 3.** It is fine for buyers, but trust is the whole problem. |
| Option 7 | 37, credible | ~2,474 ETH of volume needed | **Stage 3 / review 2.** |
| Tranche B base (review 4 #5) | n/a | 628.85M | **Stage 3.** Review 4's 15.7% case cannot occur: 830M outside the pool plus the 201.15M dumped into it would exceed supply, so the snapshot is pre-dump, and pre-dump the 201.15M is either still in holders' wallets or in excluded 0xE132. Either way the base is 628.85M. |
| Double counting migrators | Flagged, not fixed | Fixed with two tranches | **Stage 3**, but the base is still unverified (review 4 #5). |
| Vesting length | 30d | 60d | **Neither as-is.** Review 4 was right: 25% unlocked for victims plus 30d linear. |
| Split between victims and holders | none | 12/13 | **Stage 3's numbers, with review 4's rationale** (theft weighs ~3× per token). |
| Robinhood buyers | Option 5 scored on par | Excluded | **Excluded for now, with a public path.** Review 4 #6 was right that silence is not OK. |

### 5.5 Five-line community summary
1. We can't refund cash and we won't pretend to. A 1:1 airdrop would leave the pool at 10% and crash the new token ~90% within hours, so "1:1" would be worth almost nothing.
2. Plan: 10% swarm, 65% locked pool, 25% compensation, all in the contract with no admin.
3. The wallets robbed in the migration get 12% of supply (~60% of what they sent, token for token). 25% unlocks at launch, the rest over 30 days, plus all anti-sniper tax.
4. Holders at snapshot block 26213125 who did not migrate share 13% (about 1 new token per 5 old), unlocking over 30 days. What counts is what you held when the dump started (Oct 17, 18:31 UTC): selling or moving after that keeps your claim. Buying old SIMD or sending it to the migration wallet now earns nothing.
5. Both recipient lists and the script that builds them are public for 48h before launch. Check your wallet and tell us if anything is wrong.

---

## Open questions [?]
- Is the snapshot block before or after the migration transfers? It does not change tranche B coverage (~20.7% either way, §5.4), but the root script must confirm it so migrators' credits match F5.
- The exact block numbers of E (0xE132's last SIMD sale) and B2 (just before its first sale). They are defined by on-chain events; this review did not read them.
- Was it 62 or 63 wallets?
- What is the new token supply, and how much IMD seeds the pool? (Percent impacts don't need them; dollar values do.)
- How many Robinhood rug buyers were there, and is there a ledger of their buys?
- Does the factory allow a 65/25 split, or only the 80/10 in the published design (F8)? If it is fixed at 80/10, H cannot be deployed without a factory change.

---

## Addendum (2026-10-22): fallback if the factory cannot do 65/25

**[?]** Whether the factory accepts a 65/25 split is unconfirmed. The team's published design is 80/10 (F8). If only that split is possible, keep the same rules and shrink the amounts [C, by hand: 60/201.15 and 40/628.85]:

| Item | Hybrid H (65/10/25) | Fallback (80/10/10) |
|---|---|---|
| Pool | 65% | 80% |
| Tranche A (migration victims) | 12% = 59.7% coverage | 6% = about 29.8% coverage |
| Tranche B (other holders) | 13% = about 20.7% coverage | 4% = about 6.4% coverage |
| Worst-case 72h price drop if all claimable tokens are sold | about 14% | smaller, but the compensation is also much smaller |

**[J]** The fallback is much weaker for holders. It does not fix the trust problem the brief describes ("won't buy again unless made whole"). If the team can only offer the fallback, say so plainly instead of calling it "compensation in full", and treat H as a request for a factory change.
