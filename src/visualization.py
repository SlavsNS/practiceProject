import numpy as np
import matplotlib.pyplot as plt

def visualize_system(positions):
    plt.figure(figsize=(8, 8))
    for planet_name, traj in positions.items():
        traj = np.array(traj)
        plt.plot(traj[:, 0], traj[:, 1], label=planet_name)

    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title('Planet Trajectories')
    plt.legend()
    plt.show()
