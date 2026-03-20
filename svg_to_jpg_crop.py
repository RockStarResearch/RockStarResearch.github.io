import sys
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
import io

def convert_and_crop(input_svg, output_jpg, crop_amount=2):
    try:
        # 1. Convert SVG to a drawing object
        drawing = svg2rlg(input_svg)
        
        # 2. Render to a high-res PNG in memory
        # We scale it up so it stays crisp
        png_data = io.BytesIO()
        renderPM.drawToFile(drawing, png_data, fmt="PNG", dpi=300)
        png_data.seek(0)
        
        # 3. Open with Pillow and add white background
        img = Image.open(png_data).convert("RGBA")
        white_bg = Image.new("RGBA", img.size, "WHITE")
        img = Image.alpha_composite(white_bg, img).convert("RGB")

        # 4. Apply the 2px crop (approx 4% of the image)
        width, height = img.size
        shave = int(width * 0.04) 
        img = img.crop((shave, shave, width - shave, height - shave))

        # 5. Make it a perfect square with White Space
        w, h = img.size
        max_side = max(w, h)
        final_img = Image.new("RGB", (max_side, max_side), "WHITE")
        
        # Center the icon
        offset = ((max_side - w) // 2, (max_side - h) // 2)
        final_img.paste(img, offset)

        # 6. Save as JPG
        final_img.save(output_jpg, "JPEG", quality=95)
        print(f"Success! Created {output_jpg} without needing Cairo.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python svg_to_jpg_crop.py <input.svg> <output.jpg>")
    else:
        convert_and_crop(sys.argv[1], sys.argv[2])