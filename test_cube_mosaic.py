import os
from PIL import Image
from cube_mosaic import nearest_color, process_image, PALETTE


def test_nearest_color():
    name, rgb = nearest_color((250, 250, 240))
    assert name == 'WHITE'
    assert rgb == PALETTE['WHITE']


def test_process_image(tmp_path):
    # Create a simple image with mixed colors
    img = Image.new('RGB', (100, 50), (123, 20, 220))
    input_path = tmp_path / 'input.png'
    img.save(input_path)
    out_img = tmp_path / 'out.png'
    out_faces = tmp_path / 'faces.txt'
    process_image(str(input_path), str(out_img), str(out_faces))
    result = Image.open(out_img)
    assert result.size in [(90, 60), (60, 90)]
    # Ensure all pixels are in the palette
    palette_values = set(PALETTE.values())
    for pixel in result.getdata():
        assert pixel in palette_values
    assert out_faces.exists()
    with open(out_faces, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'Face (row 0, col 0):' in content
