items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}

def greedy_algorithm(items: dict, budget: int) -> tuple[list[str], int, int]:
    """
    Greedy approach:
    Select items by highest calories-to-cost ratio.
    This method is fast but NOT guaranteed to be optimal.
    """
    # Sort items by calories/cost
    sorted_items = sorted(
        items.items(),
        key=lambda x: x[1]["calories"] / x[1]["cost"],
        reverse=True,
    )

    total_cost = 0
    total_calories = 0
    chosen = []

    for name, data in sorted_items:
        if total_cost + data["cost"] <= budget:
            chosen.append(name)
            total_cost += data["cost"]
            total_calories += data["calories"]

    return chosen, total_cost, total_calories

def dynamic_programming(items: dict, budget: int) -> tuple[list[str], int, int]:
    """
    Dynamic programming approach (0/1 Knapsack).
    Guarantees optimal solution.
    """
    names = list(items.keys())
    n = len(names)

    # dp[i][w] = max calories using first i items with budget w
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    # Build DP table
    for i in range(1, n + 1):
        cost = items[names[i - 1]]["cost"]
        calories = items[names[i - 1]]["calories"]

        for w in range(budget + 1):
            if cost <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - cost] + calories,
                )
            else:
                dp[i][w] = dp[i - 1][w]

    # Restore chosen items
    w = budget
    chosen = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(names[i - 1])
            w -= items[names[i - 1]]["cost"]

    chosen.reverse()

    total_cost = sum(items[name]["cost"] for name in chosen)
    total_calories = dp[n][budget]

    return chosen, total_cost, total_calories

if __name__ == "__main__":
    budget = 100

    greedy_result = greedy_algorithm(items, budget)
    dp_result = dynamic_programming(items, budget)

    print("Greedy algorithm result:")
    print(f"Items: {greedy_result[0]}")
    print(f"Total cost: {greedy_result[1]}")
    print(f"Total calories: {greedy_result[2]}")

    print("\nDynamic programming result:")
    print(f"Items: {dp_result[0]}")
    print(f"Total cost: {dp_result[1]}")
    print(f"Total calories: {dp_result[2]}")