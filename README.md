# Cartoonify Image Project

A desktop image-cartoonizer built with Python, OpenCV, Pillow, and Tkinter.

## Run on Windows

1. Extract the ZIP file.
2. Make sure Python 3 is installed.
3. Double-click `RUN_PROJECT.bat`.
4. The first run installs the required Python packages automatically. An internet connection is needed for this first setup.
5. The app opens. Choose an image, click **Cartoonify**, then **Save Cartoon**.

## Run on macOS / Linux

Open a terminal in this folder and run:

```bash
chmod +x run.sh
./run.sh
```

## Features

- Upload PNG, JPG, JPEG, BMP, and WEBP images.
- Preview the original image.
- Convert the image into a cartoon effect using grayscale conversion, median blur, adaptive thresholding, bilateral filtering, and masking.
- Preview and save the cartoon result.

## Requirements

- Python 3
- `opencv-python`
- `Pillow`
- Tkinter (usually included with standard Python installations)

The first launch needs an internet connection to install the dependencies. After installation, the app can run locally.
