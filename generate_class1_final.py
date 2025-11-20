import os
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
FONT_FILENAME = "Nirmala.ttf"
FONT_NAME = "NirmalaCustom"

# --- SETUP CANVAS & FONT ---
def setup_canvas():
    c = canvas.Canvas(OUTPUT_FILENAME, pagesize=A4)
    
    # Load Font
    if os.path.exists(FONT_FILENAME):
        try:
            pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_FILENAME))
            print(f"Success: Loaded local {FONT_FILENAME}")
        except Exception as e:
            print(f"Error loading local font: {e}")
            return None, None
    else:
        # Fallback to Windows System Fonts
        try:
            system_path = "C:\\Windows\\Fonts\\Nirmala.ttf"
            if os.path.exists(system_path):
                pdfmetrics.registerFont(TTFont(FONT_NAME, system_path))
                print("Loaded system Nirmala.ttf")
            else:
                print("Warning: Nirmala.ttf not found. Hindi might not render.")
                return None, "Helvetica"
        except:
            pass
            
    return c, FONT_NAME

# --- DRAWING FUNCTIONS ---

def draw_watermark(c, width, height):
    if os.path.exists(WATERMARK_IMG):
        c.saveState()
        c.setFillAlpha(0.15) # 15% transparent
        wm_size = 350
        c.drawImage(WATERMARK_IMG, (width - wm_size)/2, (height - wm_size)/2, 
                    width=wm_size, height=wm_size, mask='auto', preserveAspectRatio=True)
        c.restoreState()

def draw_header(c, width, height, page_text=""):
    c.saveState() # Protect state
    
    # Logos
    logo_size = 65
    margin = 25
    if os.path.exists(LOGO_LEFT):
        c.drawImage(LOGO_LEFT, margin, height - 80, width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)
    if os.path.exists(LOGO_RIGHT):
        c.drawImage(LOGO_RIGHT, width - margin - logo_size, height - 80, width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)

    # Center Title
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 22)
    c.drawCentredString(width/2, height - 45, "DBG GURUKULAM")
    
    if page_text == "Page 1":
        # Sub-header info
        c.setFont(FONT_NAME, 11)
        info_text = "कक्षा : 1 (First)     विषय: गणित (Maths)     समय: 2 घंटे"
        c.drawCentredString(width/2, height - 70, info_text)
        
        # Name Box
        box_top = height - 90
        c.setLineWidth(1)
        c.rect(20, box_top - 25, width - 40, 25)
        c.setFont(FONT_NAME, 10)
        c.drawString(30, box_top - 17, "नाम: _____________________________   रोल नं: _______   दिनांक: _______")
        
        # Max Marks
        c.setLineWidth(1.5)
        c.line(20, box_top - 35, width - 20, box_top - 35)
        
        c.setFont(FONT_NAME, 10)
        c.drawString(20, box_top - 50, "Total Questions: 16")
        c.drawRightString(width - 20, box_top - 50, "पूर्णांक (Max Marks): 80")
        c.setLineWidth(1)
        c.line(20, box_top - 55, width - 20, box_top - 55)
    else:
        # Page 2 Header
        c.setFont(FONT_NAME, 12)
        c.drawCentredString(width/2, height - 65, "गणित - भाग 2 (Page 2)")
        c.setLineWidth(1)
        c.line(20, height - 75, width - 20, height - 75)
    
    c.restoreState()

def draw_footer(c, width, page_num):
    c.saveState()
    footer_y = 25
    c.setLineWidth(0.5)
    c.line(20, footer_y + 12, width - 20, footer_y + 12)
    
    c.setFont(FONT_NAME, 9)
    c.setFillColor(colors.black)
    c.drawString(25, footer_y, f"Page {page_num}")
    
    center_text = "Shri Classes & DBG Gurukulam (by IITian Golu Sir)"
    c.drawCentredString(width/2, footer_y, center_text)
    
    c.setFillColor(colors.blue)
    c.drawRightString(width - 25, footer_y, "https://dbggurukulam.com")
    c.restoreState()

