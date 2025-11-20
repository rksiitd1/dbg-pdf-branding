import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- CONFIGURATION ---
OUTPUT_FILENAME = "Class_1_Exam_Paper.pdf"
LOGO_LEFT = "DBG-logo.png"
LOGO_RIGHT = "DBM-logo.png"
WATERMARK_IMG = "DBG-logo.png"

# Try to locate a Hindi-supporting font (Windows default: Nirmala UI or Arial Unicode)
# If you see boxes instead of Hindi text, ensure this path points to a valid Unicode font.
FONT_PATH = "C:\\Windows\\Fonts\\Nirmala.ttf" 
FONT_NAME = "Nirmala"

if not os.path.exists(FONT_PATH):
    # Fallback for systems without Nirmala (Results in no Hindi)
    FONT_PATH = "C:\\Windows\\Fonts\\arial.ttf"
    FONT_NAME = "Arial"

# --- DATA FOR QUESTIONS ---
# Page 1 Content
Q1_DATA = ["(a) 75 : _________", "(b) 89 : _________", "(c) 46 : _________", "(d) 99 : _________", "(e) 29 : _________"]
Q2_DATA = ["(a) 540 में 5 का मान: _____", "(b) 892 में 9 का मान: _____", "(c) 1000 में 1 का मान: ____", "(d) 607 में 7 का मान: _____", "(e) 4550 में 0 का मान: ____"]
Q3_SUMS = [("4230", "+ 1540"), ("6525", "+ 2354"), ("5005", "+ 4990"), ("1234", "+ 4321")]
Q4_SUMS = [("8956", "- 4523"), ("5640", "- 2310"), ("9000", "- 1000"), ("7550", "- 2550")]
Q5_DATA = ["(a) 5426 = 5000 + 400 + 20 + 6", "(b) 3250 = ____ + ____ + ____ + 0", "(c) 7085 = ____ + 00 + ____ + 5", "(d) 1200 = 1000 + ____ + 00 + 0", "(e) 4040 = ____ + 0 + ____ + 0"]
Q6_SUMS = [("24", "x 2"), ("33", "x 3"), ("12", "x 4"), ("40", "x 2")]
Q7_DATA = [("4500", "5400"), ("8000", "8000"), ("2020", "2002"), ("500", "50"), ("1010", "1001")]
Q8_DATA = ["(a) 20 ÷ 2 = ____", "(b) 15 ÷ 3 = ____", "(c) 16 ÷ 4 = ____", "(d) 10 ÷ 5 = ____", "(e) 30 ÷ 3 = ____"]

# Page 2 Content
Q9_DATA = ["(a) 500, 200, 800, 100", "    -> ____, ____, ____, ____", "(b) 10, 50, 30, 20, 40", "    -> ____, ____, ____, ____, ____"]
Q10_DATA = ["(a) 45, 90, 12, 65", "    -> ____, ____, ____, ____", "(b) 88, 11, 55, 33, 77", "    -> ____, ____, ____, ____, ____"]
Q11_DATA = ["(a) ____ <- 500 -> ____", "(b) ____ <- 1000 -> ____", "(c) 99 के बाद: ____", "(d) 50 से पहले: ____"]
Q12_DATA = ["(a) 12 का पहाड़ा: 12, 24, ___, 48", "(b) 15 का पहाड़ा: 15, 30, ___, 60", "(c) 2 का पहाड़ा: 2, 4, 6, ___, 10", "(d) 10, 20, 30, ___, 50"]


def draw_header(c, width, height):
    """Draws Logos, Title, and Student Details"""
    # 1. Logos
    logo_size = 60
    if os.path.exists(LOGO_LEFT):
        c.drawImage(LOGO_LEFT, 20, height - 75, width=logo_size, height=logo_size, mask='auto')
    if os.path.exists(LOGO_RIGHT):
        c.drawImage(LOGO_RIGHT, width - 80, height - 75, width=logo_size, height=logo_size, mask='auto')

    # 2. Main Title
    c.setFont(FONT_NAME, 24)
    c.drawCentredString(width / 2, height - 50, "DBG GURUKULAM")

    # 3. Sub Header Line 1
    c.setFont(FONT_NAME, 12)
    c.drawCentredString(width / 2, height - 75, "कक्षा : 1 (First)   विषय: गणित (Maths)   समय: 2 घंटे")
    
    # 4. Student Details Box
    c.setLineWidth(1)
    y_pos = height - 105
    c.rect(20, y_pos, width - 40, 25)
    c.setFont(FONT_NAME, 10)
    c.drawString(30, y_pos + 8, "नाम: _________________________   रोल नं: _______   दिनांक: _______")
    
    # 5. Max Marks Line
    c.drawString(width - 150, y_pos - 15, "पूर्णांक (Max Marks): 80")
    
    # Separator Line
    c.line(20, y_pos - 20, width - 20, y_pos - 20)

