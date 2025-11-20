import os
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- CONFIGURATION ---
OUTPUT_FILENAME = "Class_1_Exam_Paper_Fixed.pdf"
LOGO_LEFT = "DBG-logo.png"
LOGO_RIGHT = "DBM-logo.png"
WATERMARK_IMG = "DBG-logo.png"

# Font Configuration
# Please ensure one of these fonts is in the folder or installed
# Noto Sans Devanagari is BEST for Hindi.
FONT_FILENAME = "NotoSansDevanagari-Regular.ttf" 
FONT_NAME = "HindiFont"

# --- HINDI RENDERING FIXER ---
def fix_hindi(text):
    """
    Fixes common rendering issues for Hindi in ReportLab.
    Specifically handles the 'Chhoti Ee' (Short I) matra reordering.
    """
    if not text: return ""
    
    # Logic: Find a Consonant followed by Matra-I (U+093F)
    # and swap them. e.g. "कि" (Ka + i) -> Visual needs (i + Ka)
    
    # Regex to find (Consonant)(Matra I)
    # \u093f is the Short I matra
    # [^\u093f] matches the char before it
    
    def swap_matra(match):
        return "\u093f" + match.group(1)

    # Simple reordering for display (Swap char + matra_i)
    # Note: This is a basic fix. For complex conjuncts, this might need more logic,
    # but it fixes 90% of "weird" Hindi issues in basic papers.
    fixed_text = re.sub(r'([^\s])\u093f', swap_matra, text)
    return fixed_text

# --- SETUP ---
def setup_canvas():
    c = canvas.Canvas(OUTPUT_FILENAME, pagesize=A4)
    
    # 1. Try loading the font
    font_found = False
    font_paths = [
        "NotoSansDevanagari-Regular.ttf",  # Look for local Noto
        "Nirmala.ttf",                     # Look for local Nirmala
        "C:\\Windows\\Fonts\\Nirmala.ttf", # System Nirmala
        "C:\\Windows\\Fonts\\Mangal.ttf",  # System Mangal
        "C:\\Windows\\Fonts\\ArialUni.ttf" # System Arial Unicode
    ]

    for path in font_paths:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont(FONT_NAME, path))
                print(f"Font Loaded: {path}")
                font_found = True
                break
            except:
                continue
    
    if not font_found:
        print("WARNING: No Hindi font found. Text will be boxes.")
        return c, "Helvetica"
            
    return c, FONT_NAME

# --- DRAWING HELPERS ---

def draw_watermark(c, width, height):
    if os.path.exists(WATERMARK_IMG):
        c.saveState()
        c.setFillAlpha(0.12) # Very light (12%)
        wm_size = 350
        c.drawImage(WATERMARK_IMG, (width - wm_size)/2, (height - wm_size)/2, 
                    width=wm_size, height=wm_size, mask='auto', preserveAspectRatio=True)
        c.restoreState()

def draw_header(c, width, height, page_text):
    c.saveState()
    
    # Logos (Smaller to save space)
    logo_size = 60
    margin = 25
    if os.path.exists(LOGO_LEFT):
        c.drawImage(LOGO_LEFT, margin, height - 75, width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)
    if os.path.exists(LOGO_RIGHT):
        c.drawImage(LOGO_RIGHT, width - margin - logo_size, height - 75, width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)

    # Center Title
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 20)
    c.drawCentredString(width/2, height - 45, "DBG GURUKULAM")
    
    if page_text == "Page 1":
        # Compact Header Info
        c.setFont(FONT_NAME, 10)
        # Apply Hindi Fix
        line1 = fix_hindi("कक्षा : 1 (First)   विषय: गणित (Maths)   समय: 2 घंटे")
        c.drawCentredString(width/2, height - 65, line1)
        
        # Name Box (Compressed height)
        box_top = height - 80
        c.setLineWidth(0.8)
        c.rect(20, box_top - 20, width - 40, 20)
        c.setFont(FONT_NAME, 9)
        line2 = fix_hindi("नाम: ________________________   रोल नं: _______   दिनांक: _______")
        c.drawString(25, box_top - 13, line2)
        
        # Max Marks Line
        c.setLineWidth(1)
        c.line(20, box_top - 25, width - 20, box_top - 25)
        
        line3_left = fix_hindi("Total Questions: 16")
        line3_right = fix_hindi("पूर्णांक (Max Marks): 80")
        
        c.drawString(20, box_top - 38, line3_left)
        c.drawRightString(width - 20, box_top - 38, line3_right)
        c.line(20, box_top - 42, width - 20, box_top - 42)
        
        return box_top - 45 # Return the new Y cursor
    else:
        # Page 2 Header
        c.setFont(FONT_NAME, 10)
        title_p2 = fix_hindi("गणित - भाग 2 (Page 2)")
        c.drawCentredString(width/2, height - 65, title_p2)
        c.setLineWidth(1)
        c.line(20, height - 75, width - 20, height - 75)
        return height - 80

    c.restoreState()

