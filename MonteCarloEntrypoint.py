import random
import matplotlib.pyplot as plt

betsPerMin = 20
contribution_per_entry=0.1
dailyRateAverage = 15000
numberOfAccounts = 50

def simulate_full_stats(
    sims=20000,
    p_win=1/1_000_000,
    cost_per_entry=0.204, # $0.2 + RTP losses
    starting_pot=500_000,
    stop_loss=200_000,
    
    your_rate=numberOfAccounts*betsPerMin,
    others_rate=dailyRateAverage/24/60/contribution_per_entry/betsPerMin,
):
    total_rate = your_rate + others_rate
    your_share = your_rate / total_rate

    hit_prob_per_min = 1 - (1 - p_win) ** total_rate

    results = []

    for _ in range(sims):
        pot = starting_pot
        spent = 0

        while spent < stop_loss:
            spent += your_rate * cost_per_entry
            pot += total_rate * contribution_per_entry

            if random.random() < hit_prob_per_min:
                if random.random() < your_share:
                    results.append(pot - spent)   # win
                else:
                    results.append(-spent)       # lose
                break
        else:
            # stop-loss triggered
            results.append(-spent)

    total_runs = len(results)

    profits = [r for r in results if r > 0]
    losses = [r for r in results if r <= 0]

    # Core stats
    chance_profit = len(profits) / total_runs
    chance_loss = len(losses) / total_runs

    avg_profit_when_win = sum(profits) / len(profits) if profits else 0
    avg_loss_when_loss = sum(losses) / len(losses) if losses else 0

    overall_avg = sum(results) / total_runs
    max_loss = min(results)

    # Tail risk
    big_loss_threshold = -1_000_000
    big_losses = [r for r in results if r <= big_loss_threshold]
    prob_big_loss = len(big_losses) / total_runs

    return {
        "chance_profit": chance_profit,
        "chance_loss": chance_loss,
        "avg_profit_when_win": avg_profit_when_win,
        "avg_loss_when_loss": avg_loss_when_loss,
        "overall_avg_profit": overall_avg,
        "max_loss": max_loss,
        "prob_loss_>=_1M": prob_big_loss,
        "num_big_losses": len(big_losses),
        "total_sims": total_runs,
        "results": results,  # for further analysis if needed
    }


# Run simulation
stats = simulate_full_stats()

for k, v in stats.items():
    if k != "results":  # skip printing raw results
        print(f"{k}: {v}")
    
plt.hist(stats["results"], bins=50, edgecolor='black')
plt.show()
