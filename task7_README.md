# Task 7 — Monte Carlo method (two dice)

This task simulates rolling **two fair six-sided dice** many times, estimates the probability of each possible sum **2..12** using the **Monte Carlo** method, and compares those estimates to the **analytical (exact)** probabilities.

## What the program does

- Simulates a large number of rolls of **two dice**
- Counts how many times each sum (2..12) occurs
- Computes **Monte Carlo probabilities** `count / trials`
- Computes **analytical probabilities** (exact fractions out of 36)
- Prints a comparison table and draws a bar chart

---

## How to run

```bash
python task7_monte_carlo_dice.py
```

Optional arguments:

```bash
python task7_monte_carlo_dice.py --trials 500000 --seed 42 --plot
```

- `--trials` — number of simulated rolls (default: 100000)
- `--seed` — random seed for reproducibility (default: not set)
- `--plot` — show a matplotlib chart (optional)

---

## Expected analytical probabilities

There are **36** equally likely outcomes `(d1, d2)`.

| Sum | Ways | Analytical probability |
|---:|---:|---:|
| 2  | 1 | 1/36 ≈ 2.78% |
| 3  | 2 | 2/36 ≈ 5.56% |
| 4  | 3 | 3/36 ≈ 8.33% |
| 5  | 4 | 4/36 ≈ 11.11% |
| 6  | 5 | 5/36 ≈ 13.89% |
| 7  | 6 | 6/36 ≈ 16.67% |
| 8  | 5 | 5/36 ≈ 13.89% |
| 9  | 4 | 4/36 ≈ 11.11% |
| 10 | 3 | 3/36 ≈ 8.33% |
| 11 | 2 | 2/36 ≈ 5.56% |
| 12 | 1 | 1/36 ≈ 2.78% |

---

## Conclusions

- The Monte Carlo estimates approach the analytical probabilities as the number of trials increases.
- With small trial counts, results deviate more due to randomness.
- Increasing `--trials` reduces the error (law of large numbers).

Typical outcomes:
- At `10,000` trials the error is noticeable.
- At `100,000` trials the table becomes close to analytical values.
- At `1,000,000` trials the estimates are usually very close to exact probabilities.

---

## Files

- `task7_monte_carlo_dice.py` — simulation + comparison + plot
- `task7_README.md` — this explanation and conclusions