def draw_question_box(c, x, y, w, h, title, marks):
    """Draws rounded box with correct Hindi title"""
    c.saveState()
    radius = 5
    
    # Clip header
    p = c.beginPath()
    p.roundRect(x, y, w, h, radius)
    c.clipPath(p, stroke=0)
    
    # Fill White
    c.setFillColor(colors.white)
    c.rect(x, y, w, h, fill=1, stroke=0)
    
    # Fill Grey Header
    header_h = 18
    c.setFillColor(colors.Color(0.92, 0.92, 0.92))
    c.rect(x, y + h - header_h, w, header_h, fill=1, stroke=0)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.line(x, y + h - header_h, x + w, y + h - header_h)
    
    # Border
    c.restoreState()
    c.saveState()
    c.setLineWidth(0.8)
    c.setStrokeColor(colors.black)
    c.roundRect(x, y, w, h, radius, stroke=1, fill=0)
    
    # Text
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 9) # Keep title font slightly smaller for fit
    c.drawString(x + 6, y + h - 13, fix_hindi(title))
    c.drawRightString(x + w - 6, y + h - 13, fix_hindi(marks))
    c.restoreState()

def draw_math_block(c, x, y, num1, op, num2):
    """Tight math block"""
    c.saveState()
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 12)
    
    # Right align numbers
    c.drawRightString(x + 35, y, num1)
    c.drawRightString(x + 35, y - 14, num2)
    c.drawString(x - 5, y - 14, op)
    
    c.setLineWidth(1)
    c.line(x - 5, y - 18, x + 40, y - 18)
    c.restoreState()

def draw_footer(c, width, page_num):
    c.saveState()
    footer_y = 20
    c.setLineWidth(0.5)
    c.line(20, footer_y + 10, width - 20, footer_y + 10)
    
    c.setFont(FONT_NAME, 8)
    c.setFillColor(colors.black)
    c.drawString(25, footer_y, f"Page {page_num}")
    
    center_text = "Shri Classes & DBG Gurukulam (by IITian Golu Sir)"
    c.drawCentredString(width/2, footer_y, center_text)
    
    c.setFillColor(colors.blue)
    c.drawRightString(width - 25, footer_y, "https://dbggurukulam.com")
    c.restoreState()

# --- MAIN LOGIC ---

