import numpy as np
import matplotlib.pyplot as plt
import laspy
from preprocess import filter_outliers, remove_outliers_zscore
from config import PROCESSED_LAS, FLOORPLAN_PNG

PROCESSED_LAS = PROCESSED_LAS
FLOORPLAN_PNG = FLOORPLAN_PNG

def load_las(file_path):
    """Loads a preprocessed .LAS file."""
    las = laspy.read(file_path)
    points = np.vstack((las.x, las.y, las.z)).T
    return points

def extract_2d_projection(points, slice_height=1.5, tolerance=0.1):
    """Extracts a horizontal 2D slice at a given height."""
    slice_points = points[(points[:, 2] >= slice_height - tolerance) & (points[:, 2] <= slice_height + tolerance)]
    print(f"[INFO] Extracted {len(slice_points)} points at height {slice_height}m ± {tolerance}m.")
    return slice_points

def plot_2d_projection(points_2d):
    """Plots a 2D top-down projection of the building."""
    plt.figure(figsize=(10, 10))
    plt.scatter(points_2d[:, 0], points_2d[:, 1], s=0.5, color="black")
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.title("2D Top-Down Projection")
    plt.show()

def save_2d_projection(points, save_path=FLOORPLAN_PNG):
    """Saves the 2D top-down projection as an image."""
    x, y = points[:, 0], points[:, 1]

    plt.figure(figsize=(10, 10))
    plt.scatter(x, y, s=1, color="black")
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.title("2D Top-Down Projection")
    plt.axis("equal")

    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"[INFO] 2D projection saved to: {save_path}")
    return np.column_stack((x, y))

if __name__ == "__main__":
    print("[INFO] Loading preprocessed .LAS file...")
    points = load_las(PROCESSED_LAS)

    print("[INFO] Extracting 2D projection...")
    points_2d = extract_2d_projection(points)
    points_2d = remove_outliers_zscore(points_2d, 2.0)
    points_2d = filter_outliers(points_2d, 80, 1.2)

    print("[INFO] Plotting 2D projection...")
    plot_2d_projection(points_2d)

    save_2d_projection(points_2d)
