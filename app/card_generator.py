from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# Try importing Urdu support
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_URDU_SUPPORT = True
except ImportError:
    HAS_URDU_SUPPORT = False

def create_poetry_card(text, attribution="AI Poet"):
    """
    Creates a vintage-style poetry card with a double border and dark textured background.
    """
    # 1. Canvas Setup
    width, height = 1080, 1080
    
    # Background: Solid Deep Charcoal (Almost Black)
    bg_color = (15, 15, 18) # #0F0F12
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Optional: Add subtle noise/texture simulation (Simple vignette via drawing)
    # We'll draw a radial gradient overlay (not fully supported natively in simple PIL drawing without heavy pixel ops, 
    # so we'll stick to a solid elegant background with frame).
    
    # 2. Frames (Double Border)
    # Colors
    gold_color = (197, 160, 89) # #C5A059
    dark_frame_color = (40, 40, 40)
    
    # Outer Border (Gold)
    margin = 40
    draw.rectangle([margin, margin, width-margin, height-margin], outline=gold_color, width=3)
    
    # Inner Border (Thin Gold)
    inner_margin = 60
    draw.rectangle([inner_margin, inner_margin, width-inner_margin, height-inner_margin], outline=gold_color, width=1)
    
    # Corner Accents (Simple Lines)
    corner_len = 50
    # Top Left
    draw.line([(margin, margin+corner_len), (margin+corner_len, margin+corner_len)], fill=gold_color, width=1)
    # (Simplified: Just the double border looks classy enough)

    # 3. Typography
    font_size = 72
    try:
        # Check standard paths
        potential_fonts = ["app/assets/NotoNastaliqUrdu-Regular.ttf", "NotoNastaliqUrdu-Regular.ttf", "arial.ttf"]
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
        bidi_text = text

    # Wrap Text: Estimate chars per line
    # For 1080px width and 72px font, approx 20-30 chars?
    wrapper = textwrap.TextWrapper(width=30)
    lines = wrapper.wrap(bidi_text)
    
    # Calculate Text Block Height
    line_height_pixels = font_size + 40
    total_text_height = len(lines) * line_height_pixels
    current_y = (height - total_text_height) // 2
    
    for line in lines:
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
        except:
             # Fallback for older PIL versions
             w, h = draw.textsize(line, font=font)
             bbox = (0, 0, w, h)
             
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) // 2
        
        # Subtle Drop Shadow
        draw.text((x+4, current_y+4), line, font=font, fill=(5, 5, 5))
        # Main Text (Cream/White)
        draw.text((x, current_y), line, font=font, fill=(240, 240, 240))
        
        current_y += line_height_pixels

    # 4. Attribution (Bottom Center, Serif Font if possible)
    try:
        attr_font = ImageFont.truetype("times.ttf", 40)
    except:
         attr_font = ImageFont.load_default()
         
    draw.text((width//2 - 50, height - 120), f"~ {attribution}", font=attr_font, fill=gold_color)

    return image
