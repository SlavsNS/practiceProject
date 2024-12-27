import numpy as np
import logging
import json
import os

class Planet:
    def __init__(self, name, mass, position, velocity):
        """
        Initialize a planet.

        :param name: Name of the planet.
        :param mass: Mass (kg).
        :param position: Initial position [x, y] (m).
        :param velocity: Initial velocity [vx, vy] (m/s).
        """
        self.name = name
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)

    def to_dict(self):
        return {
            "name": self.name,
            "mass": self.mass,
            "position": self.position.tolist(),
            "velocity": self.velocity.tolist()
        }

    @staticmethod
    def from_dict(data):
        return Planet(
            data["name"],
            data["mass"],
            data["position"],
            data["velocity"]
        )

class PlanetarySystem:
    def __init__(self, G=6.67430e-11):
        """
        Initialize a planetary system.

        :param G: Gravitational constant.
        """
        self.planets = []
        self.G = G

    def add_planet(self, planet):
        self.planets.append(planet)
        logging.debug(f"Planet added: {planet.name}")

    def calculate_gravitational_force(self, p1, p2):
        distance_vector = p2.position - p1.position
        distance = np.linalg.norm(distance_vector)
        if distance == 0:
            raise ValueError(f"Planets {p1.name} and {p2.name} are at the same position.")
        force_magnitude = self.G * p1.mass * p2.mass / distance**2
        force_direction = distance_vector / distance
        return force_magnitude * force_direction

    def runge_kutta_step(self, planet, forces, time_step):
        acceleration = forces[planet.name] / planet.mass

        k1_v = acceleration * time_step
        k1_p = planet.velocity * time_step

        k2_v = acceleration * time_step
        k2_p = (planet.velocity + k1_v / 2) * time_step

        k3_v = acceleration * time_step
        k3_p = (planet.velocity + k2_v / 2) * time_step

        k4_v = acceleration * time_step
        k4_p = (planet.velocity + k3_v) * time_step

        planet.velocity += (k1_v + 2 * k2_v + 2 * k3_v + k4_v) / 6
        planet.position += (k1_p + 2 * k2_p + 2 * k3_p + k4_p) / 6

    def simulate(self, time_span, time_step):
        if not self.planets:
            raise ValueError("No planets to simulate.")

        num_steps = int(time_span / time_step)
        positions = {planet.name: [] for planet in self.planets}

        for _ in range(num_steps):
            forces = {planet.name: np.zeros(2) for planet in self.planets}

            for i, planet1 in enumerate(self.planets):
                for planet2 in self.planets[i + 1:]:
                    force = self.calculate_gravitational_force(planet1, planet2)
                    forces[planet1.name] += force
                    forces[planet2.name] -= force

            for planet in self.planets:
                self.runge_kutta_step(planet, forces, time_step)
                positions[planet.name].append(planet.position.copy())

        return positions

    def save_to_file(self, file_path):
        data = {
            "G": self.G,
            "planets": [planet.to_dict() for planet in self.planets]
        }
        with open(file_path, "w") as file:
            json.dump(data, file)
        logging.info(f"System saved to file {file_path}.")

    def load_from_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found.")
        with open(file_path, "r") as file:
            data = json.load(file)
        # Check if it's a list or an object
        if isinstance(data, list):
            self.planets = [Planet.from_dict(planet_data) for planet_data in data]
        elif isinstance(data, dict) and "planets" in data:
            self.planets = [Planet.from_dict(planet_data) for planet_data in data["planets"]]
            self.G = data.get("G", self.G)  # Load G if present
        else:
            raise ValueError("Invalid data format in file.")
        logging.info(f"System loaded from file {file_path}.")
