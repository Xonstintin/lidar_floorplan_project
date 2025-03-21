# Floor Plan Generation from Point Cloud Data

## Overview
This project processes LiDAR point cloud data of a building and automatically generates a 2D floor plan. It consists of several steps: loading, preprocessing, projection, wall and door detection, and final DXF export. The approach prioritizes automation and generalizability over manual tuning or post-processing.

---

## Features
- LAS/LAZ point cloud loading using `laspy`
- Noise reduction with statistical filters
- PCA-based alignment
- Height slicing to extract architectural layers
- Contour and wall detection using Canny + Hough Transform
- Door detection via short-segment detection
- Export to DXF format (AutoCAD-compatible)

---

## Project Structure
- `preprocess.py` — loads and filters the original point cloud, applies alignment and height-based cropping.
- `extract_2d.py` — extracts and optionally saves a horizontal 2D slice.
- `load_and_visualize.py` — basic LAS loader and Open3D visualizer.
- `detect_features.py` — detects architectural features such as walls.
- `detect_doors.py` — attempts to find short gaps (doors/windows) using line detection.
- `export_dxf.py` — extracts contours from final floor plan and saves them to a DXF file.
- `config.py` — centralized file and directory path definitions.

---

## Approach & Challenges (written by the author)

> I approached this task with the concept of full automation and minimal manual tuning. However, tuning filtering parameters proved to be non-trivial due to the sheer volume and variety of points in the dataset.

> For example, I had to discard an external wall because statistically, it was indistinguishable in density or geometry from the internal building structure.

> I found that slicing the cloud closer to the ceiling produces cleaner contours but loses door data. Slicing lower keeps the doors but significantly increases noise. I chose not to manually clean these for consistency with my automation-first philosophy.

> Initially I suspected distorted building angles were due to slicing plane errors, but later realized that in Prague, 90° angles are far from guaranteed.

>Furniture and small objects can be removed by slicing closer to the ceiling or clustering for high-density structures.

### Thoughts
- Much of the noise could potentially be eliminated by restricting the sensor angle (e.g., clipping to 180°, shooting only inward), or by AI-driven classification of windows and ignoring points beyond them.
- A more advanced approach could include probabilistic modeling or strict contour extraction and point filtering *within* those boundaries.

### AI Ideas
I found a recent and very interesting model that does exactly this kind of structured layout extraction. It was released just days ago, so I didn’t have time to implement it — but I believe it may be of great interest to you:

👉 [SpatialLM — Large Language Model for 3D Scene Understanding](https://manycore-research.github.io/SpatialLM/)

---

## Output Example
- `floorplan.png`: top-down visual slice
- `detected_doors.png`: visualization of door candidates
- `detected_walls_canny.png`: detected building perimeter using Canny
- `floorplan.dxf`: exported 2D CAD drawing

---

## Requirements
- Python 3.10+
- Open3D
- laspy
- scikit-learn
- matplotlib
- OpenCV
- ezdxf

You can install dependencies using:
```bash
pip install -r requirements.txt
```

---

## Author
Prepared as part of a technical interview assignment.

Feel free to reach out for questions or clarifications!

