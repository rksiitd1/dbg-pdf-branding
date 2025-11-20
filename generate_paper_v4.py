import os
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- CONFIGURATION ---
OUTPUT_FILENAME = "Class_1_Exam_Paper_Final_v4.pdf"
LOGO_LEFT = "DBG-logo.png"
LOGO_RIGHT = "DBM-logo.png"
WATERMARK_IMG = "DBG-logo.png"

# Font Strategy: 'Mangal' (Windows) often renders half-letters better in PDF 
# without a complex text engine than 'Noto'.
FONT_NAME = "HindiFont"
FONT_FILENAME = "Nirmala.ttf" # Default fallback

# --- HINDI & TEXT FIXES ---

def fix_hindi_rendering(text):
    """
    1. Fixes 'Chhoti Ee' (Matra correction).
    2. Manual patch for common conjuncts in this specific paper 
       to reduce visibility of Halants if font supports it.
    """
    if not text: return ""

    # 1. Fix Matra 'i' (Reorder: Consonant + Matra -> Matra + Consonant)
    def swap_matra(match):
        return "\u093f" + match.group(1)
    text = re.sub(r'([^\s])\u093f', swap_matra, text)

    # 2. Visual tweaks (Optional: if specific rendering fails, we accept the Halant, 
    # as removing it requires a C-library based Shaping Engine like HarfBuzz).
    # However, correct Unicode usually renders decent in Mangal/Nirmala.
    return text

# --- CANVAS SETUP ---
def setup_canvas():
    c = canvas.Canvas(OUTPUT_FILENAME, pagesize=A4)
    
    # Priority List for Fonts (Windows System Fonts work best for "dumb" shaping)
    font_candidates = [
        "C:\\Windows\\Fonts\\mangal.ttf",      # Best for conjuncts on Windows
        "C:\\Windows\\Fonts\\Nirmala.ttf",     # Good alternative
        "C:\\Windows\\Fonts\\arialuni.ttf",    # Fallback
        "NotoSansDevanagari-Regular.ttf",      # Local file (Requires Shaper usually)
        "Nirmala.ttf"                          # Local file
    ]

    loaded_font = None
    for path in font_candidates:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont(FONT_NAME, path))
                print(f"Font Loaded: {path}")
                loaded_font = path
                break
            except:
                continue
    
    if not loaded_font:
        print("WARNING: No Hindi font found. Text will be boxes.")
        return c, "Helvetica"
            
    return c, FONT_NAME

# --- DRAWING HELPERS (UPDATED LAYOUT) ---

def draw_watermark(c, width, height):
    if os.path.exists(WATERMARK_IMG):
        c.saveState()
        c.setFillAlpha(0.10) # 10% Opacity (Subtle)
        wm_size = 400        # Larger watermark
        c.drawImage(WATERMARK_IMG, (width - wm_size)/2, (height - wm_size)/2, 
                    width=wm_size, height=wm_size, mask='auto', preserveAspectRatio=True)
        c.restoreState()

def draw_header(c, width, height, page_text):
    c.saveState()
    
    # Logos
    logo_size = 65
    margin = 30
    if os.path.exists(LOGO_LEFT):
        c.drawImage(LOGO_LEFT, margin, height - 75, width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)
    if os.path.exists(LOGO_RIGHT):
        c.drawImage(LOGO_RIGHT, width - margin - logo_size, height - 75, width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)

    # Title
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 24)
    c.drawCentredString(width/2, height - 45, "DBG GURUKULAM")
    
    if page_text == "Page 1":
        c.setFont(FONT_NAME, 11)
        line1 = fix_hindi_rendering("कक्षा : 1 (First)   विषय: गणित (Maths)   समय: 2 घंटे")
        c.drawCentredString(width/2, height - 70, line1)
        
        # Name Box - Expanded Width & Spacing
        box_top = height - 90
        c.setLineWidth(0.8)
        c.rect(20, box_top - 25, width - 40, 25)
        c.setFont(FONT_NAME, 10)
        line2 = fix_hindi_rendering("नाम: ___________________________   रोल नं: _________   दिनांक: _________")
        c.drawString(25, box_top - 17, line2)
        
        # Max Marks - Spaced out
        c.setLineWidth(1.2)
        c.line(20, box_top - 35, width - 20, box_top - 35)
        
        c.setFont(FONT_NAME, 10)
        line3_left = "Total Questions: 16"
        line3_right = fix_hindi_rendering("पूर्णांक (Max Marks): 80")
        
        c.drawString(20, box_top - 50, line3_left)
        c.drawRightString(width - 20, box_top - 50, line3_right)
        c.setLineWidth(1)
        c.line(20, box_top - 55, width - 20, box_top - 55)
        
        return box_top - 65 # New Start Y
    else:
        # Page 2 Header
        c.setFont(FONT_NAME, 12)
        c.drawCentredString(width/2, height - 65, fix_hindi_rendering("गणित - भाग 2 (Page 2)"))
        c.setLineWidth(1)
        c.line(20, height - 75, width - 20, height - 75)
        return height - 90

    c.restoreState()