def draw_question_box(c, x, y, w, h, title, marks):
    """Draws the rounded container with grey header"""
    c.saveState() # IMPORTANT: Save state so we don't leave the color as White
    
    radius = 6
    # 1. Draw White Filled Box
    c.setLineWidth(1)
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.white)
    c.roundRect(x, y, w, h, radius, stroke=1, fill=1)
    
    # 2. Draw Grey Header
    header_h = 20
    p = c.beginPath()
    p.roundRect(x, y, w, h, radius)
    c.clipPath(p, stroke=0) # Clip to rounded corners
    
    c.setFillColor(colors.Color(0.9, 0.9, 0.9)) # Light Grey
    c.rect(x, y + h - header_h, w, header_h, fill=1, stroke=0)
    
    # Draw Line
    c.setStrokeColor(colors.black)
    c.line(x, y + h - header_h, x + w, y + h - header_h)
    
    # Draw Text
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 10)
    c.drawString(x + 8, y + h - 14, title)
    c.drawRightString(x + w - 8, y + h - 14, marks)
    
    c.restoreState() # IMPORTANT: Restores color to Black (or whatever it was)

def draw_vertical_math(c, x, y, num1, op, num2):
    c.saveState()
    c.setFillColor(colors.black) # Ensure text is black
    c.setFont(FONT_NAME, 14)
    c.drawRightString(x + 40, y, num1)
    c.drawString(x, y - 18, op) 
    c.drawRightString(x + 40, y - 18, num2)
    c.setLineWidth(1.5)
    c.line(x, y - 22, x + 45, y - 22)
    c.restoreState()

# --- MAIN LOGIC ---

