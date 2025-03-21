import cv2
import numpy as np
import matplotlib.pyplot as plt
from config import DETECTED_DOORS_IMG, PLAN_FOR_DOORS

DETECTED_DOORS_IMG = DETECTED_DOORS_IMG
PLAN_FOR_DOORS = PLAN_FOR_DOORS

def detect_doors(image_path):
    """Detects door and window gaps using edge and line detection."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise FileNotFoundError(f"[ERROR] File not found: {image_path}")

    image = cv2.bitwise_not(image)

    _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

    # Canny Edge Detection
    edges = cv2.Canny(binary, 30, 100, apertureSize=3)

    # Hough Transform to detect lines
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=3, maxLineGap=10)

    min_door_length = 3
    max_door_length = 30

    doors = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if min_door_length <= length <= max_door_length:
                doors.append(line)

    return doors, edges

def draw_detected_doors(image_path, doors, edges, output_path=DETECTED_DOORS_IMG):
    """Draws detected doors and displays the result."""
    image = cv2.imread(image_path)

    # Plot edges
    plt.figure(figsize=(10, 10))
    plt.subplot(1, 2, 1)
    plt.imshow(edges, cmap="gray")
    plt.title("Edges (Canny)")

    # Plot detected doors
    plt.subplot(1, 2, 2)
    plt.imshow(image, cmap="gray")

    if doors:
        for line in doors:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green lines = doors

    plt.imshow(image)
    plt.title("Detected Doors")

    # Save and display
    cv2.imwrite(output_path, image)
    print(f"[INFO] Detected doors saved to: {output_path}")
    plt.show()

if __name__ == "__main__":
    image_path = PLAN_FOR_DOORS 
    print("[INFO] Detecting doors...")

    doors, edges = detect_doors(image_path)

    if doors:
        print(f"[INFO] Found {len(doors)} door(s).")
        draw_detected_doors(image_path, doors, edges)
    else:
        print("[WARNING] No doors detected.")
