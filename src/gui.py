import tkinter as tk
from tkinter import ttk
import logging
from src.planetary_system import PlanetarySystem, Planet
from src.visualization import visualize_system

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Planetary System Simulation")
        self.system = PlanetarySystem()

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Planet Name:").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(frame, width=20)
        self.name_entry.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(frame, text="Mass (kg):").grid(row=1, column=0, sticky=tk.W)
        self.mass_entry = ttk.Entry(frame, width=20)
        self.mass_entry.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(frame, text="Position (x, y):").grid(row=2, column=0, sticky=tk.W)
        self.position_entry = ttk.Entry(frame, width=20)
        self.position_entry.grid(row=2, column=1, sticky=tk.W)

        ttk.Label(frame, text="Velocity (vx, vy):").grid(row=3, column=0, sticky=tk.W)
        self.velocity_entry = ttk.Entry(frame, width=20)
        self.velocity_entry.grid(row=3, column=1, sticky=tk.W)

        ttk.Button(frame, text="Add Planet", command=self.add_planet).grid(row=4, column=0, columnspan=2, sticky=tk.W + tk.E)
        ttk.Button(frame, text="Start Simulation", command=self.run_simulation).grid(row=5, column=0, columnspan=2, sticky=tk.W + tk.E)
        ttk.Button(frame, text="Save System", command=self.save_system).grid(row=6, column=0, columnspan=2, sticky=tk.W + tk.E)
        ttk.Button(frame, text="Load System", command=self.load_system).grid(row=7, column=0, columnspan=2, sticky=tk.W + tk.E)

        # Space for error messages
        self.error_label = ttk.Label(frame, text="", foreground="red")
        self.error_label.grid(row=8, column=0, columnspan=2)

    def add_planet(self):
        try:
            name = self.name_entry.get()
            mass = float(self.mass_entry.get())
            position = list(map(float, self.position_entry.get().split(',')))
            velocity = list(map(float, self.velocity_entry.get().split(',')))

            if len(position) != 2 or len(velocity) != 2:
                raise ValueError("Position and velocity must contain two values (x, y).")
            if mass <= 0:
                raise ValueError("Mass must be positive.")

            self.system.add_planet(Planet(name, mass, position, velocity))
            self.name_entry.delete(0, tk.END)
            self.mass_entry.delete(0, tk.END)
            self.position_entry.delete(0, tk.END)
            self.velocity_entry.delete(0, tk.END)
            self.error_label.config(text="")
            logging.info(f"Planet {name} added to the system.")
        except ValueError as e:
            self.error_label.config(text=f"Input error: {e}")
            logging.error(f"Error adding planet: {e}")

    def run_simulation(self):
        try:
            positions = self.system.simulate(3.154e7, 86400)  # Simulate 1 year with 1-day steps
            visualize_system(positions)
            self.error_label.config(text="")  # Hide error after a successful simulation
            logging.info("Simulation completed successfully.")
        except Exception as e:
            self.error_label.config(text=f"Simulation error: {e}")  # Show error
            logging.error(f"Error during simulation: {e}")

    def save_system(self):
        try:
            file_path = "resources/config.json"
            self.system.save_to_file(file_path)
            self.error_label.config(text="System saved.")
            logging.info("System saved to file.")
        except Exception as e:
            self.error_label.config(text=f"Save error: {e}")
            logging.error(f"Error saving system: {e}")

    def load_system(self):
        try:
            file_path = "resources/planets.json"
            self.system.load_from_file(file_path)
            self.error_label.config(text="System loaded.")
            logging.info("System loaded from file.")
        except Exception as e:
            self.error_label.config(text=f"Load error: {e}")
            logging.error(f"Error loading system: {e}")
