import os
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

# --- CONFIGURATION ---
OUTPUT_FILENAME = "Class_1_Modern_Exam.pdf"
LOGO_LEFT = "DBG-logo.png"
LOGO_RIGHT = "DBM-logo.png"
WATERMARK_IMG = "DBG-logo.png"

# --- COLOR PALETTE (Modern & Fancy) ---
COLOR_PRIMARY = HexColor("#154c79")   # Deep Navy Blue
COLOR_ACCENT = HexColor("#e08d3c")    # Muted Gold/Orange
COLOR_BG_HEADER = HexColor("#f4f6f9") # Very Light Grey/Blue
COLOR_BORDER = HexColor("#d1d5db")    # Soft Grey
COLOR_TEXT = HexColor("#1f2937")      # Dark Charcoal (Not pitch black)

# --- FONT & TEXT FIXING ENGINE ---

FONT_NAME = "HindiFont"
FONT_BOLD = "HindiFontBold"

# A dictionary of words that commonly break in PDF generation and their specific unicode fixes.
# We use Zero Width Joiners (ZWJ) or specific sequences to force conjuncts.
HINDI_FIX_MAP = {
    "शब्दों": "शब्‍दों",  # Forced half-b
    "स्थान": "स्‍थान",   # Forced half-s
    "विस्तारित": "विस्‍तारित", # Forced half-s
    "चिन्ह": "चिन्‍ह",    # Forced half-n
    "उपस्थित": "उपस् थित", # Tweaked spacing
    "निम्न": "निम्‍न",    # Forced half-m
    "क्रम": "क्रम",
    "सप्ताह": "सप्‍ताह",   # Forced half-p
    "नमस्ते": "नमस्‍ते",
    "बच्चे": "बच्‍चे",
    "स्कूल": "स्‍कूल",
    "श्याम": "श्‍याम",
    "उत्तर": "उत्‍तर",
    "रुपये": "रुपये"
}

def fix_text(text):
    """
    Applies specific Dictionary Fixes and Matra Reordering for correct Hindi rendering
    without a complex shaping engine.
    """
    if not text: return ""
    
    # 1. Dictionary Replacement for broken conjuncts
    for bad, good in HINDI_FIX_MAP.items():
        if bad in text:
            text = text.replace(bad, good)
            
    # 2. Matra 'i' (Chhoti Ee) Reordering
    # Moves the matra before the consonant (Visual reordering)
    def swap_matra(match):
        return "\u093f" + match.group(1)
    
    # Regex finds (Consonant + Halant + Consonant) OR (Consonant) followed by Matra I
    # This is a simplified reorderer.
    text = re.sub(r'([^\s\u093f])\u093f', swap_matra, text)
    
    return text

def setup_fonts():
    """
    Loads the best available Windows font. 
    Mangal is usually best for conjuncts on Windows.
    """
    font_paths = [
        "C:\\Windows\\Fonts\\mangal.ttf",      # Priority 1: Mangal (Good Shaping)
        "C:\\Windows\\Fonts\\mangal.ttc",      
        "C:\\Windows\\Fonts\\Nirmala.ttf",     # Priority 2: Nirmala
        "C:\\Windows\\Fonts\\arialuni.ttf",    # Priority 3: Arial Unicode
    ]
    
    found = False
    for path in font_paths:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont(FONT_NAME, path))
                # We register the same font as "Bold" because real bold might not exist
                # We will handle bolding by text stroke in the canvas if needed
                pdfmetrics.registerFont(TTFont(FONT_BOLD, path)) 
                print(f"Loaded Font: {path}")
                found = True
                break
            except:
                continue
    
    if not found:
        print("Warning: No Hindi font found. Using default.")

# --- DRAWING PRIMITIVES (The "Fancy" Stuff) ---

