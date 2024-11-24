import numpy as np
from forest_fire_phase_transition import run_phase_transition_experiment

# Parameters for testing
density_values = np.linspace(0.57, 0.62, 6)  # Focused range near phase transition
grid_size = 50  # Moderate grid size
iterations = 10  # Reduced number of iterations for faster testing

# Run the experiment once to use in multiple tests
results = run_phase_transition_experiment(grid_size, density_values, iterations)

# Test 1: Spread probability increases across the range
def test_spread_probability():
    spread_probs = results["SpreadProbability"].values
    is_increasing = all(p2 >= p1 for p1, p2 in zip(spread_probs, spread_probs[1:]))
    print("Test Spread Probability Increasing:", "PASS" if is_increasing else "FAIL")
    if not is_increasing:
        print(f"Spread probabilities: {spread_probs}")

# Test 2: Burned fraction peaks near the transition
def test_burned_fraction_peak():
    burned_fractions = results["AvgBurnedFraction"].values
    peak_index = np.argmax(burned_fractions)
    is_peak_in_range = 0 < peak_index < len(burned_fractions) - 1
    print("Test Burned Fraction Peak:", "PASS" if is_peak_in_range else "FAIL")
    if not is_peak_in_range:
        print(f"Burned fractions: {burned_fractions}")

# Test 3: Results are consistent across repeated runs
def test_consistency():
    results_repeat = run_phase_transition_experiment(grid_size, density_values, iterations)
    spread_diff = np.abs(results["SpreadProbability"] - results_repeat["SpreadProbability"]).max()
    burned_diff = np.abs(results["AvgBurnedFraction"] - results_repeat["AvgBurnedFraction"]).max()
    is_consistent = spread_diff < 0.1 and burned_diff < 0.1
    print("Test Consistency Across Runs:", "PASS" if is_consistent else "FAIL")
    if not is_consistent:
        print(f"Spread difference: {spread_diff}, Burned difference: {burned_diff}")

# Test 4: Phase transition occurs in expected range
def test_phase_transition_location():
    transition_density = results.loc[results["SpreadProbability"] >= 0.5, "Density"].iloc[0]
    is_in_range = 0.57 <= transition_density <= 0.62
    print("Test Phase Transition Location:", "PASS" if is_in_range else "FAIL")
    if not is_in_range:
        print(f"Transition density: {transition_density}")

# Run all tests
if __name__ == "__main__":
    test_spread_probability()
    test_burned_fraction_peak()
    test_consistency()
    test_phase_transition_location()
