import cv2
import matplotlib.pyplot as plt
from config import PLAN_FOR_WALLS, DETECTED_WALLS_IMG


def detect_walls_canny(image_path):
    """Detects walls using Canny edge detection and contours instead of Hough Transform."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise FileNotFoundError(f"[ERROR] File not found: {image_path}")

    image = cv2.bitwise_not(image)

    _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

    edges = cv2.Canny(binary, 50, 150, apertureSize=3)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_wall_length = 50  # Tune this value (higher means less noise)
    walls = [cnt for cnt in contours if cv2.arcLength(cnt, closed=True) > min_wall_length]

    return walls, edges

def draw_detected_walls(image_path, walls, edges, output_path=DETECTED_WALLS_IMG):
    """Draws detected walls and shows the result on screen."""
    image = cv2.imread(image_path)

    plt.figure(figsize=(10, 10))
    plt.subplot(1, 2, 1)
    plt.imshow(edges, cmap="gray")
    plt.title("Edges (Canny)")

    plt.subplot(1, 2, 2)
    plt.imshow(image)

    if walls:
        cv2.drawContours(image, walls, -1, (255, 0, 0), 2)  # Blue lines = walls

    plt.imshow(image)
    plt.title("Detected Walls (Canny)")

    # Save and show
    cv2.imwrite(output_path, image)
    print(f"[INFO] Detected walls saved to: {output_path}")
    plt.show()

if __name__ == "__main__":
    image_path = PLAN_FOR_WALLS
    print("[INFO] Detecting walls (Canny)...")

    walls, edges = detect_walls_canny(image_path)

    if walls:
        print(f"[INFO] Found {len(walls)} contours (walls).")
        draw_detected_walls(image_path, walls, edges)
    else:
        print("[WARNING] No walls detected.")