def draw_modern_header(c, width, height, page_num):
    c.saveState()
    
    # 1. Background Header Strip
    header_height = 110
    c.setFillColor(COLOR_BG_HEADER)
    c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
    
    # 2. Bottom Line of Header
    c.setStrokeColor(COLOR_PRIMARY)
    c.setLineWidth(3)
    c.line(0, height - header_height, width, height - header_height)
    
    # 3. Logos
    logo_size = 75
    margin_x = 25
    logo_y = height - 95
    
    if os.path.exists(LOGO_LEFT):
        c.drawImage(LOGO_LEFT, margin_x, logo_y, width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)
    if os.path.exists(LOGO_RIGHT):
        c.drawImage(LOGO_RIGHT, width - margin_x - logo_size, logo_y, width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)

    # 4. Center Text
    c.setFillColor(COLOR_PRIMARY)
    c.setFont(FONT_NAME, 26)
    c.drawCentredString(width/2, height - 50, "DBG GURUKULAM")
    
    # 5. Sub Header
    if page_num == 1:
        c.setFont(FONT_NAME, 12)
        c.setFillColor(COLOR_TEXT)
        sub_text = fix_text("कक्षा : 1 (First)   |   विषय: गणित (Maths)   |   समय: 2 घंटे")
        c.drawCentredString(width/2, height - 75, sub_text)
        
        # Student Details Strip
        strip_y = height - 145
        c.setStrokeColor(COLOR_BORDER)
        c.setLineWidth(1)
        c.roundRect(20, strip_y, width - 40, 30, 5, stroke=1, fill=0)
        
        c.setFont(FONT_NAME, 10)
        c.setFillColor(colors.black)
        details = fix_text("नाम: ___________________________   रोल नं: _________   दिनांक: _________")
        c.drawString(35, strip_y + 10, details)
        
        # Marks Strip
        marks_y = strip_y - 25
        c.setFont(FONT_NAME, 10)
        c.setFillColor(COLOR_PRIMARY)
        c.drawString(20, marks_y, "Total Questions: 16")
        c.drawRightString(width - 20, marks_y, fix_text("पूर्णांक (Max Marks): 80"))
        
        return marks_y - 15 # Return Cursor Y
    else:
        c.setFont(FONT_NAME, 12)
        c.setFillColor(COLOR_TEXT)
        c.drawCentredString(width/2, height - 75, fix_text("गणित - भाग 2 (Page 2)"))
        return height - 120

    c.restoreState()

def draw_card(c, x, y, w, h, title, marks, accent_color=COLOR_PRIMARY):
    """
    Draws a modern card with a shadow, rounded corners, and a colored title bar.
    """
    c.saveState()
    radius = 8
    shadow_offset = 3
    
    # 1. Shadow (Grey Offset)
    c.setFillColor(colors.Color(0.9, 0.9, 0.9))
    c.roundRect(x + shadow_offset, y - shadow_offset, w, h, radius, fill=1, stroke=0)
    
    # 2. Main Box (White)
    c.setFillColor(colors.white)
    c.setStrokeColor(COLOR_BORDER)
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    
    # 3. Title Bar (Clip to top rounded corners)
    header_h = 24
    
    # Clip path for header
    p = c.beginPath()
    p.roundRect(x, y, w, h, radius)
    c.clipPath(p, stroke=0)
    
    # Draw Header Background
    c.setFillColor(accent_color) # Use Accent Color
    c.rect(x, y + h - header_h, w, header_h, fill=1, stroke=0)
    
    # Draw Text in Header
    c.setFillColor(colors.white) # White text on color
    c.setFont(FONT_NAME, 10)
    c.drawString(x + 10, y + h - 16, fix_text(title))
    c.drawRightString(x + w - 10, y + h - 16, fix_text(marks))
    
    c.restoreState()

def draw_watermark(c, width, height):
    if os.path.exists(WATERMARK_IMG):
        c.saveState()
        c.setFillAlpha(0.08) # Very subtle
        wm_size = 450
        c.translate(width/2, height/2)
        c.rotate(0) # Can rotate 45 if desired
        c.drawImage(WATERMARK_IMG, -wm_size/2, -wm_size/2, 
                    width=wm_size, height=wm_size, mask='auto', preserveAspectRatio=True)
        c.restoreState()

def draw_math_vertical(c, x, y, num1, op, num2):
    """Draws a vertical math problem aligned to the right"""
    c.saveState()
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 14)
    
    # Align Numbers Right
    # Assuming monospaced-ish width or fixed alignment
    c.drawRightString(x + 40, y, num1)
    c.drawRightString(x + 40, y - 18, num2)
    
    # Operator
    c.drawString(x - 5, y - 18, op)
    
    # Line
    c.setLineWidth(1.5)
    c.setStrokeColor(colors.black)
    c.line(x - 5, y - 24, x + 45, y - 24)
    c.restoreState()

