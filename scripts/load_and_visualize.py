import laspy
import numpy as np
import open3d as o3d
import os
from config import PROCESSED_LAS

LAS_FILE = PROCESSED_LAS

def load_las(file_path):
    """Loads a .LAS file and returns an array of coordinates."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    las = laspy.read(file_path)
    points = np.vstack((las.x, las.y, las.z)).T
    return points

def visualize_point_cloud(points):
    """Visualizes the point cloud using Open3D."""
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    print("[INFO] Displaying point cloud...")
    o3d.visualization.draw_geometries([pcd])

if __name__ == "__main__":
    print("[INFO] Loading .LAS file...")
    points = load_las(LAS_FILE)

    print(f"[INFO] Loaded {points.shape[0]} points")

    visualize_point_cloud(points)  # 3D visualization