def draw_footer(c, width):
    """Draws Branding Footer"""
    footer_y = 30
    c.setLineWidth(0.5)
    c.line(20, footer_y + 10, width - 20, footer_y + 10)
    
    c.setFont("Helvetica", 9)
    c.drawString(30, footer_y, f"Page {c.getPageNumber()}")
    c.drawCentredString(width / 2, footer_y, "Shri Classes & DBG Gurukulam (by IITian Golu Sir)")
    c.setFillColor(colors.blue)
    c.drawRightString(width - 30, footer_y, "https://dbggurukulam.com")
    c.setFillColor(colors.black)

def draw_watermark(c, width, height):
    """Draws faded watermark"""
    if os.path.exists(WATERMARK_IMG):
        c.saveState()
        c.setFillAlpha(0.15) # 15% visibility (very faded)
        wm_size = 300
        c.drawImage(WATERMARK_IMG, (width - wm_size)/2, (height - wm_size)/2, width=wm_size, height=wm_size, mask='auto')
        c.restoreState()

def draw_box(c, x, y, w, h, title, marks):
    """Draws the rounded box for a question"""
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, 4, stroke=1, fill=0)
    
    # Title Bar
    c.saveState()
    c.setFillColor(colors.lightgrey)
    # Clip header path if we wanted rounded top corners only, but simple rect is fine for now
    # Draw Text
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 10)
    c.drawString(x + 5, y + h - 14, title)
    c.drawRightString(x + w - 5, y + h - 14, marks)
    # Separator line below title
    c.line(x, y + h - 18, x + w, y + h - 18)
    c.restoreState()

