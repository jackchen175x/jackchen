# Cube Mosaic Generator

This repository contains a simple script to convert an input image into a Rubik's cube style mosaic.

## Features
- Resizes an image to 90×60 or 60×90 pixels depending on the original orientation.
- Reduces colors to the six Rubik's cube colors: white, yellow, red, orange, blue and green.
- Saves the quantized image and outputs the color pattern for each 3×3 cube face.

## Usage

```bash
python cube_mosaic.py path/to/image.jpg --output-image mosaic.png --output-faces faces.txt
```

The resulting `mosaic.png` is composed of the six cube colors. The file `faces.txt` lists the color layout of each 3×3 cube face using color names.

## Testing

Run the tests with:

```bash
pytest
```
