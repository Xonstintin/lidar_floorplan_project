# config.py

# === Base Paths ===
BASE_DIR = ""
DATA_DIR = f"{BASE_DIR}/data"
OUTPUT_DIR = f"{BASE_DIR}/output"

# === File Paths ===
ORIGINAL_LAS = f"{DATA_DIR}/PointCloud.laz"
PROCESSED_LAS = f"{DATA_DIR}/ProcessedPointCloud.las"
PLAN_FOR_DOORS = f"{DATA_DIR}/plan_for_doors.png"
PLAN_FOR_WALLS = f"{DATA_DIR}/plan_for_walls.png"

DETECTED_DOORS_IMG = f"{OUTPUT_DIR}/detected_doors.png"
DETECTED_WALLS_IMG = f"{OUTPUT_DIR}/detected_walls_canny.png"
FLOORPLAN_DXF = f"{OUTPUT_DIR}/floorplan.dxf"
FLOORPLAN_PNG = f"{OUTPUT_DIR}/floorplan.png"
