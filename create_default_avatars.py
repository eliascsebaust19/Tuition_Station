import sys
from PIL import Image, ImageDraw, ImageFont
import os

def create_default_avatar(name, output_path):
    """Create a default avatar with first letter of name"""
    # Professional color palette (Deep Plum + Gold theme)
    colors = [
        (30, 58, 138),   # Deep Blue
        (59, 130, 246),   # Medium Blue
        (139, 92, 246),   # Purple
        (245, 158, 11),    # Gold
        (16, 185, 129),    # Green
    ]
    
    # Select color based on name hash
    color_index = hash(name) % len(colors)
    bg_color = colors[color_index]
    
    # Create image
    size = 200
    img = Image.new('RGB', (size, size), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Get first letter
    letter = name[0].upper() if name else '?'
    
    # Try to use a nice font, fallback to default
    try:
        # Try to find a font
        font_paths = [
            "C:\\Windows\\Fonts\\Arial.ttf",
            "C:\\Windows\\Fonts\\arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc"
        ]
        font = None
        for fp in font_paths:
            if os.path.exists(fp):
                font = ImageFont.truetype(fp, 80)
                break
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Calculate text position (center)
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) / 2
    y = (size - text_height) / 2 - bbox[1]
    
    # Draw text
    draw.text((x, y), letter, fill='white', font=font)
    
    # Save
    img.save(output_path)
    print(f"Created default avatar for {name} at {output_path}")
    return output_path

if __name__ == '__main__':
    # Create default avatars for sample users
    output_dir = "E:\\Level 2 term II\\DBMS\\tuition_system\\static\\Assets\\Image"
    
    names = ['Ahmed', 'Sarah', 'Khan', 'Fatima', 'Abu', 'Rahim', 'Karim']
    
    for name in names:
        output_path = os.path.join(output_dir, f'default_{name.lower()}.png')
        create_default_avatar(name, output_path)
    
    print("\nAll default avatars created!")
