# Planetary System Simulation

This project provides a graphical user interface (GUI) and backend to simulate planetary systems. The application enables users to create, save, load, and simulate the dynamics of multiple planets using the laws of gravity.

## Features

- Add Planets: Specify planet properties such as name, mass, position, and velocity.
- Simulate Motion: Visualize the trajectories of planets under gravitational influence using the Runge-Kutta method.
- Save and Load: Save planetary configurations to a JSON file and reload them for further use.
- Visualization: View and analyze planetary trajectories graphically.

## Installation

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### File Structure

project/
├── src/
│   ├── gui.py
│    ├── __init__.py
│   ├── planetary_system.py
│   ├── visualization.py
│   ├── logging_config.py
├── tests/
│    ├── __init__.py
│   ├── test_gui.py
│   ├── test_planetary_system.py
│   ├── test_visualization.py
├── resources/
│    ├── __init__.py
│   ├── config.json
│   ├── planets.json
│   ├── simulation_results.json
│   ├── test_system.json
├── logs.log
├── requirements.txt
├── README.md
└── main.py

## Usage

Run the main script to start the application:

python main.py

### GUI Usage

1. Enter the planet's name, mass, position (x, y), and velocity (vx, vy).
2. Click Add Planet to include the planet in the simulation.
3. Use Start Simulation to calculate and visualize planetary trajectories.
4. Use Save System to save the current configuration to a file.
5. Use Load System to reload a previously saved configuration.

### Logging

Logging is enabled by default. All logs are stored in `logs.log`.

## Testing

Run the test suite using pytest:

pytest

This project includes unit tests for the following:
- Adding planets
- Simulating planetary dynamics
- Validating visualization

## Examples

### Adding a Planet

from src.planetary_system import PlanetarySystem, Planet

system = PlanetarySystem()
earth = Planet("Earth", 5.972e24, [1.5e11, 0], [0, 30000])
system.add_planet(earth)

### Simulating a Year

positions = system.simulate(3.154e7, 86400)  # Simulate 1 year with daily steps

### Visualization

from src.visualization import visualize_system
visualize_system(positions)

## License

This project is licensed under the MIT License.

