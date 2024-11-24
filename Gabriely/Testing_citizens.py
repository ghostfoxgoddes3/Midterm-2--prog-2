from model import ForestFire
from agent import Citizen, CityCell, TreeCell

def test_citizen_behavior():
    """
    Test that citizens:
    1. Evacuate from an evacuating city to the nearest safe city.
    2. Die if caught by fire during evacuation.
    """
    print("Starting Citizen Behavior Test...")

    # Initialize a small test model
    width, height = 10, 10
    density = 0.0  # No trees initially to focus on city and citizens
    model = ForestFire(width, height, density=density, city_probability=0.2)

    # Place a city and a citizen in one position
    city_pos = (2, 2)
    safe_city_pos = (7, 7)

    city = CityCell(city_pos, model)
    model.grid.place_agent(city, city_pos)
    model.schedule.add(city)

    citizen = Citizen(city_pos, model)
    model.grid.place_agent(citizen, city_pos)
    model.schedule.add(citizen)

    # Place a safe city in another position
    safe_city = CityCell(safe_city_pos, model)
    model.grid.place_agent(safe_city, safe_city_pos)
    model.schedule.add(safe_city)

    # Evacuate the initial city
    city.condition = "Evacuated"

    # Simulate one step to trigger evacuation
    model.step()
    assert citizen.target_city == safe_city_pos, "Citizen did not find the nearest safe city."
    assert citizen.pos != city_pos, "Citizen did not start moving away from the evacuating city."
    print("Citizen started evacuation correctly.")

    # Simulate multiple steps until the citizen reaches the safe city
    while citizen.target_city is not None:
        old_pos = citizen.pos
        model.step()
        assert citizen.pos != old_pos, "Citizen did not move toward the safe city."

    assert citizen.pos == safe_city_pos, "Citizen did not reach the safe city."
    print("Citizen successfully evacuated to the nearest safe city.")

    # Test death scenario: Set fire near the citizen's path
    fire_pos = (6, 6)
    burning_tree = TreeCell(fire_pos, model, prob_de_sobrevivencia=0.0)
    burning_tree.condition = "On Fire"
    model.grid.place_agent(burning_tree, fire_pos)
    model.schedule.add(burning_tree)

    # Move the citizen near the fire
    citizen.pos = (6, 5)
    model.step()

    assert not citizen.alive, "Citizen did not die when caught by fire."
    assert citizen.condition == "Dead", "Citizen condition is not updated to Dead."
    print("Citizen died correctly when caught by fire.")

    print("All Citizen Behavior Tests Passed!")

# Run the test
if __name__ == "__main__":
    test_citizen_behavior()
