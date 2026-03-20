import sys
from PIL import Image, ImageOps
import io

# Note: This script requires 'cairosvg' and 'Pillow'
# pip install cairosvg Pillow

try:
    import cairosvg
except ImportError:
    print("Error: Please install cairosvg (pip install cairosvg) to convert SVGs.")
    sys.exit(1)

def convert_and_crop(input_svg, output_jpg, crop_amount=2):
    try:
        # 1. Convert SVG to PNG in memory (JPEGs don't support transparency)
        # We use a high scale to keep the icon crisp
        png_data = cairosvg.svg2png(url=input_svg, output_width=500, output_height=500)
        img = Image.open(io.BytesIO(png_data)).convert("RGBA")

        # 2. Add a white background (since SVGs are often transparent)
        white_bg = Image.new("RGBA", img.size, "WHITE")
        img = Image.alpha_composite(white_bg, img).convert("RGB")

        # 3. Apply the 2px crop (relative to our 500px scale, that's about 20px)
        # We'll calculate the exact percentage to match your '2px' feel
        width, height = img.size
        # Shaving ~4% roughly equals a 2px crop on a small icon
        border_shave = int(width * 0.04) 
        
        left = border_shave
        top = border_shave
        right = width - border_shave
        bottom = height - border_shave
        
        img = img.crop((left, top, right, bottom))

        # 4. Make it a perfect square using White Space Padding
        w, h = img.size
        max_side = max(w, h)
        final_img = Image.new("RGB", (max_side, max_side), "WHITE")
        
        # Paste the cropped image into the center of the white square
        offset = ((max_side - w) // 2, (max_side - h) // 2)
        final_img.paste(img, offset)

        # 5. Save as JPG
        final_img.save(output_jpg, "JPEG", quality=95)
        print(f"Success! {output_jpg} created as a border-free square.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python svg_to_jpg_crop.py <input.svg> <output.jpg>")
    else:
        convert_and_crop(sys.argv[1], sys.argv[2])