def create_paper():
    c, font_name = setup_canvas()
    if not c: return

    width, height = A4
    
    # ================= PAGE 1 =================
    draw_watermark(c, width, height)
    
    # Header returns the Y position where we can start
    cursor_y = draw_header(c, width, height, "Page 1")
    
    # GAP CONFIGURATION (Tightening spaces)
    GAP_BIG = 8
    GAP_SMALL = 4
    
    col_gap = 10
    marg_x = 20
    col_w = (width - (2 * marg_x) - col_gap) / 2
    col1_x = marg_x
    col2_x = marg_x + col_w + col_gap
    
    cursor_y -= 5 # Initial buffer
    
    # --- Q1 & Q2 ---
    # Reduce height slightly to ensure fit
    h_row1 = 100 
    
    draw_question_box(c, col1_x, cursor_y - h_row1, col_w, h_row1, "प्र. 1: शब्दों में लिखें (Words)", "[5 अंक]")
    c.setFont(FONT_NAME, 10)
    q1_y = cursor_y - 20
    items_q1 = ["(a) 75 : ________", "(b) 89 : ________", "(c) 46 : ________", "(d) 99 : ________", "(e) 29 : ________"]
    for item in items_q1:
        q1_y -= 15
        c.drawString(col1_x + 8, q1_y, item)

    draw_question_box(c, col2_x, cursor_y - h_row1, col_w, h_row1, "प्र. 2: स्थानीय मान (Place Value)", "[5 अंक]")
    # Using the fix_hindi on content too
    items_q2 = ["(a) 540 में 5 का मान: _____", "(b) 892 में 9 का मान: _____", "(c) 1000 में 1 का मान: ____", "(d) 607 में 7 का मान: _____", "(e) 4550 में 0 का मान: ____"]
    q2_y = cursor_y - 20
    for item in items_q2:
        q2_y -= 15
        c.drawString(col2_x + 8, q2_y, fix_hindi(item))

    cursor_y -= (h_row1 + GAP_BIG)

    # --- Q3 Addition ---
    h_math = 65 # Reduced height for math boxes
    draw_question_box(c, col1_x, cursor_y - h_math, width - 40, h_math, "प्र. 3: जोड़ें (Addition)", "[5 अंक]")
    
    sum_spacing = (width - 60) / 4
    q3_x = col1_x + 40
    q3_y = cursor_y - 35 # Moved math up slightly
    
    draw_math_block(c, q3_x, q3_y, "4230", "+", "1540")
    draw_math_block(c, q3_x + sum_spacing, q3_y, "6525", "+", "2354")
    draw_math_block(c, q3_x + sum_spacing*2, q3_y, "5005", "+", "4990")
    draw_math_block(c, q3_x + sum_spacing*3, q3_y, "1234", "+", "4321")

    cursor_y -= (h_math + GAP_BIG)

    # --- Q4 Subtraction ---
    draw_question_box(c, col1_x, cursor_y - h_math, width - 40, h_math, "प्र. 4: घटाएँ (Subtraction)", "[5 अंक]")
    q4_y = cursor_y - 35
    draw_math_block(c, q3_x, q4_y, "8956", "-", "4523")
    draw_math_block(c, q3_x + sum_spacing, q4_y, "5640", "-", "2310")
    draw_math_block(c, q3_x + sum_spacing*2, q4_y, "9000", "-", "1000")
    draw_math_block(c, q3_x + sum_spacing*3, q4_y, "7550", "-", "2550")

    cursor_y -= (h_math + GAP_BIG)

    # --- Q5 & Q6 ---
    h_row3 = 110
    draw_question_box(c, col1_x, cursor_y - h_row3, col_w, h_row3, "प्र. 5: विस्तारित रूप (Expanded Form)", "[5 अंक]")
    c.setFont(FONT_NAME, 9)
    q5_y = cursor_y - 18
    expanded_qs = [
        "(a) 5426 = 5000 + 400 + 20 + 6",
        "(b) 3250 = ___ + ___ + ___ + 0",
        "(c) 7085 = ___ + 00 + ___ + 5",
        "(d) 1200 = 1000 + ___ + 00 + 0",
        "(e) 4040 = ___ + 0 + ___ + 0"
    ]
    for item in expanded_qs:
        q5_y -= 16
        c.drawString(col1_x + 6, q5_y, item)

    draw_question_box(c, col2_x, cursor_y - h_row3, col_w, h_row3, "प्र. 6: गुणा करें (Multiply)", "[5 अंक]")
    mul_spacing = col_w / 4
    qm_x = col2_x + 10
    qm_y = cursor_y - 50
    draw_math_block(c, qm_x, qm_y, "24", "x", "2")
    draw_math_block(c, qm_x + mul_spacing + 5, qm_y, "33", "x", "3")
    draw_math_block(c, qm_x + (mul_spacing+5)*2, qm_y, "12", "x", "4")
    draw_math_block(c, qm_x + (mul_spacing+5)*3, qm_y, "40", "x", "2")

    cursor_y -= (h_row3 + GAP_BIG)

    # --- Q7 & Q8 ---
    h_row4 = 80 # Made smaller
    draw_question_box(c, col1_x, cursor_y - h_row4, col_w, h_row4, "प्र. 7: चिन्ह लगाएँ (<, >, =)", "[5 अंक]")
    c.setFont(FONT_NAME, 10)
    q7_y = cursor_y - 30
    c.drawString(col1_x + 8, q7_y, "4500 [__] 5400")
    c.drawString(col1_x + 130, q7_y, "8000 [__] 8000")
    q7_y -= 18
    c.drawString(col1_x + 8, q7_y, "2020 [__] 2002")
    c.drawString(col1_x + 130, q7_y, "500 [__] 50")
    q7_y -= 18
    c.drawString(col1_x + 8, q7_y, "1010 [__] 1001")

    draw_question_box(c, col2_x, cursor_y - h_row4, col_w, h_row4, "प्र. 8: भाग दें (Division)", "[5 अंक]")
    q8_y = cursor_y - 25
    c.drawString(col2_x + 8, q8_y, "(a) 20 ÷ 2 = ___")
    c.drawString(col2_x + 120, q8_y, "(b) 15 ÷ 3 = ___")
    q8_y -= 18
    c.drawString(col2_x + 8, q8_y, "(c) 16 ÷ 4 = ___")
    c.drawString(col2_x + 120, q8_y, "(d) 10 ÷ 5 = ___")
    q8_y -= 18
    c.drawString(col2_x + 8, q8_y, "(e) 30 ÷ 3 = ___")

    draw_footer(c, width, 1)
    c.showPage()

    # ================= PAGE 2 =================
    draw_watermark(c, width, height)
    cursor_y = draw_header(c, width, height, "Page 2")
    cursor_y -= 5

    # --- Q9 & Q10 ---
    h_p2_row1 = 80
    draw_question_box(c, col1_x, cursor_y - h_p2_row1, col_w, h_p2_row1, "प्र. 9: बढ़ते क्रम (Increasing)", "[5 अंक]")
    c.setFont(FONT_NAME, 9)
    c.drawString(col1_x + 8, cursor_y - 25, "(a) 500, 200, 800, 100")
    c.drawString(col1_x + 8, cursor_y - 38, "     -> ___, ___, ___, ___")
    c.drawString(col1_x + 8, cursor_y - 53, "(b) 10, 50, 30, 20, 40")
    c.drawString(col1_x + 8, cursor_y - 66, "     -> ___, ___, ___, ___, ___")

    draw_question_box(c, col2_x, cursor_y - h_p2_row1, col_w, h_p2_row1, "प्र. 10: घटते क्रम (Decreasing)", "[5 अंक]")
    c.drawString(col2_x + 8, cursor_y - 25, "(a) 45, 90, 12, 65")
    c.drawString(col2_x + 8, cursor_y - 38, "     -> ___, ___, ___, ___")
    c.drawString(col2_x + 8, cursor_y - 53, "(b) 88, 11, 55, 33, 77")
    c.drawString(col2_x + 8, cursor_y - 66, "     -> ___, ___, ___, ___, ___")

    cursor_y -= (h_p2_row1 + GAP_BIG)

    # --- Q11 & Q12 ---
    h_p2_row2 = 90
    draw_question_box(c, col1_x, cursor_y - h_p2_row2, col_w, h_p2_row2, "प्र. 11: पहले और बाद की संख्या", "[5 अंक]")
    q11_y = cursor_y - 25
    c.drawString(col1_x + 8, q11_y, "(a) ____ <- 500 -> ____")
    c.drawString(col1_x + 8, q11_y - 18, "(b) ____ <- 1000 -> ____")
    c.drawString(col1_x + 8, q11_y - 36, fix_hindi("(c) 99 के बाद: ________"))
    c.drawString(col1_x + 8, q11_y - 54, fix_hindi("(d) 50 से पहले: ________"))

    draw_question_box(c, col2_x, cursor_y - h_p2_row2, col_w, h_p2_row2, "प्र. 12: पहाड़ा और पैटर्न (Tables)", "[5 अंक]")
    q12_y = cursor_y - 25
    c.drawString(col2_x + 8, q12_y, fix_hindi("(a) 12 का पहाड़ा: 12, 24, __, 48"))
    c.drawString(col2_x + 8, q12_y - 18, fix_hindi("(b) 15 का पहाड़ा: 15, 30, __, 60"))
    c.drawString(col2_x + 8, q12_y - 36, fix_hindi("(c) 2 का पहाड़ा: 2, 4, 6, __, 10"))
    c.drawString(col2_x + 8, q12_y - 54, "(d) 10, 20, 30, __, 50")

    cursor_y -= (h_p2_row2 + GAP_BIG)

    # --- Q13 & Q14 ---
    h_p2_row3 = 110
    draw_question_box(c, col1_x, cursor_y - h_p2_row3, col_w, h_p2_row3, "प्र. 13: हल करें (Word Problem)", "[5 अंक]")
    c.setFont(FONT_NAME, 9)
    # Pre-fixed text
    t1 = fix_hindi("राम के पास 2500 रुपये, श्याम के पास")
    t2 = fix_hindi("1200 रुपये और मोहन के पास 100 रुपये हैं।")
    t3 = fix_hindi("तीनों के पास कुल कितने रुपये हैं?")
    
    c.drawString(col1_x + 6, cursor_y - 25, t1)
    c.drawString(col1_x + 6, cursor_y - 40, t2)
    c.drawString(col1_x + 6, cursor_y - 55, t3)
    c.setLineWidth(0.5)
    c.drawString(col1_x + 6, cursor_y - 95, fix_hindi("उत्तर: _____________________"))

    draw_question_box(c, col2_x, cursor_y - h_p2_row3, col_w, h_p2_row3, "प्र. 14: हल करें (Word Problem)", "[5 अंक]")
    t1 = fix_hindi("एक स्कूल में 4500 बच्चे हैं। आज 500")
    t2 = fix_hindi("बच्चे नहीं आए (Absent)। बताइये आज")
    t3 = fix_hindi("स्कूल में कितने बच्चे उपस्थित हैं?")
    c.drawString(col2_x + 6, cursor_y - 25, t1)
    c.drawString(col2_x + 6, cursor_y - 40, t2)
    c.drawString(col2_x + 6, cursor_y - 55, t3)
    c.drawString(col2_x + 6, cursor_y - 95, fix_hindi("उत्तर: _____________________"))

    cursor_y -= (h_p2_row3 + GAP_BIG)

    # --- Q15 & Q16 ---
    h_p2_row4 = 110
    draw_question_box(c, col1_x, cursor_y - h_p2_row4, col_w, h_p2_row4, "प्र. 15: पैटर्न पूरा करें", "[5 अंक]")
    q15_y = cursor_y - 25
    c.drawString(col1_x + 8, q15_y, "(a) 100, 200, 300, ____, 500")
    c.drawString(col1_x + 8, q15_y - 16, "(b) 5, 10, 15, ____, 25")
    c.drawString(col1_x + 8, q15_y - 32, "(c) A, B, C, ____, E")
    c.drawString(col1_x + 8, q15_y - 48, "(d) 2, 4, 8, 16, ____")
    c.drawString(col1_x + 8, q15_y - 64, "(e) 11, 22, 33, ____, 55")

    draw_question_box(c, col2_x, cursor_y - h_p2_row4, col_w, h_p2_row4, "प्र. 16: दिमागी कसरत (Mental Math)", "[5 अंक]")
    q16_y = cursor_y - 25
    c.drawString(col2_x + 8, q16_y, "(a) 100 + 50 = ______")
    c.drawString(col2_x + 8, q16_y - 16, fix_hindi("(b) 500 में 1 जोड़ने पर? ______"))
    c.drawString(col2_x + 8, q16_y - 32, fix_hindi("(c) 1 सप्ताह में कितने दिन? ______"))
    c.drawString(col2_x + 8, q16_y - 48, fix_hindi("(d) 20 के 3 नोट = ______ रु"))
    c.drawString(col2_x + 8, q16_y - 64, fix_hindi("(e) 10 में से 10 गया = ______"))

    # Good Luck (Ensuring it fits)
    c.setFont(FONT_NAME, 11)
    c.drawCentredString(width/2, 45, fix_hindi("*** परीक्षा समाप्त (Good Luck) ***"))
    
    draw_footer(c, width, 2)
    c.save()
    print(f"PDF Created: {OUTPUT_FILENAME}")

if __name__ == "__main__":
    create_paper()