def draw_question_box(c, x, y, w, h, title, marks):
    """Draws rounded box with header"""
    c.saveState()
    radius = 6
    
    # Clip
    p = c.beginPath()
    p.roundRect(x, y, w, h, radius)
    c.clipPath(p, stroke=0)
    
    # Background
    c.setFillColor(colors.white)
    c.rect(x, y, w, h, fill=1, stroke=0)
    
    # Header Strip
    header_h = 22
    c.setFillColor(colors.Color(0.92, 0.92, 0.92))
    c.rect(x, y + h - header_h, w, header_h, fill=1, stroke=0)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.line(x, y + h - header_h, x + w, y + h - header_h)
    
    # Restore to draw border on top
    c.restoreState()
    c.saveState()
    c.setLineWidth(0.8)
    c.setStrokeColor(colors.black)
    c.roundRect(x, y, w, h, radius, stroke=1, fill=0)
    
    # Text
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 10)
    c.drawString(x + 8, y + h - 15, fix_hindi_rendering(title))
    c.drawRightString(x + w - 8, y + h - 15, fix_hindi_rendering(marks))
    c.restoreState()

def draw_math_block(c, x, y, num1, op, num2):
    c.saveState()
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 13)
    
    # Right Alignment
    c.drawRightString(x + 45, y, num1)
    c.drawRightString(x + 45, y - 16, num2)
    
    # Operator
    c.drawString(x, y - 16, op)
    
    # Line
    c.setLineWidth(1.2)
    c.line(x, y - 20, x + 50, y - 20)
    c.restoreState()

def draw_footer(c, width, page_num):
    c.saveState()
    footer_y = 25
    c.setLineWidth(0.5)
    c.line(20, footer_y + 12, width - 20, footer_y + 12)
    
    c.setFont(FONT_NAME, 9)
    c.setFillColor(colors.black)
    c.drawString(25, footer_y, f"Page {page_num}")
    
    c.drawCentredString(width/2, footer_y, "Shri Classes & DBG Gurukulam (by IITian Golu Sir)")
    
    c.setFillColor(colors.blue)
    c.drawRightString(width - 25, footer_y, "https://dbggurukulam.com")
    c.restoreState()

# --- MAIN CONTENT GENERATION ---

