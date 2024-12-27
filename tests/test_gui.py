import pytest
from tkinter import Tk
from src.gui import App
from src.planetary_system import PlanetarySystem, Planet

@pytest.fixture
def app():
    root = Tk()
    application = App(root)
    yield application
    root.quit()

def test_add_planet(app):
    app.name_entry.insert(0, "Earth")
    app.mass_entry.insert(0, "5.972e24")
    app.position_entry.insert(0, "1.5e11, 0")
    app.velocity_entry.insert(0, "0, 30000")
    app.add_planet()
    assert len(app.system.planets) == 1
    assert app.system.planets[0].name == "Earth"
    assert app.system.planets[0].mass == 5.972e24
    assert app.system.planets[0].position.tolist() == [1.5e11, 0]
    assert app.system.planets[0].velocity.tolist() == [0, 30000]

def test_add_planet_invalid_data(app):
    # Attempt to add a planet with invalid data
    app.name_entry.insert(0, "Earth")
    app.mass_entry.insert(0, "5.972e24")
    app.position_entry.insert(0, "1.5e11")
    app.velocity_entry.insert(0, "0, 30000")
    app.add_planet()
    assert len(app.system.planets) == 0  # Planet is not added due to invalid position

def test_run_simulation(app):
    planet = Planet("Earth", 5.972e24, [1.5e11, 0], [0, 30000])
    app.system.add_planet(planet)
    try:
        app.run_simulation()  # Check that simulation runs without errors
    except Exception as e:
        pytest.fail(f"Simulation failed with exception: {e}")

def test_run_simulation_empty_system(app):
    # Check that the simulation does not raise errors if no planets exist
    try:
        app.run_simulation()  # Simulation with an empty system
    except Exception as e:
        pytest.fail(f"Simulation failed with exception: {e}")

def test_simulate_trajectories():
    system = PlanetarySystem()
    earth = Planet("Earth", 5.972e24, [1.5e11, 0], [0, 30000])
    sun = Planet("Sun", 1.989e30, [0, 0], [0, 0])
    system.add_planet(earth)
    system.add_planet(sun)

    positions = system.simulate(3.154e7, 86400)  # Simulate 1 year with a 1-day step
    assert len(positions["Earth"]) > 0
    assert len(positions["Sun"]) > 0