def create_pdf():
    # Register Font
    try:
        pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))
        print(f"Font registered: {FONT_NAME}")
    except Exception as e:
        print(f"Font Error: {e}. Ensure {FONT_PATH} exists.")
        return

    c = canvas.Canvas(OUTPUT_FILENAME, pagesize=A4)
    width, height = A4
    
    # ================= PAGE 1 =================
    draw_watermark(c, width, height)
    draw_header(c, width, height)
    
    # Layout Config
    col1_x = 20
    col2_x = width / 2 + 10
    col_w = (width / 2) - 30
    start_y = height - 150
    
    # --- Q1: Words (Left) ---
    h_q1 = 110
    draw_box(c, col1_x, start_y - h_q1, col_w, h_q1, "प्र. 1: शब्दों में लिखें (Words)", "[5 अंक]")
    c.setFont(FONT_NAME, 10)
    line_h = 18
    curr_y = start_y - 40
    for line in Q1_DATA:
        c.drawString(col1_x + 10, curr_y, line)
        curr_y -= line_h

    # --- Q2: Place Value (Right) ---
    draw_box(c, col2_x, start_y - h_q1, col_w, h_q1, "प्र. 2: स्थानीय मान (Place Value)", "[5 अंक]")
    curr_y = start_y - 40
    for line in Q2_DATA:
        c.drawString(col2_x + 10, curr_y, line)
        curr_y -= line_h

    # --- Q3: Addition (Full Width) ---
    y_q3 = start_y - h_q1 - 10
    h_q3 = 70
    draw_box(c, col1_x, y_q3 - h_q3, width - 40, h_q3, "प्र. 3: जोड़ें (Addition)", "[5 अंक]")
    # Draw 4 sums
    spacing = (width - 60) / 4
    curr_x = col1_x + 30
    c.setFont(FONT_NAME, 12)
    for top, bot in Q3_SUMS:
        c.drawString(curr_x, y_q3 - 35, top)
        c.drawString(curr_x, y_q3 - 50, bot)
        c.line(curr_x, y_q3 - 52, curr_x + 40, y_q3 - 52) # Underline
        curr_x += spacing

    # --- Q4: Subtraction (Full Width) ---
    y_q4 = y_q3 - h_q3 - 10
    h_q4 = 70
    draw_box(c, col1_x, y_q4 - h_q4, width - 40, h_q4, "प्र. 4: घटाएँ (Subtraction)", "[5 अंक]")
    curr_x = col1_x + 30
    for top, bot in Q4_SUMS:
        c.drawString(curr_x, y_q4 - 35, top)
        c.drawString(curr_x, y_q4 - 50, bot)
        c.line(curr_x, y_q4 - 52, curr_x + 40, y_q4 - 52)
        curr_x += spacing

    # --- Q5: Expanded Form (Left) ---
    y_q5 = y_q4 - h_q4 - 10
    h_q5 = 110
    draw_box(c, col1_x, y_q5 - h_q5, col_w, h_q5, "प्र. 5: विस्तारित रूप (Expanded)", "[5 अंक]")
    c.setFont(FONT_NAME, 9) # Slightly smaller to fit
    curr_y = y_q5 - 35
    for line in Q5_DATA:
        c.drawString(col1_x + 5, curr_y, line)
        curr_y -= line_h

    # --- Q6: Multiply (Right) ---
    draw_box(c, col2_x, y_q5 - h_q5, col_w, h_q5, "प्र. 6: गुणा करें (Multiply)", "[5 अंक]")
    spacing_mul = col_w / 4
    curr_x = col2_x + 20
    c.setFont(FONT_NAME, 12)
    for top, bot in Q6_SUMS:
        c.drawString(curr_x, y_q5 - 40, top)
        c.drawString(curr_x, y_q5 - 55, bot)
        c.line(curr_x - 5, y_q5 - 57, curr_x + 25, y_q5 - 57)
        curr_x += spacing_mul + 10

    # --- Q7: Signs (Left) ---
    y_q7 = y_q5 - h_q5 - 10
    h_q7 = 80
    draw_box(c, col1_x, y_q7 - h_q7, col_w, h_q7, "प्र. 7: चिन्ह लगाएँ (<, >, =)", "[5 अंक]")
    c.setFont(FONT_NAME, 10)
    curr_y = y_q7 - 35
    # Manually laying out the boxes for signs
    for left, right in Q7_DATA:
        # This is tricky to do dynamically, simplifying layout
        pass 
    # Hardcoding the 3 lines of signs
    c.drawString(col1_x + 10, y_q7 - 35, "4500 [___] 5400")
    c.drawString(col1_x + 110, y_q7 - 35, "8000 [___] 8000")
    c.drawString(col1_x + 10, y_q7 - 55, "2020 [___] 2002")
    c.drawString(col1_x + 110, y_q7 - 55, "500 [___] 50")
    c.drawString(col1_x + 10, y_q7 - 75, "1010 [___] 1001")

    # --- Q8: Division (Right) ---
    draw_box(c, col2_x, y_q7 - h_q7, col_w, h_q7, "प्र. 8: भाग दें (Division)", "[5 अंक]")
    curr_y = y_q7 - 30
    c.setFont(FONT_NAME, 10)
    # 2 columns inside the box
    c.drawString(col2_x + 10, curr_y, "(a) 20 / 2 = ___")
    c.drawString(col2_x + 110, curr_y, "(b) 15 / 3 = ___")
    curr_y -= 20
    c.drawString(col2_x + 10, curr_y, "(c) 16 / 4 = ___")
    c.drawString(col2_x + 110, curr_y, "(d) 10 / 5 = ___")
    curr_y -= 20
    c.drawString(col2_x + 10, curr_y, "(e) 30 / 3 = ___")

    draw_footer(c, width)
    c.showPage()

    # ================= PAGE 2 =================
    draw_watermark(c, width, height)
    # Simple Header for Page 2
    c.setFont(FONT_NAME, 14)
    c.drawCentredString(width / 2, height - 40, "DBG GURUKULAM")
    c.setFont(FONT_NAME, 10)
    c.drawCentredString(width / 2, height - 60, "गणित - भाग 2 (Page 2)")
    c.line(20, height - 70, width - 20, height - 70)
    
    start_y = height - 90
    
    # --- Q9: Increasing (Left) ---
    h_q9 = 80
    draw_box(c, col1_x, start_y - h_q9, col_w, h_q9, "प्र. 9: बढ़ते क्रम (Increasing)", "[5 अंक]")
    curr_y = start_y - 30
    for line in Q9_DATA:
        c.drawString(col1_x + 10, curr_y, line)
        curr_y -= 15

    # --- Q10: Decreasing (Right) ---
    draw_box(c, col2_x, start_y - h_q9, col_w, h_q9, "प्र. 10: घटते क्रम (Decreasing)", "[5 अंक]")
    curr_y = start_y - 30
    for line in Q10_DATA:
        c.drawString(col2_x + 10, curr_y, line)
        curr_y -= 15
        
    # --- Q11: Before/After (Left) ---
    y_q11 = start_y - h_q9 - 10
    h_q11 = 90
    draw_box(c, col1_x, y_q11 - h_q11, col_w, h_q11, "प्र. 11: पहले और बाद (Before/After)", "[5 अंक]")
    curr_y = y_q11 - 30
    for line in Q11_DATA:
        c.drawString(col1_x + 10, curr_y, line)
        curr_y -= 18

    # --- Q12: Tables (Right) ---
    draw_box(c, col2_x, y_q11 - h_q11, col_w, h_q11, "प्र. 12: पहाड़ा और पैटर्न (Tables)", "[5 अंक]")
    curr_y = y_q11 - 30
    for line in Q12_DATA:
        c.drawString(col2_x + 10, curr_y, line)
        curr_y -= 18

    # --- Q13: Word Prob (Left) ---
    y_q13 = y_q11 - h_q11 - 10
    h_q13 = 100
    draw_box(c, col1_x, y_q13 - h_q13, col_w, h_q13, "प्र. 13: हल करें (Word Problem)", "[5 अंक]")
    c.setFont(FONT_NAME, 9)
    text = "राम के पास 2500 रुपये, श्याम के पास 1200\nरुपये और मोहन के पास 100 रुपये हैं।\nतीनों के पास कुल कितने रुपये हैं?"
    t = c.beginText(col1_x + 5, y_q13 - 30)
    t.setFont(FONT_NAME, 9)
    t.textLines(text)
    c.drawText(t)
    c.drawString(col1_x + 5, y_q13 - 80, "उत्तर: _________________")

    # --- Q14: Word Prob (Right) ---
    draw_box(c, col2_x, y_q13 - h_q13, col_w, h_q13, "प्र. 14: हल करें (Word Problem)", "[5 अंक]")
    text = "एक स्कूल में 4500 बच्चे हैं। आज 500\nबच्चे नहीं आए (Absent)। बताइये आज\nस्कूल में कितने बच्चे उपस्थित हैं?"
    t = c.beginText(col2_x + 5, y_q13 - 30)
    t.setFont(FONT_NAME, 9)
    t.textLines(text)
    c.drawText(t)
    c.drawString(col2_x + 5, y_q13 - 80, "उत्तर: _________________")

    # --- Q15: Patterns (Left) ---
    y_q15 = y_q13 - h_q13 - 10
    h_q15 = 100
    draw_box(c, col1_x, y_q15 - h_q15, col_w, h_q15, "प्र. 15: पैटर्न पूरा करें", "[5 अंक]")
    c.drawString(col1_x + 5, y_q15 - 30, "(a) 100, 200, 300, ____, 500")
    c.drawString(col1_x + 5, y_q15 - 45, "(b) 5, 10, 15, ____, 25")
    c.drawString(col1_x + 5, y_q15 - 60, "(c) A, B, C, ____, E")
    c.drawString(col1_x + 5, y_q15 - 75, "(d) 2, 4, 8, 16, ____")
    
    # --- Q16: Mental Math (Right) ---
    draw_box(c, col2_x, y_q15 - h_q15, col_w, h_q15, "प्र. 16: दिमागी कसरत (Mental Math)", "[5 अंक]")
    c.drawString(col2_x + 5, y_q15 - 30, "(a) 100 + 50 = ____")
    c.drawString(col2_x + 5, y_q15 - 45, "(b) 500 में 1 जोड़ने पर? ____")
    c.drawString(col2_x + 5, y_q15 - 60, "(c) 1 सप्ताह में कितने दिन? ____")
    c.drawString(col2_x + 5, y_q15 - 75, "(d) 20 के 3 नोट = ____ रु")

    # Footer
    c.setFont(FONT_NAME, 12)
    c.drawCentredString(width / 2, 70, "*** परीक्षा समाप्त (Good Luck) ***")
    draw_footer(c, width)
    
    c.save()
    print(f"PDF Generated: {OUTPUT_FILENAME}")

if __name__ == "__main__":
    create_pdf()