def draw_footer_modern(c, width, page_num):
    c.saveState()
    footer_y = 20
    
    # Decorative Line
    c.setStrokeColor(COLOR_ACCENT)
    c.setLineWidth(2)
    c.line(0, footer_y + 15, width, footer_y + 15)
    
    # Page Number Circle
    c.setFillColor(COLOR_PRIMARY)
    c.circle(30, footer_y + 6, 12, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(FONT_NAME, 9)
    c.drawCentredString(30, footer_y + 3, str(page_num))
    
    # Text
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 9)
    c.drawCentredString(width/2, footer_y + 3, "Shri Classes & DBG Gurukulam (by IITian Golu Sir)")
    
    # Link
    c.setFillColor(COLOR_PRIMARY)
    c.drawRightString(width - 20, footer_y + 3, "https://dbggurukulam.com")
    c.restoreState()

# --- MAIN GENERATION LOGIC ---

def create_modern_paper():
    setup_fonts()
    c = canvas.Canvas(OUTPUT_FILENAME, pagesize=A4)
    width, height = A4
    
    # ================= PAGE 1 =================
    draw_watermark(c, width, height)
    cursor_y = draw_modern_header(c, width, height, 1)
    
    # Constants
    MARGIN = 20
    GAP = 15
    col_width = (width - (3 * MARGIN)) / 2
    
    col1 = MARGIN
    col2 = MARGIN + col_width + MARGIN
    
    # Q1 & Q2
    h_row1 = 120
    draw_card(c, col1, cursor_y - h_row1, col_width, h_row1, "प्र. 1: शब्दों में लिखें (Words)", "[5 अंक]")
    c.setFont(FONT_NAME, 10)
    c.setFillColor(COLOR_TEXT)
    for i, q in enumerate(["(a) 75 :", "(b) 89 :", "(c) 46 :", "(d) 99 :", "(e) 29 :"]):
        y_pos = cursor_y - 30 - (i * 18)
        c.drawString(col1 + 10, y_pos, q)
        c.setLineWidth(0.5)
        c.setStrokeColor(colors.grey)
        c.line(col1 + 50, y_pos - 2, col1 + col_width - 10, y_pos - 2)

    draw_card(c, col2, cursor_y - h_row1, col_width, h_row1, "प्र. 2: स्थानीय मान (Place Value)", "[5 अंक]")
    qs_q2 = ["(a) 540 में 5 का मान:", "(b) 892 में 9 का मान:", "(c) 1000 में 1 का मान:", "(d) 607 में 7 का मान:", "(e) 4550 में 0 का मान:"]
    for i, q in enumerate(qs_q2):
        y_pos = cursor_y - 30 - (i * 18)
        c.drawString(col2 + 10, y_pos, fix_text(q))
        c.setLineWidth(0.5)
        c.setStrokeColor(colors.grey)
        c.line(col2 + 120, y_pos - 2, col2 + col_width - 10, y_pos - 2)

    cursor_y -= (h_row1 + GAP)
    
    # Q3 Addition (Wide Card)
    h_math = 80
    draw_card(c, col1, cursor_y - h_math, width - 40, h_math, "प्र. 3: जोड़ें (Addition)", "[5 अंक]", accent_color=COLOR_ACCENT)
    
    # Grid for Math
    math_y = cursor_y - 50
    spacing = (width - 80) / 4
    start_x = col1 + 50
    
    draw_math_vertical(c, start_x, math_y, "4230", "+", "1540")
    draw_math_vertical(c, start_x + spacing, math_y, "6525", "+", "2354")
    draw_math_vertical(c, start_x + spacing*2, math_y, "5005", "+", "4990")
    draw_math_vertical(c, start_x + spacing*3, math_y, "1234", "+", "4321")
    
    cursor_y -= (h_math + GAP)
    
    # Q4 Subtraction (Wide Card)
    draw_card(c, col1, cursor_y - h_math, width - 40, h_math, "प्र. 4: घटाएँ (Subtraction)", "[5 अंक]", accent_color=COLOR_ACCENT)
    math_y = cursor_y - 50
    draw_math_vertical(c, start_x, math_y, "8956", "-", "4523")
    draw_math_vertical(c, start_x + spacing, math_y, "5640", "-", "2310")
    draw_math_vertical(c, start_x + spacing*2, math_y, "9000", "-", "1000")
    draw_math_vertical(c, start_x + spacing*3, math_y, "7550", "-", "2550")

    cursor_y -= (h_math + GAP)
    
    # Q5 & Q6
    h_row3 = 130
    draw_card(c, col1, cursor_y - h_row3, col_width, h_row3, "प्र. 5: विस्तारित रूप (Expanded Form)", "[5 अंक]")
    c.setFont(FONT_NAME, 9)
    q5_list = [
        "(a) 5426 = 5000 + 400 + 20 + 6",
        "(b) 3250 = ___ + ___ + ___ + 0",
        "(c) 7085 = ___ + 00 + ___ + 5",
        "(d) 1200 = 1000 + ___ + 00 + 0",
        "(e) 4040 = ___ + 0 + ___ + 0"
    ]
    for i, q in enumerate(q5_list):
        c.drawString(col1 + 10, cursor_y - 30 - (i*19), q)

    draw_card(c, col2, cursor_y - h_row3, col_width, h_row3, "प्र. 6: गुणा करें (Multiply)", "[5 अंक]")
    mul_spacing = col_width / 4
    mx = col2 + 10
    my = cursor_y - 60
    draw_math_vertical(c, mx, my, "24", "x", "2")
    draw_math_vertical(c, mx + mul_spacing + 5, my, "33", "x", "3")
    draw_math_vertical(c, mx + (mul_spacing+5)*2, my, "12", "x", "4")
    draw_math_vertical(c, mx + (mul_spacing+5)*3, my, "40", "x", "2")

    cursor_y -= (h_row3 + GAP)
    
    # Q7 & Q8
    h_row4 = 90
    draw_card(c, col1, cursor_y - h_row4, col_width, h_row4, "प्र. 7: चिन्ह लगाएँ (<, >, =)", "[5 अंक]")
    c.setFont(FONT_NAME, 11)
    c.drawString(col1 + 15, cursor_y - 35, "4500 [  ] 5400")
    c.drawString(col1 + 150, cursor_y - 35, "8000 [  ] 8000")
    c.drawString(col1 + 15, cursor_y - 55, "2020 [  ] 2002")
    c.drawString(col1 + 150, cursor_y - 55, "500 [  ] 50")
    c.drawString(col1 + 15, cursor_y - 75, "1010 [  ] 1001")

    draw_card(c, col2, cursor_y - h_row4, col_width, h_row4, "प्र. 8: भाग दें (Division)", "[5 अंक]")
    c.setFont(FONT_NAME, 10)
    c.drawString(col2 + 10, cursor_y - 30, "(a) 20 / 2 = ___")
    c.drawString(col2 + 120, cursor_y - 30, "(b) 15 / 3 = ___")
    c.drawString(col2 + 10, cursor_y - 50, "(c) 16 / 4 = ___")
    c.drawString(col2 + 120, cursor_y - 50, "(d) 10 / 5 = ___")
    c.drawString(col2 + 10, cursor_y - 70, "(e) 30 / 3 = ___")

    draw_footer_modern(c, width, 1)
    c.showPage()
    
    # ================= PAGE 2 =================
    draw_watermark(c, width, height)
    cursor_y = draw_modern_header(c, width, height, 2)
    
    # Page 2 Spacing
    P2_GAP = 18
    
    # Q9 & Q10
    h_p2_r1 = 110
    draw_card(c, col1, cursor_y - h_p2_r1, col_width, h_p2_r1, "प्र. 9: बढ़ते क्रम (Increasing Order)", "[5 अंक]")
    c.setFont(FONT_NAME, 10)
    c.drawString(col1 + 10, cursor_y - 30, "(a) 500, 200, 800, 100")
    c.drawString(col1 + 10, cursor_y - 45, "     -> ____, ____, ____, ____")
    c.drawString(col1 + 10, cursor_y - 65, "(b) 10, 50, 30, 20, 40")
    c.drawString(col1 + 10, cursor_y - 80, "     -> ____, ____, ____, ____, ____")

    draw_card(c, col2, cursor_y - h_p2_r1, col_width, h_p2_r1, "प्र. 10: घटते क्रम (Decreasing Order)", "[5 अंक]")
    c.drawString(col2 + 10, cursor_y - 30, "(a) 45, 90, 12, 65")
    c.drawString(col2 + 10, cursor_y - 45, "     -> ____, ____, ____, ____")
    c.drawString(col2 + 10, cursor_y - 65, "(b) 88, 11, 55, 33, 77")
    c.drawString(col2 + 10, cursor_y - 80, "     -> ____, ____, ____, ____, ____")

    cursor_y -= (h_p2_r1 + P2_GAP)

    # Q11 & Q12
    h_p2_r2 = 110
    draw_card(c, col1, cursor_y - h_p2_r2, col_width, h_p2_r2, "प्र. 11: पहले और बाद की संख्या", "[5 अंक]")
    c.drawString(col1 + 10, cursor_y - 30, "(a) ____ <- 500 -> ____")
    c.drawString(col1 + 10, cursor_y - 50, "(b) ____ <- 1000 -> ____")
    c.drawString(col1 + 10, cursor_y - 70, fix_text("(c) 99 के बाद: ________"))
    c.drawString(col1 + 10, cursor_y - 90, fix_text("(d) 50 से पहले: ________"))

    draw_card(c, col2, cursor_y - h_p2_r2, col_width, h_p2_r2, "प्र. 12: पहाड़ा और पैटर्न (Tables)", "[5 अंक]")
    c.drawString(col2 + 10, cursor_y - 30, fix_text("(a) 12 का पहाड़ा: 12, 24, ___, 48"))
    c.drawString(col2 + 10, cursor_y - 50, fix_text("(b) 15 का पहाड़ा: 15, 30, ___, 60"))
    c.drawString(col2 + 10, cursor_y - 70, fix_text("(c) 2 का पहाड़ा: 2, 4, 6, ___, 10"))
    c.drawString(col2 + 10, cursor_y - 90, "(d) 10, 20, 30, ___, 50")

    cursor_y -= (h_p2_r2 + P2_GAP)
    
    # Q13 & Q14 Word Problems (More Height)
    h_p2_r3 = 150
    draw_card(c, col1, cursor_y - h_p2_r3, col_width, h_p2_r3, "प्र. 13: हल करें (Word Problem)", "[5 अंक]", accent_color=COLOR_ACCENT)
    c.setFont(FONT_NAME, 10)
    # Broken lines for word wrapping
    lines_q13 = [
        "राम के पास 2500 रुपये, श्याम के पास",
        "1200 रुपये और मोहन के पास 100 रुपये हैं।",
        "तीनों के पास कुल कितने रुपये हैं?"
    ]
    for i, l in enumerate(lines_q13):
        c.drawString(col1 + 10, cursor_y - 35 - (i*18), fix_text(l))
        
    c.setFont(FONT_NAME, 11)
    c.drawString(col1 + 10, cursor_y - 120, fix_text("उत्तर: ______________________"))

    draw_card(c, col2, cursor_y - h_p2_r3, col_width, h_p2_r3, "प्र. 14: हल करें (Word Problem)", "[5 अंक]", accent_color=COLOR_ACCENT)
    lines_q14 = [
        "एक स्कूल में 4500 बच्चे हैं। आज 500",
        "बच्चे नहीं आए (Absent)। बताइये आज",
        "स्कूल में कितने बच्चे उपस्थित हैं?"
    ]
    c.setFont(FONT_NAME, 10)
    for i, l in enumerate(lines_q14):
        c.drawString(col2 + 10, cursor_y - 35 - (i*18), fix_text(l))
    
    c.setFont(FONT_NAME, 11)
    c.drawString(col2 + 10, cursor_y - 120, fix_text("उत्तर: ______________________"))

    cursor_y -= (h_p2_r3 + P2_GAP)
    
    # Q15 & Q16
    h_p2_r4 = 120
    draw_card(c, col1, cursor_y - h_p2_r4, col_width, h_p2_r4, "प्र. 15: पैटर्न पूरा करें", "[5 अंक]")
    c.setFont(FONT_NAME, 10)
    pats = [
        "(a) 100, 200, 300, ____, 500",
        "(b) 5, 10, 15, ____, 25",
        "(c) A, B, C, ____, E",
        "(d) 2, 4, 8, 16, ____",
        "(e) 11, 22, 33, ____, 55"
    ]
    for i, p in enumerate(pats):
        c.drawString(col1 + 10, cursor_y - 30 - (i*18), p)

    draw_card(c, col2, cursor_y - h_p2_r4, col_width, h_p2_r4, "प्र. 16: दिमागी कसरत (Mental Math)", "[5 अंक]")
    mmath = [
        "(a) 100 + 50 = ______",
        "(b) 500 में 1 जोड़ने पर? ______",
        "(c) 1 सप्ताह में कितने दिन? ______",
        "(d) 20 के 3 नोट = ______ रु",
        "(e) 10 में से 10 गया = ______"
    ]
    for i, m in enumerate(mmath):
        c.drawString(col2 + 10, cursor_y - 30 - (i*18), fix_text(m))

    # Bottom Good Luck
    c.setFont(FONT_NAME, 12)
    c.setFillColor(COLOR_PRIMARY)
    c.drawCentredString(width/2, cursor_y - h_p2_r4 - 30, fix_text("*** परीक्षा समाप्त (Good Luck) ***"))

    draw_footer_modern(c, width, 2)
    c.save()
    print(f"Successfully Created Modern Paper: {OUTPUT_FILENAME}")

if __name__ == "__main__":
    create_modern_paper()