def create_paper():
    c, font_name = setup_canvas()
    if not c: return

    width, height = A4
    
    # ================= PAGE 1 =================
    draw_watermark(c, width, height)
    draw_header(c, width, height, "Page 1")

    col_gap = 15
    marg_x = 20
    col_w = (width - (2 * marg_x) - col_gap) / 2
    col1_x = marg_x
    col2_x = marg_x + col_w + col_gap
    
    cursor_y = height - 160
    
    # --- Q1 & Q2 ---
    h_row1 = 110
    draw_question_box(c, col1_x, cursor_y - h_row1, col_w, h_row1, "प्र. 1: शब्दों में लिखें (Words)", "[5 अंक]")
    
    c.setFillColor(colors.black) # FIX: Ensure black text
    c.setFont(FONT_NAME, 11)
    q1_y = cursor_y - 20
    items_q1 = ["(a) 75 : ________________", "(b) 89 : ________________", "(c) 46 : ________________", "(d) 99 : ________________", "(e) 29 : ________________"]
    for item in items_q1:
        q1_y -= 16
        c.drawString(col1_x + 10, q1_y, item)

    draw_question_box(c, col2_x, cursor_y - h_row1, col_w, h_row1, "प्र. 2: स्थानीय मान (Place Value)", "[5 अंक]")
    c.setFillColor(colors.black)
    items_q2 = ["(a) 540 में 5 का मान: _______", "(b) 892 में 9 का मान: _______", "(c) 1000 में 1 का मान: ______", "(d) 607 में 7 का मान: _______", "(e) 4550 में 0 का मान: ______"]
    q2_y = cursor_y - 20
    for item in items_q2:
        q2_y -= 16
        c.drawString(col2_x + 10, q2_y, item)

    cursor_y -= (h_row1 + 10)

    # --- Q3 Addition ---
    h_math = 75
    draw_question_box(c, col1_x, cursor_y - h_math, width - 40, h_math, "प्र. 3: जोड़ें (Addition)", "[5 अंक]")
    
    sum_spacing = (width - 40) / 4
    q3_x = col1_x + 40
    q3_y = cursor_y - 45
    
    draw_vertical_math(c, q3_x, q3_y, "4230", "+", "1540")
    draw_vertical_math(c, q3_x + sum_spacing, q3_y, "6525", "+", "2354")
    draw_vertical_math(c, q3_x + sum_spacing*2, q3_y, "5005", "+", "4990")
    draw_vertical_math(c, q3_x + sum_spacing*3, q3_y, "1234", "+", "4321")

    cursor_y -= (h_math + 10)

    # --- Q4 Subtraction ---
    draw_question_box(c, col1_x, cursor_y - h_math, width - 40, h_math, "प्र. 4: घटाएँ (Subtraction)", "[5 अंक]")
    q4_y = cursor_y - 45
    draw_vertical_math(c, q3_x, q4_y, "8956", "-", "4523")
    draw_vertical_math(c, q3_x + sum_spacing, q4_y, "5640", "-", "2310")
    draw_vertical_math(c, q3_x + sum_spacing*2, q4_y, "9000", "-", "1000")
    draw_vertical_math(c, q3_x + sum_spacing*3, q4_y, "7550", "-", "2550")

    cursor_y -= (h_math + 10)

    # --- Q5 & Q6 ---
    h_row3 = 120
    draw_question_box(c, col1_x, cursor_y - h_row3, col_w, h_row3, "प्र. 5: विस्तारित रूप (Expanded Form)", "[5 अंक]")
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 10)
    q5_y = cursor_y - 20
    expanded_qs = [
        "(a) 5426 = 5000 + 400 + 20 + 6",
        "(b) 3250 = ____ + ____ + ____ + 0",
        "(c) 7085 = ____ + 00 + ____ + 5",
        "(d) 1200 = 1000 + ____ + 00 + 0",
        "(e) 4040 = ____ + 0 + ____ + 0"
    ]
    for item in expanded_qs:
        q5_y -= 18
        c.drawString(col1_x + 8, q5_y, item)

    draw_question_box(c, col2_x, cursor_y - h_row3, col_w, h_row3, "प्र. 6: गुणा करें (Multiply)", "[5 अंक]")
    mul_spacing = col_w / 4
    qm_x = col2_x + 15
    qm_y = cursor_y - 60
    draw_vertical_math(c, qm_x, qm_y, "24", "x", "2")
    draw_vertical_math(c, qm_x + mul_spacing + 10, qm_y, "33", "x", "3")
    draw_vertical_math(c, qm_x + (mul_spacing+10)*2, qm_y, "12", "x", "4")
    draw_vertical_math(c, qm_x + (mul_spacing+10)*3, qm_y, "40", "x", "2")

    cursor_y -= (h_row3 + 10)

    # --- Q7 & Q8 ---
    h_row4 = 90
    draw_question_box(c, col1_x, cursor_y - h_row4, col_w, h_row4, "प्र. 7: चिन्ह लगाएँ (<, >, =)", "[5 अंक]")
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 11)
    q7_y = cursor_y - 35
    c.drawString(col1_x + 10, q7_y, "4500 [___] 5400")
    c.drawString(col1_x + 140, q7_y, "8000 [___] 8000")
    q7_y -= 20
    c.drawString(col1_x + 10, q7_y, "2020 [___] 2002")
    c.drawString(col1_x + 140, q7_y, "500 [___] 50")
    q7_y -= 20
    c.drawString(col1_x + 10, q7_y, "1010 [___] 1001")

    draw_question_box(c, col2_x, cursor_y - h_row4, col_w, h_row4, "प्र. 8: भाग दें (Division)", "[5 अंक]")
    c.setFillColor(colors.black)
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
    draw_header(c, width, height, "Page 2")
    
    cursor_y = height - 90
    
    # --- Q9 & Q10 ---
    h_p2_row1 = 85
    draw_question_box(c, col1_x, cursor_y - h_p2_row1, col_w, h_p2_row1, "प्र. 9: बढ़ते क्रम (Increasing Order)", "[5 अंक]")
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 10)
    c.drawString(col1_x + 10, cursor_y - 30, "(a) 500, 200, 800, 100")
    c.drawString(col1_x + 10, cursor_y - 45, "     → ___, ___, ___, ___")
    c.drawString(col1_x + 10, cursor_y - 60, "(b) 10, 50, 30, 20, 40")
    c.drawString(col1_x + 10, cursor_y - 75, "     → ___, ___, ___, ___, ___")

    draw_question_box(c, col2_x, cursor_y - h_p2_row1, col_w, h_p2_row1, "प्र. 10: घटते क्रम (Decreasing Order)", "[5 अंक]")
    c.setFillColor(colors.black)
    c.drawString(col2_x + 10, cursor_y - 30, "(a) 45, 90, 12, 65")
    c.drawString(col2_x + 10, cursor_y - 45, "     → ___, ___, ___, ___")
    c.drawString(col2_x + 10, cursor_y - 60, "(b) 88, 11, 55, 33, 77")
    c.drawString(col2_x + 10, cursor_y - 75, "     → ___, ___, ___, ___, ___")

    cursor_y -= (h_p2_row1 + 10)

    # --- Q11 & Q12 ---
    h_p2_row2 = 100
    draw_question_box(c, col1_x, cursor_y - h_p2_row2, col_w, h_p2_row2, "प्र. 11: पहले और बाद की संख्या", "[5 अंक]")
    c.setFillColor(colors.black)
    q11_y = cursor_y - 30
    c.drawString(col1_x + 10, q11_y, "(a) ____ ← 500 → ____")
    c.drawString(col1_x + 10, q11_y - 20, "(b) ____ ← 1000 → ____")
    c.drawString(col1_x + 10, q11_y - 40, "(c) 99 के बाद: ________")
    c.drawString(col1_x + 10, q11_y - 60, "(d) 50 से पहले: ________")

    draw_question_box(c, col2_x, cursor_y - h_p2_row2, col_w, h_p2_row2, "प्र. 12: पहाड़ा और पैटर्न (Tables)", "[5 अंक]")
    c.setFillColor(colors.black)
    q12_y = cursor_y - 30
    c.drawString(col2_x + 10, q12_y, "(a) 12 का पहाड़ा: 12, 24, ___, 48")
    c.drawString(col2_x + 10, q12_y - 20, "(b) 15 का पहाड़ा: 15, 30, ___, 60")
    c.drawString(col2_x + 10, q12_y - 40, "(c) 2 का पहाड़ा: 2, 4, 6, ___, 10")
    c.drawString(col2_x + 10, q12_y - 60, "(d) 10, 20, 30, ___, 50")

    cursor_y -= (h_p2_row2 + 10)

    # --- Q13 & Q14 ---
    h_p2_row3 = 120
    draw_question_box(c, col1_x, cursor_y - h_p2_row3, col_w, h_p2_row3, "प्र. 13: हल करें (Word Problem)", "[5 अंक]")
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 10)
    c.drawString(col1_x + 5, cursor_y - 30, "राम के पास 2500 रुपये, श्याम के पास")
    c.drawString(col1_x + 5, cursor_y - 45, "1200 रुपये और मोहन के पास 100 रुपये हैं।")
    c.drawString(col1_x + 5, cursor_y - 60, "तीनों के पास कुल कितने रुपये हैं?")
    c.setLineWidth(1)
    c.line(col1_x + 5, cursor_y - 90, col1_x + col_w - 5, cursor_y - 90)
    c.drawString(col1_x + 5, cursor_y - 105, "उत्तर:")

    draw_question_box(c, col2_x, cursor_y - h_p2_row3, col_w, h_p2_row3, "प्र. 14: हल करें (Word Problem)", "[5 अंक]")
    c.setFillColor(colors.black)
    c.drawString(col2_x + 5, cursor_y - 30, "एक स्कूल में 4500 बच्चे हैं। आज 500")
    c.drawString(col2_x + 5, cursor_y - 45, "बच्चे नहीं आए (Absent)। बताइये आज")
    c.drawString(col2_x + 5, cursor_y - 60, "स्कूल में कितने बच्चे उपस्थित हैं?")
    c.line(col2_x + 5, cursor_y - 90, col2_x + col_w - 5, cursor_y - 90)
    c.drawString(col2_x + 5, cursor_y - 105, "उत्तर:")

    cursor_y -= (h_p2_row3 + 10)

    # --- Q15 & Q16 ---
    h_p2_row4 = 110
    draw_question_box(c, col1_x, cursor_y - h_p2_row4, col_w, h_p2_row4, "प्र. 15: पैटर्न पूरा करें", "[5 अंक]")
    c.setFillColor(colors.black)
    q15_y = cursor_y - 30
    c.drawString(col1_x + 10, q15_y, "(a) 100, 200, 300, _____, 500")
    c.drawString(col1_x + 10, q15_y - 18, "(b) 5, 10, 15, _____, 25")
    c.drawString(col1_x + 10, q15_y - 36, "(c) A, B, C, _____, E")
    c.drawString(col1_x + 10, q15_y - 54, "(d) 2, 4, 8, 16, ______")
    c.drawString(col1_x + 10, q15_y - 72, "(e) 11, 22, 33, _____, 55")

    draw_question_box(c, col2_x, cursor_y - h_p2_row4, col_w, h_p2_row4, "प्र. 16: दिमागी कसरत (Mental Math)", "[5 अंक]")
    c.setFillColor(colors.black)
    q16_y = cursor_y - 30
    c.drawString(col2_x + 10, q16_y, "(a) 100 + 50 = ______")
    c.drawString(col2_x + 10, q16_y - 18, "(b) 500 में 1 जोड़ने पर? ______")
    c.drawString(col2_x + 10, q16_y - 36, "(c) 1 सप्ताह में कितने दिन? ______")
    c.drawString(col2_x + 10, q16_y - 54, "(d) 20 के 3 नोट = ______ रु")
    c.drawString(col2_x + 10, q16_y - 72, "(e) 10 में से 10 गया = ______")

    # Good Luck
    c.setFont(FONT_NAME, 12)
    c.drawCentredString(width/2, cursor_y - h_p2_row4 - 30, "*** परीक्षा समाप्त (Good Luck) ***")
    
    draw_footer(c, width, 2)
    c.save()
    print(f"PDF Created Successfully: {OUTPUT_FILENAME}")

if __name__ == "__main__":
    create_paper()