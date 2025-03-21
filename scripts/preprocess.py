import os
import laspy
import numpy as np
import open3d as o3d
import hdbscan
from sklearn.decomposition import PCA
from scipy.spatial import ConvexHull
from matplotlib.path import Path
from config import ORIGINAL_LAS, PROCESSED_LAS 

LAS_FILE = ORIGINAL_LAS
PROCESSED_LAS = PROCESSED_LAS
os.environ["OMP_NUM_THREADS"] = "24"

def grid_subsampling(points, grid_size=0.1):
    """Reduces the number of points by uniform grid subsampling."""
    print(f"[INFO] Applying grid filtering with step {grid_size} m...")

    grid_coords = (points[:, :2] / grid_size).astype(int)
    _, unique_indices = np.unique(grid_coords, axis=0, return_index=True)

    subsampled_points = points[unique_indices]
    print(f"[INFO] Retained {len(subsampled_points)} out of {len(points)} points after filtering.")
    return subsampled_points

def load_las(file_path):
    """Loads a .LAS file and returns a point array."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    las = laspy.read(file_path)
    points = np.vstack((las.x, las.y, las.z)).T
    return points

def filter_outliers(points, neighbors, std_ratio):
    """Removes noise using Statistical Outlier Removal (SOR)."""
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=neighbors, std_ratio=std_ratio)
    filtered_points = np.asarray(cl.points)

    print(f"[INFO] Noise removed: {len(points) - len(filtered_points)} points deleted.")
    return filtered_points

def align_point_cloud(points):
    """Aligns the point cloud with PCA to remove tilt."""
    pca = PCA(n_components=2)
    pca.fit(points[:, :2])
    main_axis = pca.components_[0]
    angle = np.arctan2(main_axis[1], main_axis[0])

    rotation_matrix = np.array([
        [np.cos(-angle), -np.sin(-angle), 0],
        [np.sin(-angle),  np.cos(-angle), 0],
        [0, 0, 1]
    ])

    rotated_points = points @ rotation_matrix.T
    print(f"[INFO] Alignment complete. Correction angle: {np.degrees(angle):.2f} degrees.")
    return rotated_points

def crop_height(points, min_z=1.0, max_z=3.0):
    """Keeps only points within the specified height range."""
    filtered_points = points[(points[:, 2] >= min_z) & (points[:, 2] <= max_z)]
    print(f"[INFO] Retained {len(filtered_points)} points after height filtering.")
    return filtered_points

def remove_outliers_zscore(points, threshold=2):
    """Removes outliers using Z-score filtering."""
    mean_x, mean_y = np.mean(points[:, :2], axis=0)
    std_x, std_y = np.std(points[:, :2], axis=0)

    filtered_points = points[(np.abs(points[:, 0] - mean_x) < threshold * std_x) & 
                             (np.abs(points[:, 1] - mean_y) < threshold * std_y)]
    print(f"[INFO] Z-score filtering removed {len(points) - len(filtered_points)} points.")
    return filtered_points

def remove_outside_points(points):
    """Applies HDBSCAN to isolate building structure, then filters with Convex Hull."""
    print("[INFO] Running HDBSCAN to isolate building structure...")
    clustering = hdbscan.HDBSCAN(
        min_cluster_size=50,
        min_samples=20,
        core_dist_n_jobs=-1,
        memory=""
    ).fit(points[:, :2])

    labels = clustering.labels_
    unique, counts = np.unique(labels, return_counts=True)
    largest_cluster = unique[np.argmax(counts)]
    filtered_points = points[labels == largest_cluster]
    print(f"[INFO] {len(filtered_points)} points remain after HDBSCAN.")

    print("[INFO] Determining building boundary with Convex Hull...")
    xy_points = filtered_points[:, :2]
    hull = ConvexHull(xy_points)
    hull_vertices = xy_points[hull.vertices]
    hull_path = Path(hull_vertices)
    inside_mask = hull_path.contains_points(xy_points)
    final_points = filtered_points[inside_mask]

    print(f"[INFO] {len(final_points)} points remain after Convex Hull.")
    return final_points

def save_las(file_path, points):
    """Saves the point cloud to a .LAS file."""
    header = laspy.LasHeader(point_format=3, version="1.2")
    las = laspy.LasData(header)
    las.x = points[:, 0]
    las.y = points[:, 1]
    las.z = points[:, 2]
    las.write(file_path)
    print(f"[INFO] Processed LAS file saved: {file_path}")

def cut_walls(points):
    """Cuts off all points left of a given X threshold (e.g. external noise)."""
    x_cutoff = -11.0
    cut_points = points[points[:, 0] > x_cutoff]
    print(f"[INFO] Retained {len(cut_points)} points after X cutoff (removed {len(points) - len(cut_points)}).")
    return cut_points

if __name__ == "__main__":
    print("[INFO] Loading original .LAS file...")
    points = load_las(LAS_FILE)

    print("[INFO] Starting preprocessing...")
    points = filter_outliers(points, 40, 1.5)
    points = align_point_cloud(points)
    points = crop_height(points)
    points = cut_walls(points)
    points = remove_outliers_zscore(points)
    # points = grid_subsampling(points, grid_size=0.001)
    # points = remove_outside_points(points)

    print("[INFO] Saving processed LAS file...")
    save_las(PROCESSED_LAS, points)

    print("[INFO] Done! You can now use the preprocessed .LAS file.")