def create_paper():
    c, font_name = setup_canvas()
    if not c: return

    width, height = A4
    
    # ================= PAGE 1 =================
    draw_watermark(c, width, height)
    cursor_y = draw_header(c, width, height, "Page 1")
    
    # SPACING CONSTANTS (Expanded)
    GAP = 12        # Gap between boxes
    INNER_PAD = 20  # Space inside box before text starts
    
    col_gap = 15
    marg_x = 20
    col_w = (width - (2 * marg_x) - col_gap) / 2
    col1_x = marg_x
    col2_x = marg_x + col_w + col_gap
    
    # --- Q1 & Q2 (Height increased) ---
    h_row1 = 125 
    
    draw_question_box(c, col1_x, cursor_y - h_row1, col_w, h_row1, "प्र. 1: शब्दों में लिखें (Words)", "[5 अंक]")
    c.setFont(FONT_NAME, 10)
    q1_y = cursor_y - 25
    for item in ["(a) 75 : ________________", "(b) 89 : ________________", "(c) 46 : ________________", "(d) 99 : ________________", "(e) 29 : ________________"]:
        q1_y -= 18 # More line spacing
        c.drawString(col1_x + 10, q1_y, item)

    draw_question_box(c, col2_x, cursor_y - h_row1, col_w, h_row1, "प्र. 2: स्थानीय मान (Place Value)", "[5 अंक]")
    q2_y = cursor_y - 25
    items_q2 = ["(a) 540 में 5 का मान: _______", "(b) 892 में 9 का मान: _______", "(c) 1000 में 1 का मान: ______", "(d) 607 में 7 का मान: _______", "(e) 4550 में 0 का मान: ______"]
    for item in items_q2:
        q2_y -= 18
        c.drawString(col2_x + 10, q2_y, fix_hindi_rendering(item))

    cursor_y -= (h_row1 + GAP)

    # --- Q3 Addition (Height increased) ---
    h_math = 85 
    draw_question_box(c, col1_x, cursor_y - h_math, width - 40, h_math, "प्र. 3: जोड़ें (Addition)", "[5 अंक]")
    
    # Math items spacing
    sum_spacing = (width - 80) / 4
    q3_x = col1_x + 50
    q3_y = cursor_y - 45 # Centered vertically in box
    
    draw_math_block(c, q3_x, q3_y, "4230", "+", "1540")
    draw_math_block(c, q3_x + sum_spacing, q3_y, "6525", "+", "2354")
    draw_math_block(c, q3_x + sum_spacing*2, q3_y, "5005", "+", "4990")
    draw_math_block(c, q3_x + sum_spacing*3, q3_y, "1234", "+", "4321")

    cursor_y -= (h_math + GAP)

    # --- Q4 Subtraction ---
    draw_question_box(c, col1_x, cursor_y - h_math, width - 40, h_math, "प्र. 4: घटाएँ (Subtraction)", "[5 अंक]")
    q4_y = cursor_y - 45
    draw_math_block(c, q3_x, q4_y, "8956", "-", "4523")
    draw_math_block(c, q3_x + sum_spacing, q4_y, "5640", "-", "2310")
    draw_math_block(c, q3_x + sum_spacing*2, q4_y, "9000", "-", "1000")
    draw_math_block(c, q3_x + sum_spacing*3, q4_y, "7550", "-", "2550")

    cursor_y -= (h_math + GAP)

    # --- Q5 & Q6 ---
    h_row3 = 135 # Bigger for text
    draw_question_box(c, col1_x, cursor_y - h_row3, col_w, h_row3, "प्र. 5: विस्तारित रूप (Expanded Form)", "[5 अंक]")
    c.setFont(FONT_NAME, 9)
    q5_y = cursor_y - 25
    expanded_qs = [
        "(a) 5426 = 5000 + 400 + 20 + 6",
        "(b) 3250 = ____ + ____ + ____ + 0",
        "(c) 7085 = ____ + 00 + ____ + 5",
        "(d) 1200 = 1000 + ____ + 00 + 0",
        "(e) 4040 = ____ + 0 + ____ + 0"
    ]
    for item in expanded_qs:
        q5_y -= 19
        c.drawString(col1_x + 8, q5_y, item)

    draw_question_box(c, col2_x, cursor_y - h_row3, col_w, h_row3, "प्र. 6: गुणा करें (Multiply)", "[5 अंक]")
    mul_spacing = col_w / 4
    qm_x = col2_x + 15
    qm_y = cursor_y - 60
    draw_math_block(c, qm_x, qm_y, "24", "x", "2")
    draw_math_block(c, qm_x + mul_spacing + 5, qm_y, "33", "x", "3")
    draw_math_block(c, qm_x + (mul_spacing+5)*2, qm_y, "12", "x", "4")
    draw_math_block(c, qm_x + (mul_spacing+5)*3, qm_y, "40", "x", "2")

    cursor_y -= (h_row3 + GAP)

    # --- Q7 & Q8 ---
    h_row4 = 100 # More breathing room
    draw_question_box(c, col1_x, cursor_y - h_row4, col_w, h_row4, "प्र. 7: चिन्ह लगाएँ (<, >, =)", "[5 अंक]")
    c.setFont(FONT_NAME, 11)
    q7_y = cursor_y - 35
    c.drawString(col1_x + 10, q7_y, "4500 [___] 5400")
    c.drawString(col1_x + 140, q7_y, "8000 [___] 8000")
    q7_y -= 22
    c.drawString(col1_x + 10, q7_y, "2020 [___] 2002")
    c.drawString(col1_x + 140, q7_y, "500 [___] 50")
    q7_y -= 22
    c.drawString(col1_x + 10, q7_y, "1010 [___] 1001")

    draw_question_box(c, col2_x, cursor_y - h_row4, col_w, h_row4, "प्र. 8: भाग दें (Division)", "[5 अंक]")
    q8_y = cursor_y - 30
    c.drawString(col2_x + 10, q8_y, "(a) 20 ÷ 2 = ___")
    c.drawString(col2_x + 130, q8_y, "(b) 15 ÷ 3 = ___")
    q8_y -= 20
    c.drawString(col2_x + 10, q8_y, "(c) 16 ÷ 4 = ___")
    c.drawString(col2_x + 130, q8_y, "(d) 10 ÷ 5 = ___")
    q8_y -= 20
    c.drawString(col2_x + 10, q8_y, "(e) 30 ÷ 3 = ___")

    draw_footer(c, width, 1)
    c.showPage()

    # ================= PAGE 2 =================
    draw_watermark(c, width, height)
    cursor_y = draw_header(c, width, height, "Page 2")
    cursor_y -= 5

    # Page 2 Vertical Spacing Strategy - Fill the page
    P2_GAP = 20 
    
    # --- Q9 & Q10 ---
    h_p2_row1 = 100
    draw_question_box(c, col1_x, cursor_y - h_p2_row1, col_w, h_p2_row1, "प्र. 9: बढ़ते क्रम (Increasing Order)", "[5 अंक]")
    c.setFont(FONT_NAME, 10)
    c.drawString(col1_x + 10, cursor_y - 30, "(a) 500, 200, 800, 100")
    c.drawString(col1_x + 10, cursor_y - 45, "     -> ____, ____, ____, ____")
    c.drawString(col1_x + 10, cursor_y - 65, "(b) 10, 50, 30, 20, 40")
    c.drawString(col1_x + 10, cursor_y - 80, "     -> ____, ____, ____, ____, ____")

    draw_question_box(c, col2_x, cursor_y - h_p2_row1, col_w, h_p2_row1, "प्र. 10: घटते क्रम (Decreasing Order)", "[5 अंक]")
    c.drawString(col2_x + 10, cursor_y - 30, "(a) 45, 90, 12, 65")
    c.drawString(col2_x + 10, cursor_y - 45, "     -> ____, ____, ____, ____")
    c.drawString(col2_x + 10, cursor_y - 65, "(b) 88, 11, 55, 33, 77")
    c.drawString(col2_x + 10, cursor_y - 80, "     -> ____, ____, ____, ____, ____")

    cursor_y -= (h_p2_row1 + P2_GAP)

    # --- Q11 & Q12 ---
    h_p2_row2 = 120
    draw_question_box(c, col1_x, cursor_y - h_p2_row2, col_w, h_p2_row2, "प्र. 11: पहले और बाद की संख्या", "[5 अंक]")
    q11_y = cursor_y - 30
    c.drawString(col1_x + 10, q11_y, "(a) ____ <- 500 -> ____")
    c.drawString(col1_x + 10, q11_y - 22, "(b) ____ <- 1000 -> ____")
    c.drawString(col1_x + 10, q11_y - 44, fix_hindi_rendering("(c) 99 के बाद: ________"))
    c.drawString(col1_x + 10, q11_y - 66, fix_hindi_rendering("(d) 50 से पहले: ________"))

    draw_question_box(c, col2_x, cursor_y - h_p2_row2, col_w, h_p2_row2, "प्र. 12: पहाड़ा और पैटर्न (Tables)", "[5 अंक]")
    q12_y = cursor_y - 30
    c.drawString(col2_x + 10, q12_y, fix_hindi_rendering("(a) 12 का पहाड़ा: 12, 24, ___, 48"))
    c.drawString(col2_x + 10, q12_y - 22, fix_hindi_rendering("(b) 15 का पहाड़ा: 15, 30, ___, 60"))
    c.drawString(col2_x + 10, q12_y - 44, fix_hindi_rendering("(c) 2 का पहाड़ा: 2, 4, 6, ___, 10"))
    c.drawString(col2_x + 10, q12_y - 66, "(d) 10, 20, 30, ___, 50")

    cursor_y -= (h_p2_row2 + P2_GAP)

    # --- Q13 & Q14 ---
    h_p2_row3 = 140 # Extra space for word problems
    draw_question_box(c, col1_x, cursor_y - h_p2_row3, col_w, h_p2_row3, "प्र. 13: हल करें (Word Problem)", "[5 अंक]")
    c.setFont(FONT_NAME, 10)
    t1 = fix_hindi_rendering("राम के पास 2500 रुपये, श्याम के पास")
    t2 = fix_hindi_rendering("1200 रुपये और मोहन के पास 100 रुपये हैं।")
    t3 = fix_hindi_rendering("तीनों के पास कुल कितने रुपये हैं?")
    
    c.drawString(col1_x + 8, cursor_y - 30, t1)
    c.drawString(col1_x + 8, cursor_y - 48, t2)
    c.drawString(col1_x + 8, cursor_y - 66, t3)
    
    c.drawString(col1_x + 8, cursor_y - 115, fix_hindi_rendering("उत्तर: __________________________"))

    draw_question_box(c, col2_x, cursor_y - h_p2_row3, col_w, h_p2_row3, "प्र. 14: हल करें (Word Problem)", "[5 अंक]")
    t1 = fix_hindi_rendering("एक स्कूल में 4500 बच्चे हैं। आज 500")
    t2 = fix_hindi_rendering("बच्चे नहीं आए (Absent)। बताइये आज")
    t3 = fix_hindi_rendering("स्कूल में कितने बच्चे उपस्थित हैं?")
    c.drawString(col2_x + 8, cursor_y - 30, t1)
    c.drawString(col2_x + 8, cursor_y - 48, t2)
    c.drawString(col2_x + 8, cursor_y - 66, t3)
    
    c.drawString(col2_x + 8, cursor_y - 115, fix_hindi_rendering("उत्तर: __________________________"))

    cursor_y -= (h_p2_row3 + P2_GAP)

    # --- Q15 & Q16 ---
    h_p2_row4 = 120
    draw_question_box(c, col1_x, cursor_y - h_p2_row4, col_w, h_p2_row4, "प्र. 15: पैटर्न पूरा करें", "[5 अंक]")
    q15_y = cursor_y - 30
    c.drawString(col1_x + 10, q15_y, "(a) 100, 200, 300, _____, 500")
    c.drawString(col1_x + 10, q15_y - 18, "(b) 5, 10, 15, _____, 25")
    c.drawString(col1_x + 10, q15_y - 36, "(c) A, B, C, _____, E")
    c.drawString(col1_x + 10, q15_y - 54, "(d) 2, 4, 8, 16, ______")
    c.drawString(col1_x + 10, q15_y - 72, "(e) 11, 22, 33, _____, 55")

    draw_question_box(c, col2_x, cursor_y - h_p2_row4, col_w, h_p2_row4, "प्र. 16: दिमागी कसरत (Mental Math)", "[5 अंक]")
    q16_y = cursor_y - 30
    c.drawString(col2_x + 10, q16_y, "(a) 100 + 50 = ______")
    c.drawString(col2_x + 10, q16_y - 18, fix_hindi_rendering("(b) 500 में 1 जोड़ने पर? ______"))
    c.drawString(col2_x + 10, q16_y - 36, fix_hindi_rendering("(c) 1 सप्ताह में कितने दिन? ______"))
    c.drawString(col2_x + 10, q16_y - 54, fix_hindi_rendering("(d) 20 के 3 नोट = ______ रु"))
    c.drawString(col2_x + 10, q16_y - 72, fix_hindi_rendering("(e) 10 में से 10 गया = ______"))

    # Good Luck - Moved to bottom area
    c.setFont(FONT_NAME, 12)
    c.drawCentredString(width/2, cursor_y - h_p2_row4 - 35, fix_hindi_rendering("*** परीक्षा समाप्त (Good Luck) ***"))
    
    draw_footer(c, width, 2)
    c.save()
    print(f"PDF Created: {OUTPUT_FILENAME}")

if __name__ == "__main__":
    create_paper()