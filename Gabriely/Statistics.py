import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from forest_fire_model import ForestFireModel  # Assuming base code remains unchanged

def run_phase_transition_experiment(grid_size, densities, iterations=30):
    """
    Run experiments to identify the phase transition in fire spread.

    Parameters:
        grid_size (int): Size of the grid (grid_size x grid_size).
        densities (list of float): Initial tree densities to test.
        iterations (int): Number of runs for each density value.

    Returns:
        pd.DataFrame: Results with density, spread fraction, and other statistics.
    """
    results = []

    for density in densities:
        spread_counts = 0
        burned_fractions = []

        for _ in range(iterations):
            # Initialize and run the model
            model = ForestFireModel(grid_size, grid_size, density)
            while model.running:
                model.step()

            # Get final burned fraction
            data = model.datacollector.get_model_vars_dataframe()
            burned_fraction = data["BurnedFraction"].iloc[-1]
            burned_fractions.append(burned_fraction)

            # Check if fire reached the opposite edge
            fire_reached_opposite = any(
                agent.condition == "On Fire" or agent.condition == "Burned Out"
                for (x, y), agent in model.grid.iter_cell_list_contents()
                if x == grid_size - 1  # Opposite edge
            )
            if fire_reached_opposite:
                spread_counts += 1

        # Aggregate results for this density
        spread_probability = spread_counts / iterations
        avg_burned_fraction = np.mean(burned_fractions)
        std_burned_fraction = np.std(burned_fractions)

        results.append({
            "Density": density,
            "SpreadProbability": spread_probability,
            "AvgBurnedFraction": avg_burned_fraction,
            "StdBurnedFraction": std_burned_fraction,
        })

    return pd.DataFrame(results)


def visualize_results(results, grid_size):
    """
    Visualize the phase transition and other statistics.

    Parameters:
        results (pd.DataFrame): Results from the experiment.
        grid_size (int): Size of the grid (used for labeling).
    """
    plt.figure(figsize=(12, 6))

    # Plot Spread Probability
    plt.subplot(1, 2, 1)
    plt.plot(results["Density"], results["SpreadProbability"], marker='o', label="Spread Probability")
    plt.axvline(
        results.loc[results["SpreadProbability"] >= 0.5, "Density"].iloc[0],
        color="red", linestyle="--", label="Phase Transition"
    )
    plt.title(f"Spread Probability vs Density (Grid: {grid_size}x{grid_size})")
    plt.xlabel("Tree Density")
    plt.ylabel("Spread Probability")
    plt.legend()

    # Plot Burned Fraction
    plt.subplot(1, 2, 2)
    plt.errorbar(
        results["Density"],
        results["AvgBurnedFraction"],
        yerr=results["StdBurnedFraction"],
        fmt="o", label="Avg Burned Fraction ± Std Dev"
    )
    plt.title(f"Burned Fraction vs Density (Grid: {grid_size}x{grid_size})")
    plt.xlabel("Tree Density")
    plt.ylabel("Burned Fraction")
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Parameters
    grid_size = 50  # Grid size (e.g., 50x50)
    densities = np.linspace(0.1, 0.9, 20)  # Densities to test
    iterations = 30  # Number of runs per density

    # Run experiments
    results = run_phase_transition_experiment(grid_size, densities, iterations)

    # Save results to a CSV file
    results.to_csv(f"forest_fire_phase_transition_{grid_size}x{grid_size}.csv", index=False)

    # Visualize results
    visualize_results(results, grid_size)
