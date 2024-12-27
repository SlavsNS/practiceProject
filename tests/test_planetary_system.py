import pytest
import numpy as np
from src.planetary_system import Planet, PlanetarySystem

@pytest.fixture
def setup_planetary_system():
    """Create an instance of PlanetarySystem and add planets for testing."""
    system = PlanetarySystem()
    earth = Planet("Earth", 5.972e24, [0, 0], [0, 0])
    moon = Planet("Moon", 7.348e22, [384400000, 0], [0, 1022])
    system.add_planet(earth)
    system.add_planet(moon)
    return system, earth, moon

def test_add_planet(setup_planetary_system):
    system, earth, moon = setup_planetary_system
    assert len(system.planets) == 2
    mars = Planet("Mars", 6.4171e23, [227940000000, 0], [0, 24077])
    system.add_planet(mars)
    assert len(system.planets) == 3

def test_calculate_gravitational_force(setup_planetary_system):
    system, earth, moon = setup_planetary_system
    force = system.calculate_gravitational_force(earth, moon)
    expected_force = system.G * earth.mass * moon.mass / np.linalg.norm(moon.position - earth.position)**2
    assert np.isclose(np.linalg.norm(force), expected_force)

def test_runge_kutta_step(setup_planetary_system):
    system, earth, moon = setup_planetary_system
    initial_position = earth.position.copy()

    # Calculate forces for both planets
    forces = {planet.name: np.zeros(2) for planet in system.planets}
    forces[earth.name] = system.calculate_gravitational_force(earth, moon)
    forces[moon.name] = -forces[earth.name]  # Force on the Moon is equal in magnitude but opposite in direction

    # Perform a Runge-Kutta step
    system.runge_kutta_step(earth, forces, 1)  # 1-second step

    # Check that the position has changed
    assert not np.array_equal(initial_position, earth.position)

def test_simulate(setup_planetary_system):
    system, earth, moon = setup_planetary_system
    positions = system.simulate(3600, 1)  # Simulate for 1 hour with a 1-second step
    assert earth.name in positions
    assert moon.name in positions
    assert len(positions[earth.name]) == 3600
    assert len(positions[moon.name]) == 3600

def test_zero_distance(setup_planetary_system):
    system, earth, _ = setup_planetary_system
    with pytest.raises(ValueError):
        system.calculate_gravitational_force(earth, earth)

def test_no_planets():
    """Check simulation with no planets."""
    empty_system = PlanetarySystem()
    with pytest.raises(ValueError):
        empty_system.simulate(3600, 1)
