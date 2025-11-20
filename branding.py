import fitz  # PyMuPDF
import os
import io
from PIL import Image  # Requires: pip install Pillow

# --- Configuration ---
INPUT_FOLDER = "."
OUTPUT_FOLDER = "branded_output"
LEFT_LOGO = "DBG-logo.png"
RIGHT_LOGO = "DBM-logo.png"
WATERMARK_LOGO = "DBG-logo.png"

# Footer Configuration
FOOTER_TEXT_CENTER = "Shri Classes & DBG Gurukulam (by IITian Golu Sir)"
FOOTER_URL = "https://dbggurukulam.com"

# Files to process
TARGET_FILES = [
    "Maths Bodh Manthan II Class 1.pdf",
    "Maths Bodh Manthan II Class LKG  v1.0.pdf",
    "Maths Bodh Manthan II Class UKG v2.0.pdf"
]

def create_transparent_watermark(image_path, opacity=0.30):
    """
    Reads an image, reduces its opacity (Alpha channel) to the given percentage,
    and returns the image data in bytes.
    opacity=0.30 means 30% visibility (70% transparent).
    """
    if not os.path.exists(image_path):
        return None
        
    # Open image and ensure it has an Alpha channel (RGBA)
    img = Image.open(image_path).convert("RGBA")
    
    # Get the pixel data
    datas = img.getdata()
    
    new_data = []
    for item in datas:
        # item is a tuple (R, G, B, A)
        # We scale the existing Alpha (A) by the opacity factor
        # This ensures transparent backgrounds stay transparent!
        new_alpha = int(item[3] * opacity)
        new_data.append((item[0], item[1], item[2], new_alpha))
    
    # Update image data
    img.putdata(new_data)
    
    # Save to a byte buffer (memory) instead of a file
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    return img_buffer.getvalue()

def apply_branding(filename):
    input_path = os.path.join(INPUT_FOLDER, filename)
    
    if not os.path.exists(input_path):
        print(f"Skipping: {filename} (File not found)")
        return

    print(f"Processing: {filename}...")
    doc = fitz.open(input_path)

    # Create output directory
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Prepare the watermark image in memory (30% visible)
    watermark_data = create_transparent_watermark(WATERMARK_LOGO, opacity=0.25) # 0.25 is usually best for text readability

    for page_num, page in enumerate(doc):
        rect = page.rect
        
        # ---------------------------------------------------------
        # 1. ADD WATERMARK (Centered, 30% visibility)
        # ---------------------------------------------------------
        if watermark_data:
            wm_width = 300
            wm_height = 300
            wm_x = (rect.width - wm_width) / 2
            wm_y = (rect.height - wm_height) / 2
            wm_rect = fitz.Rect(wm_x, wm_y, wm_x + wm_width, wm_y + wm_height)

            # We use overlay=True so it sits "above" white backgrounds, 
            # but because we reduced opacity in the image itself, text is visible through it.
            page.insert_image(
                wm_rect,
                stream=watermark_data, # Use the in-memory transparent image
                keep_proportion=True,
                overlay=True 
            )

        # ---------------------------------------------------------
        # 2. ADD HEADER LOGOS (ALL PAGES)
        # ---------------------------------------------------------
        # Configuration for Header Logos
        logo_size = 65
        margin_top = 10
        margin_side = 20
        
        # Left Logo Rect
        left_rect = fitz.Rect(
            margin_side, 
            margin_top, 
            margin_side + logo_size, 
            margin_top + logo_size
        )
        
        # Right Logo Rect
        right_rect = fitz.Rect(
            rect.width - margin_side - logo_size, 
            margin_top, 
            rect.width - margin_side, 
            margin_top + logo_size
        )

        # Insert Left Logo (DBG)
        if os.path.exists(LEFT_LOGO):
            page.insert_image(left_rect, filename=LEFT_LOGO, keep_proportion=True, overlay=True)
        
        # Insert Right Logo (Mission)
        if os.path.exists(RIGHT_LOGO):
            page.insert_image(right_rect, filename=RIGHT_LOGO, keep_proportion=True, overlay=True)

        # ---------------------------------------------------------
        # 3. ADD FOOTER (ALL PAGES)
        # ---------------------------------------------------------
        footer_y = rect.height - 30
        
        # Draw line
        shape = page.new_shape()
        shape.draw_line((20, footer_y - 15), (rect.width - 20, footer_y - 15))
        shape.finish(color=(0, 0, 0), width=0.5)
        shape.commit()

        # Page Number
        page.insert_text((30, footer_y), f"Page {page_num + 1} of {len(doc)}", fontsize=9, fontname="helv", color=(0, 0, 0))

        # Center Text
        text_len = fitz.get_text_length(FOOTER_TEXT_CENTER, fontname="helv", fontsize=9)
        center_x = (rect.width - text_len) / 2
        page.insert_text((center_x, footer_y), FOOTER_TEXT_CENTER, fontsize=9, fontname="helv", color=(0, 0, 0))

        # URL
        url_len = fitz.get_text_length(FOOTER_URL, fontname="helv", fontsize=9)
        page.insert_text((rect.width - url_len - 30, footer_y), FOOTER_URL, fontsize=9, fontname="helv", color=(0, 0, 1))

    # Save
    output_filename = f"BRANDED_{filename}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    doc.save(output_path)
    print(f"Saved: {output_path}")
    print("-" * 30)

if __name__ == "__main__":
    print("Starting PDF Branding V2...")
    for pdf_file in TARGET_FILES:
        apply_branding(pdf_file)
    print("All done! Check the 'branded_output' folder.")