import cv2
import ezdxf
from config import FLOORPLAN_DXF, DETECTED_WALLS_IMG

def load_image(image_path):
    """Loads the processed floorplan image with detected doors and walls."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"[ERROR] File not found: {image_path}")
    return image

def extract_edges(image):
    """Finds contours in the image using Canny edge detection."""
    edges = cv2.Canny(image, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def export_to_dxf(contours, output_path=FLOORPLAN_DXF):
    """Exports the floorplan as a DXF file (AutoCAD format)."""
    doc = ezdxf.new()
    msp = doc.modelspace()

    for contour in contours:
        points = [(pt[0][0], -pt[0][1]) for pt in contour]  # Invert Y-axis for CAD coordinate system
        if len(points) > 2:
            msp.add_lwpolyline(points, close=True)

    doc.saveas(output_path)
    print(f"[INFO] DXF file saved to: {output_path}")

if __name__ == "__main__":
    image_path = DETECTED_WALLS_IMG  # Final plan with doors and walls
    print("[INFO] Loading image...")

    image = load_image(image_path)
    contours = extract_edges(image)

    print("[INFO] Exporting to DXF...")
    export_to_dxf(contours)

    print("[✅] Done! Floorplan saved to 'C:/Users/Konstantin/Desktop/lidar_floorplan_project/output/floorplan.dxf'.")
