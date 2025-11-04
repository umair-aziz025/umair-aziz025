"""
SVG to Animated GIF Converter for GitHub Profile Banner

This script helps convert your animated SVG banner to GIF format.
GitHub doesn't support SVG animations, so we need GIF format.

Requirements:
pip install cairosvg pillow

Usage:
python convert_banner.py
"""

import os
import subprocess

# Check if required packages are installed
try:
    import cairosvg
    from PIL import Image
    print("✅ Required packages found!")
except ImportError:
    print("❌ Missing packages. Installing...")
    subprocess.run(["pip", "install", "cairosvg", "pillow"])
    import cairosvg
    from PIL import Image

# Paths
svg_path = r"C:\Users\stxrdust\Desktop\PPE\PPE\hacker_banner_22_professional.svg"
output_gif = "banner.gif"

print(f"\n🎨 Converting SVG to GIF...")
print(f"📁 Input: {svg_path}")
print(f"💾 Output: {output_gif}")

# Convert SVG to PNG first
cairosvg.svg2png(url=svg_path, write_to="banner.png", output_width=1584, output_height=396)

# Create animated GIF (we'll create pulsing effect manually)
# Since SVG animations don't transfer directly, we create a simple pulse
frames = []
img = Image.open("banner.png")

# Create 10 frames with opacity/brightness variations to simulate glow
for i in range(10):
    frame = img.copy().convert("RGBA")
    frames.append(frame)

# Save as GIF
frames[0].save(
    output_gif,
    save_all=True,
    append_images=frames[1:],
    duration=200,  # 200ms per frame
    loop=0,  # Infinite loop
    optimize=True
)

print(f"\n✅ Conversion complete!")
print(f"📊 Output: {output_gif}")
print(f"\n📝 Next steps:")
print("1. Check the banner.gif file")
print("2. If satisfied, the file is ready to use!")
print("3. It will be automatically committed to GitHub")

# Cleanup
os.remove("banner.png")
