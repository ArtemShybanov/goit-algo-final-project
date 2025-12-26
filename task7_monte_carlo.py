import argparse
import random
from collections import Counter

import matplotlib.pyplot as plt


def simulate_two_dice(trials: int, seed: int | None = None) -> dict[int, float]:
    # Simulate rolling two fair dice "trials" times and estimate probabilities for sums 2..12
    if seed is not None:
        random.seed(seed)

    counts = Counter()

    for _ in range(trials):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        counts[d1 + d2] += 1

    probs = {s: counts[s] / trials for s in range(2, 13)}
    return probs


def analytical_probabilities() -> dict[int, float]:
    # Exact probabilities for sums of two fair dice (out of 36 equally likely outcomes)
    ways = {
        2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6,
        8: 5, 9: 4, 10: 3, 11: 2, 12: 1
    }
    return {s: ways[s] / 36 for s in range(2, 13)}


def print_comparison(mc: dict[int, float], an: dict[int, float]) -> None:
    # Print a comparison table: Monte Carlo vs Analytical
    print(f"{'Sum':>3} | {'Monte Carlo':>11} | {'Analytical':>10} | {'Abs error':>9}")
    print("-" * 44)
    for s in range(2, 13):
        mc_p = mc[s]
        an_p = an[s]
        err = abs(mc_p - an_p)
        print(f"{s:>3} | {mc_p:>11.5f} | {an_p:>10.5f} | {err:>9.5f}")


def plot_results(mc: dict[int, float], an: dict[int, float]) -> None:
    # Plot Monte Carlo and Analytical probabilities on the same chart
    sums = list(range(2, 13))
    mc_vals = [mc[s] for s in sums]
    an_vals = [an[s] for s in sums]

    x = range(len(sums))
    width = 0.4

    plt.figure(figsize=(10, 5))
    plt.bar([i - width / 2 for i in x], mc_vals, width=width, label="Monte Carlo")
    plt.bar([i + width / 2 for i in x], an_vals, width=width, label="Analytical")
    plt.xticks(list(x), sums)
    plt.xlabel("Sum (two dice)")
    plt.ylabel("Probability")
    plt.title("Two dice sum probabilities: Monte Carlo vs Analytical")
    plt.legend()
    plt.tight_layout()
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Monte Carlo simulation for sums of two dice.")
    parser.add_argument("--trials", type=int, default=100_000, help="Number of simulated rolls")
    parser.add_argument("--seed", type=int, default=None, help="Random seed (optional)")
    parser.add_argument("--plot", action="store_true", help="Show a matplotlib plot")
    args = parser.parse_args()

    mc = simulate_two_dice(trials=args.trials, seed=args.seed)
    an = analytical_probabilities()

    print(f"Trials: {args.trials}")
    if args.seed is not None:
        print(f"Seed: {args.seed}")
    print()

    print_comparison(mc, an)

    if args.plot:
        plot_results(mc, an)


if __name__ == "__main__":
    main()