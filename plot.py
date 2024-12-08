import numpy as np
import matplotlib.pyplot as plt

def plot_combined(prm_samples_file="prm_samples.csv",
                  prm_obstacles_file="prm_obstacles.csv",
                  planned_path_file="planned_path.csv",
                  prm_roadmap_file="prm_roadmap.csv",
                  robot_pose_file="robotPose.csv"):
    """
    Plots two subplots side-by-side:
    - Left subplot: PRM graph (samples, obstacles, edges) and the planned path
    - Right subplot: Planned path, robot's executed path, and obstacles

    Assumptions:
    - prm_samples.csv: has columns sample_x,sample_y
    - prm_obstacles.csv: has columns obs_x,obs_y
    - planned_path.csv: has columns x,y
    - prm_roadmap.csv: adjacency list of the PRM graph (node_index, neighbors...)
    - robotPose.csv: includes kf_x and kf_y columns for the robot's executed path
    """

    prm_samples = np.loadtxt(prm_samples_file, delimiter=",", skiprows=1)
    sample_x, sample_y = prm_samples[:,0], prm_samples[:,1]

    prm_obstacles = np.loadtxt(prm_obstacles_file, delimiter=",", skiprows=1)
    obs_x, obs_y = prm_obstacles[:,0], prm_obstacles[:,1]

    planned_path = np.loadtxt(planned_path_file, delimiter=",", skiprows=1)
    path_x, path_y = planned_path[:,0], planned_path[:,1]

    roadmap = []
    with open(prm_roadmap_file, 'r') as f:
        f.readline()  # skip header line
        for line in f:
            parts = line.strip().split(",")
            # first part is node_index, rest are neighbors
            if len(parts) > 1:
                neighbors = [int(x) for x in parts[1:] if x.strip() != '']
            else:
                neighbors = []
            roadmap.append(neighbors)

    with open(robot_pose_file, 'r') as f:
        header_line = f.readline().strip()
    headers = [h.strip() for h in header_line.split(",") if h.strip() != '']

    try:
        kf_x_index = headers.index("kf_x")
        kf_y_index = headers.index("kf_y")
    except ValueError:
        raise ValueError("kf_x or kf_y column not found in robotPose.csv")

    robot_data = np.genfromtxt(robot_pose_file, delimiter=",", skip_header=1,
                               usecols=(kf_x_index, kf_y_index), dtype=float)
    robot_x = robot_data[:, 0]
    robot_y = robot_data[:, 1]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    for i, neighbors in enumerate(roadmap):
        for ind in neighbors:
            ax1.plot([sample_x[i], sample_x[ind]], [sample_y[i], sample_y[ind]], "-c")
    ax1.plot(sample_x, sample_y, ".b", label="PRM Samples")
    ax1.plot(obs_x, obs_y, ".k", label="Obstacles")
    ax1.plot(path_x, path_y, "-r", label="Planned Path")
    ax1.scatter(path_x[0], path_y[0], c='g', marker='^', label='Start')
    ax1.scatter(path_x[-1], path_y[-1], c='m', marker='^', label='Goal')

    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_title('PRM Graph and Planned Path')
    ax1.grid(True)
    ax1.axis('equal')
    ax1.legend()

    # Right Subplot: Planned Path vs Robot Path with Obstacles
    ax2.plot(obs_x, obs_y, '.k', label='Obstacles')
    ax2.plot(path_x, path_y, '-r', label='Planned Path')
    ax2.scatter(path_x[0], path_y[0], c='g', marker='^', label='Start')
    ax2.scatter(path_x[-1], path_y[-1], c='m', marker='^', label='Goal')
    ax2.plot(robot_x, robot_y, '-b', label='Robot Path')

    ax2.set_xlabel('X (m)')
    ax2.set_ylabel('Y (m)')
    ax2.set_title('Planned Path vs Executed Robot Path with Map')
    ax2.grid(True)
    ax2.axis('equal')
    ax2.legend()

    plt.tight_layout()
    plt.show()

def plot_path_and_robot(robot_pose_file="robotPose.csv",
                        planned_path_file="planned_path.csv",
                        prm_obstacles_file="prm_obstacles.csv"):
    """
    Plots the planned path, the robot’s executed path, and the map (obstacles)
    on the same graph.
    Assumes:
    - robotPose.csv includes columns named 'kf_x' and 'kf_y' for the robot’s position
    - planned_path.csv has columns 'x,y' for the planned path waypoints
    - prm_obstacles.csv has columns 'obs_x,obs_y' for obstacle positions
    """

    planned_path = np.loadtxt(planned_path_file, delimiter=",", skiprows=1)
    path_x, path_y = planned_path[:,0], planned_path[:,1]

    with open(robot_pose_file, 'r') as f:
        header_line = f.readline().strip()
    headers = [h.strip() for h in header_line.split(",") if h.strip() != '']

    try:
        kf_x_index = headers.index("kf_x")
        kf_y_index = headers.index("kf_y")
    except ValueError:
        raise ValueError("kf_x or kf_y column not found in robotPose.csv")

    robot_data = np.genfromtxt(robot_pose_file, delimiter=",", skip_header=1,
                               usecols=(kf_x_index, kf_y_index), dtype=float)
    robot_x = robot_data[:, 0]
    robot_y = robot_data[:, 1]

    prm_obstacles = np.loadtxt(prm_obstacles_file, delimiter=",", skiprows=1)
    obs_x, obs_y = prm_obstacles[:,0], prm_obstacles[:,1]

    plt.figure()
    plt.plot(obs_x, obs_y, '.k', label='Obstacles')
    plt.plot(path_x, path_y, '-r', label='Planned Path')
    plt.scatter(path_x[0], path_y[0], c='g', marker='^', label='Start')
    plt.scatter(path_x[-1], path_y[-1], c='m', marker='^', label='Goal')
    plt.plot(robot_x, robot_y, '-b', label='Robot Path')

    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.title('Planned Path vs Executed Robot Path with Map')
    plt.grid(True)
    plt.axis('equal')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    # Example usage:
    # plot_combined(prm_samples_file="prm_samples.csv",
    #               prm_obstacles_file="prm_obstacles.csv",
    #               planned_path_file="planned_path.csv",
    #               prm_roadmap_file="prm_roadmap.csv",
    #               robot_pose_file="robotPose.csv")
    plot_path_and_robot()
