import fitz  # PyMuPDF
import os
import io
from PIL import Image  # Requires: pip install Pillow

try:
    import tkinter as tk
    from tkinter import filedialog
except ImportError:
    tk = None
    filedialog = None

# --- Configuration ---
LEFT_LOGO = "DBG-logo.png"
RIGHT_LOGO = "DBM-logo.png"
WATERMARK_LOGO = "DBG-logo.png"

# Footer Configuration
FOOTER_TEXT_CENTER = "Shri Classes & DBG Gurukulam (by IITian Golu Sir)"
FOOTER_URL = "https://dbggurukulam.com"

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

def apply_branding(input_path, output_filename, logos_all_pages=True):
    input_path = os.path.abspath(input_path)
    if not os.path.exists(input_path):
        print(f"Skipping: {input_path} (File not found)")
        return

    print(f"Processing: {input_path}...")
    doc = fitz.open(input_path)
    output_dir = os.path.dirname(input_path)
    output_path = os.path.join(output_dir, output_filename)

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
        margin_top = 40
        margin_side = 60
        
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

        apply_logos = logos_all_pages or page_num == 0
        if apply_logos:
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
    doc.save(output_path)
    print(f"Saved: {output_path}")
    print("-" * 30)

if __name__ == "__main__":
    print("Starting PDF Branding V2...")
    input_path = None
    if filedialog:
        print("Select the PDF to brand (a file picker window will open)...")
        root = tk.Tk()
        root.withdraw()
        input_path = filedialog.askopenfilename(
            title="Select PDF to brand",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        root.destroy()
        if not input_path:
            print("No file selected in dialog.")
    if not input_path:
        input_path = input("Enter the full path of the PDF to brand: ").strip()
    if not input_path:
        print("No input file provided. Exiting.")
    else:
        base_name = os.path.basename(input_path)
        default_output = f"DBG_{base_name}" if base_name else "DBG_BRANDED_output.pdf"
        output_name = input(f"Enter output filename (default: {default_output}): ").strip()
        output_filename = output_name or default_output
        if not output_filename.lower().endswith(".pdf"):
            output_filename += ".pdf"

        logo_preference = input(
            "Apply top logos on (A)ll pages or (F)irst page only? [A/F]: "
        ).strip().lower()
        logos_all_pages = logo_preference in ("a", "all", "y", "yes", "")

        apply_branding(input_path, output_filename, logos_all_pages)
        print("All done! Output saved next to the input file.")