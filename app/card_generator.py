from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import random

# Try to import Urdu support libraries, fail gracefully if not found
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_URDU_SUPPORT = True
except ImportError:
    HAS_URDU_SUPPORT = False

def create_poetry_card(text, attribution="AI Poet"):
    """
    Creates a social-media ready image card with the given poetry text.
    """
    # 1. Canvas Setup
    width, height = 1080, 1080  # Square for Instagram/LinkedIn
    
    # Background: Dark gradient or solid dark color for premium look
    # We'll create a vertical gradient from deep blue/black to midnight purple
    image = Image.new("RGB", (width, height), "#0f0c29")
    draw = ImageDraw.Draw(image)
    
    # Simple Gradient Effect
    for y in range(height):
        r = int(15 + (y / height) * 45)   # 15 -> 60
        g = int(12 + (y / height) * 10)   # 12 -> 22
        b = int(41 + (y / height) * 60)   # 41 -> 101
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 2. Add Decorative Border (Gold)
    border_color = (212, 175, 55) # Gold
    border_width = 15
    draw.rectangle([border_width, border_width, width-border_width, height-border_width], outline=border_color, width=3)
    
    # 3. Add Text
    # Load Font
    font_path = "arial.ttf" # Fallback
    # Attempt to use a Nastaliq font if available in assets, else system default
    # For now we will use a default size
    font_size = 60
    
    try:
        # User should ideally provide 'NotoNastaliqUrdu-Regular.ttf' in app folder
        # We will check if it exists in 'app/assets' or root
        potential_fonts = ["app/assets/NotoNastaliqUrdu-Regular.ttf", "NotoNastaliqUrdu-Regular.ttf", "arial.ttf", "seguiemj.ttf"]
        found_font = False
        for p in potential_fonts:
            if os.path.exists(p):
                font = ImageFont.truetype(p, font_size)
                found_font = True
                break
        if not found_font:
             font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    # Process Urdu Text
    if HAS_URDU_SUPPORT:
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
    else:
        bidi_text = text # Will look broken for joined scripts but it's a fallback

    # Wrap Text (Manual wrapping for Urdu is tricky, we'll try a simple char count split)
    # Note: textwrap module works on characters, Urdu words vary in width. 
    # For a simple card, we'll try to split by space if the string is too long.
    
    lines = textwrap.wrap(bidi_text, width=40) # 40 chars width approx
    
    # Draw Lines Centered
    total_text_height = len(lines) * (font_size + 20)
    current_y = (height - total_text_height) // 2
    
    for line in lines:
        # Get text bounding box using getbbox()
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        x = (width - text_w) // 2
        
        # Draw Shadow
        draw.text((x+2, current_y+2), line, font=font, fill="black")
        # Draw Text
        draw.text((x, current_y), line, font=font, fill="white")
        
        current_y += font_size + 20

    # 4. Add Attribution
    attr_font_size = 30
    try:
        attr_font = ImageFont.truetype("arial.ttf", attr_font_size)
    except:
         attr_font = ImageFont.load_default()
         
    draw.text((width//2 - 50, height - 100), f"- {attribution}", font=attr_font, fill=border_color)

    return image
