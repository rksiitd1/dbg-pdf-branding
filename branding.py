import fitz  # PyMuPDF
import os

# --- Configuration ---
INPUT_FOLDER = "."  # Current directory
OUTPUT_FOLDER = "branded_output"
LEFT_LOGO = "DBG-logo.png"
RIGHT_LOGO = "DBM-logo.png"
# We will use the DBG logo as the watermark as well
WATERMARK_LOGO = "DBG-logo.png" 

# Footer Text Configuration
FOOTER_TEXT_CENTER = "Shri Classes & DBG Gurukulam (by IITian Golu Sir)"
FOOTER_URL = "https://dbggurukulam.com"

# List of files to process (excluding the Class 4 one which is already done)
TARGET_FILES = [
    "Maths Bodh Manthan II Class 1.pdf",
    "Maths Bodh Manthan II Class LKG  v1.0.pdf",
    "Maths Bodh Manthan II Class UKG v2.0.pdf"
]

def apply_branding(filename):
    input_path = os.path.join(INPUT_FOLDER, filename)
    
    # Check if file exists
    if not os.path.exists(input_path):
        print(f"Skipping: {filename} (File not found)")
        return

    print(f"Processing: {filename}...")
    doc = fitz.open(input_path)

    # Create output directory if not exists
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    for page_num, page in enumerate(doc):
        rect = page.rect  # Get page dimensions
        
        # ---------------------------------------------------------
        # 1. ADD WATERMARK (All Pages)
        # ---------------------------------------------------------
        # Calculate center for watermark
        wm_width = 300  # Size of watermark
        wm_height = 300
        wm_x = (rect.width - wm_width) / 2
        wm_y = (rect.height - wm_height) / 2
        
        wm_rect = fitz.Rect(wm_x, wm_y, wm_x + wm_width, wm_y + wm_height)
        
        # Insert image with low opacity (alpha)
        page.insert_image(
            wm_rect,
            filename=WATERMARK_LOGO,
            keep_proportion=True,
            overlay=False  # Put behind text
        )
        
        # We draw a semi-transparent white rectangle over the image 
        # to make it 'faded' since insert_image doesn't support direct opacity in older versions
        # BUT, PyMuPDF v1.18+ supports 'fill_opacity' in shapes. 
        # Let's use a simpler approach: Place the image, let text sit on top (overlay=False).
        # If it's too dark, we can draw a white box with 0.8 opacity over it.
        
        shape = page.new_shape()
        shape.draw_rect(wm_rect)
        shape.finish(color=None, fill=(1, 1, 1), fill_opacity=0.85) # White overlay to fade it
        shape.commit()

        # ---------------------------------------------------------
        # 2. ADD HEADER LOGOS (Page 1 Only)
        # ---------------------------------------------------------
        if page_num == 0:
            # Define sizes. We use slightly smaller logos (60x60) to fit tight spaces
            logo_size = 65 
            margin_top = 10
            margin_side = 20
            
            # Left Logo Coordinates (x1, y1, x2, y2)
            left_rect = fitz.Rect(
                margin_side, 
                margin_top, 
                margin_side + logo_size, 
                margin_top + logo_size
            )
            
            # Right Logo Coordinates
            right_rect = fitz.Rect(
                rect.width - margin_side - logo_size, 
                margin_top, 
                rect.width - margin_side, 
                margin_top + logo_size
            )

            # Insert Left Logo (DBG)
            if os.path.exists(LEFT_LOGO):
                page.insert_image(left_rect, filename=LEFT_LOGO, keep_proportion=True)
            
            # Insert Right Logo (Mission)
            if os.path.exists(RIGHT_LOGO):
                page.insert_image(right_rect, filename=RIGHT_LOGO, keep_proportion=True)

        # ---------------------------------------------------------
        # 3. ADD FOOTER (All Pages)
        # ---------------------------------------------------------
        footer_y = rect.height - 30 # 30 units from bottom
        
        # Draw a line separator
        shape = page.new_shape()
        shape.draw_line((20, footer_y - 15), (rect.width - 20, footer_y - 15))
        shape.finish(color=(0, 0, 0), width=0.5)
        shape.commit()

        # Page Number (Left)
        page.insert_text(
            (30, footer_y),
            f"Page {page_num + 1} of {len(doc)}",
            fontsize=9,
            fontname="helv",
            color=(0, 0, 0)
        )

        # Center Text (Shri Classes...)
        # We calculate text width to center it approximately
        text_len = fitz.get_text_length(FOOTER_TEXT_CENTER, fontname="helv", fontsize=9)
        center_x = (rect.width - text_len) / 2
        page.insert_text(
            (center_x, footer_y),
            FOOTER_TEXT_CENTER,
            fontsize=9,
            fontname="helv",
            color=(0, 0, 0)
        )

        # URL (Right)
        url_len = fitz.get_text_length(FOOTER_URL, fontname="helv", fontsize=9)
        page.insert_text(
            (rect.width - url_len - 30, footer_y),
            FOOTER_URL,
            fontsize=9,
            fontname="helv",
            color=(0, 0, 1) # Blue color
        )

    # Save the modified file
    output_filename = f"BRANDED_{filename}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    doc.save(output_path)
    print(f"Saved: {output_path}")
    print("-" * 30)

# --- Execution ---
if __name__ == "__main__":
    print("Starting PDF Branding...")
    for pdf_file in TARGET_FILES:
        apply_branding(pdf_file)
    print("All done! Check the 'branded_output' folder.")