import argparse
from dataclasses import dataclass
from PIL import Image, ImageOps
from typing import List, Tuple

# Define the six cube colors in RGB
PALETTE = {
    'WHITE': (255, 255, 255),
    'YELLOW': (255, 255, 0),
    'RED': (255, 0, 0),
    'ORANGE': (255, 165, 0),
    'BLUE': (0, 0, 255),
    'GREEN': (0, 255, 0),
}

PALETTE_LIST = list(PALETTE.items())


def nearest_color(rgb: Tuple[int, int, int]) -> Tuple[str, Tuple[int, int, int]]:
    """Return the palette color name and value closest to the given RGB value."""
    r, g, b = rgb
    best_name, best_rgb = PALETTE_LIST[0]
    best_dist = (r - best_rgb[0]) ** 2 + (g - best_rgb[1]) ** 2 + (b - best_rgb[2]) ** 2
    for name, value in PALETTE_LIST[1:]:
        dist = (r - value[0]) ** 2 + (g - value[1]) ** 2 + (b - value[2]) ** 2
        if dist < best_dist:
            best_name, best_rgb, best_dist = name, value, dist
    return best_name, best_rgb


def quantize_image(img: Image.Image) -> Tuple[Image.Image, List[List[str]]]:
    """Quantize image to six cube colors.

    Returns the quantized image and a 2D array of color names for each pixel.
    """
    quantized = Image.new('RGB', img.size)
    color_names: List[List[str]] = []
    for y in range(img.height):
        row = []
        for x in range(img.width):
            name, value = nearest_color(img.getpixel((x, y)))
            quantized.putpixel((x, y), value)
            row.append(name)
        color_names.append(row)
    return quantized, color_names


def face_patterns(color_names: List[List[str]]) -> List[str]:
    """Return textual patterns for each 3x3 cube face."""
    height = len(color_names)
    width = len(color_names[0])
    patterns = []
    for face_y in range(0, height, 3):
        for face_x in range(0, width, 3):
            lines = []
            for dy in range(3):
                line = color_names[face_y + dy][face_x: face_x + 3]
                lines.append(' '.join(line))
            patterns.append((face_y // 3, face_x // 3, lines))
    output_lines = []
    for row, col, lines in patterns:
        output_lines.append(f"Face (row {row}, col {col}):")
        output_lines.extend(lines)
        output_lines.append('')
    return output_lines


def process_image(input_path: str, output_image: str, output_faces: str) -> None:
    img = Image.open(input_path)
    # Choose orientation based on original aspect ratio
    if img.width >= img.height:
        target_size = (90, 60)
    else:
        target_size = (60, 90)
    img = ImageOps.fit(img, target_size, Image.LANCZOS)
    quantized, color_names = quantize_image(img)
    quantized.save(output_image)

    patterns = face_patterns(color_names)
    with open(output_faces, 'w', encoding='utf-8') as f:
        f.write('\n'.join(patterns))


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Rubik's cube mosaic from an image.")
    parser.add_argument('image', help='Input image path')
    parser.add_argument('--output-image', default='mosaic.png', help='Path to save the quantized image')
    parser.add_argument('--output-faces', default='faces.txt', help='Path to save cube face patterns')
    args = parser.parse_args()
    process_image(args.image, args.output_image, args.output_faces)


if __name__ == '__main__':
    main()
