import numpy as np

def compute_path_length(planned_path_file="planned_path.csv"):
    path = np.loadtxt(planned_path_file, delimiter=",", skiprows=1)

    if path.shape[0] < 2:
        return 0.0

    diff = np.diff(path, axis=0)

    distances = np.sqrt(diff[:,0]**2 + diff[:,1]**2)

    total_length = np.sum(distances)
    return total_length

if __name__ == "__main__":
    length = compute_path_length("goal2/planned_path.csv")
    print("Path length:", length)

