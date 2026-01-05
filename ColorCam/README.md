# ColorCam: Real-Time Color-Blindness Correction App

## Overview
ColorCam is a computer vision project designed to help people with color vision deficiencies (color blindness) see colors more accurately. The project applies real-time color correction filters to images and live camera feeds to enhance distinguishability of colors for users with Protanopia, Deuteranopia, and Tritanopia.
---

## Features
- Real-time color correction (and simulation) for different types of color blindness:
  - **Protanopia** (red deficiency)
  - **Deuteranopia** (green deficiency)
  - **Tritanopia** (blue deficiency)
- Python + OpenCV + NumPy implementation
- Prototype ready to be converted into a mobile app using Kivy

## How to Run
- Use terminal for running the files, if possible. For example:
  ```bash
  python src/webcam_kivy.py
  ```
---

## Installation
1. **Install Python 3** (macOS / Windows / Linux)
2. **Create virtual environment**:
```bash
python -m venv venv (python3 for macOS/Linux)
source venv/bin/activate
```
4. **Install dependencies**:
```bash
pip3 install opencv-python numpy
pip3 install kivy
```
---

## Explanation of Files
- color_corrector.py: contains functions for the daltonization (correction) algorithms.
- colorcam.kv: outline of the Kivy interface.
- main.py: the initial file to test the algorithms on images (present in images sub-folder)
- webcam.py: raw webcam for testing algorithms on camera feed. number keys 1-8 used as keyboard shortcuts ('q' to quit)
- webcam_kivy.py: main Kivy app with the webcam, different filters, and camera functionality.

---

## Explanation of Folders
- icons: contains camera icon for 'capture' button
- images: contains test images for daltonization algorithm
- src: contains source code
