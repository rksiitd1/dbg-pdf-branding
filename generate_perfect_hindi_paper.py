import os
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from PIL import Image, ImageDraw, ImageFont

# --- CONFIGURATION ---
OUTPUT_FILENAME = "Class_1_Exam_Perfect_Hindi.pdf"
LOGO_LEFT = "DBG-logo.png"
LOGO_RIGHT = "DBM-logo.png"
WATERMARK_IMG = "DBG-logo.png"

# --- COLORS ---
COLOR_PRIMARY = "#154c79"   # Navy Blue
COLOR_ACCENT = "#e08d3c"    # Gold/Orange
COLOR_BG_HEADER = "#f4f6f9" # Light Grey
COLOR_TEXT = "#000000"      # Black

# --- FONT CONFIGURATION ---
# We use PIL ImageFont, which renders Hindi perfectly on Windows
FONT_PATH = "C:\\Windows\\Fonts\\Nirmala.ttf" 
# Fallback if Nirmala doesn't exist
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:\\Windows\\Fonts\\arial.ttf" 

# --- THE MAGIC ENGINE: TEXT TO IMAGE ---
def get_hindi_image(text, fontsize, color_hex="#000000", bold=False):
    """
    Renders Hindi text to a high-res transparent image using Pillow.
    This guarantees perfect Sanyuktakshars (half-letters).
    """
    if not text: return None, 0, 0

    # 1. Load Font (Scale up 4x for high resolution crispness)
    scale_factor = 4
    try:
        font = ImageFont.truetype(FONT_PATH, int(fontsize * scale_factor))
    except:
        font = ImageFont.load_default()

    # 2. Measure Text Size
    # getbbox returns (left, top, right, bottom)
    dummy_img = Image.new('RGBA', (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    
    # Add some padding to avoid cutting off matras
    w += 20 
    h += 20

    # 3. Draw Text on Transparent Image
    img = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Convert Hex color to RGB tuple
    c_code = color_hex.lstrip('#')
    rgb = tuple(int(c_code[i:i+2], 16) for i in (0, 2, 4))
    
    # Draw text (adjusting for padding)
    draw.text((10, 5), text, font=font, fill=rgb)
    
    # 4. Return Image and Scaled Dimensions for PDF
    final_w = w / scale_factor
    final_h = h / scale_factor
    return img, final_w, final_h

def draw_hindi(c, x, y, text, fontsize=10, color="#000000", align="left"):
    """
    Wrapper to place the Hindi Image onto the PDF Canvas.
    align: 'left', 'center', 'right'
    """
    img, w, h = get_hindi_image(text, fontsize, color)
    if img is None: return

    # Adjust X based on alignment
    if align == "center":
        x_pos = x - (w / 2)
    elif align == "right":
        x_pos = x - w
    else:
        x_pos = x

    # Adjust Y to align somewhat with baseline (Images draw top-down)
    # We shift up slightly because the image box includes ascenders
    y_pos = y - (h * 0.75) 

    # Convert PIL Image to ReportLab ImageReader
    img_reader = ImageReader(img)
    
    # Draw on Canvas
    c.drawImage(img_reader, x_pos, y_pos, width=w, height=h, mask='auto')

# --- DRAWING COMPONENTS ---

def draw_modern_header(c, width, height, page_num):
    c.saveState()
    
    # Header Background
    header_h = 110
    c.setFillColor(HexColor(COLOR_BG_HEADER))
    c.rect(0, height - header_h, width, header_h, fill=1, stroke=0)
    c.setStrokeColor(HexColor(COLOR_PRIMARY))
    c.setLineWidth(3)
    c.line(0, height - header_h, width, height - header_h)
    
    # Logos
    logo_size = 75
    logo_y = height - 95
    if os.path.exists(LOGO_LEFT):
        c.drawImage(LOGO_LEFT, 25, logo_y, width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)
    if os.path.exists(LOGO_RIGHT):
        c.drawImage(LOGO_RIGHT, width - 25 - logo_size, logo_y, width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)

    # Main Title (English is fine in standard font)
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(HexColor(COLOR_PRIMARY))
    c.drawCentredString(width/2, height - 50, "DBG GURUKULAM")
    
    if page_num == 1:
        # Sub Header (Hindi Mixed)
        info_text = "कक्षा : 1 (First)   |   विषय: गणित (Maths)   |   समय: 2 घंटे"
        draw_hindi(c, width/2, height - 75, info_text, 12, "#000000", align="center")
        
        # Student Details
        strip_y = height - 145
        c.setStrokeColor(HexColor("#d1d5db"))
        c.setLineWidth(1)
        c.roundRect(20, strip_y, width - 40, 30, 5, stroke=1, fill=0)
        
        details = "नाम: ___________________________   रोल नं: _________   दिनांक: _________"
        draw_hindi(c, 35, strip_y + 10, details, 10, "#000000")
        
        # Marks
        marks_y = strip_y - 25
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor(COLOR_PRIMARY))
        c.drawString(20, marks_y, "Total Questions: 16")
        draw_hindi(c, width - 20, marks_y + 2, "पूर्णांक (Max Marks): 80", 10, COLOR_PRIMARY, align="right")
        
        return marks_y - 15
    else:
        draw_hindi(c, width/2, height - 75, "गणित - भाग 2 (Page 2)", 12, "#000000", align="center")
        return height - 120
    c.restoreState()

def draw_card(c, x, y, w, h, title, marks, accent_color=COLOR_PRIMARY):
    c.saveState()
    radius = 8
    
    # Shadow
    c.setFillColor(colors.Color(0.9, 0.9, 0.9))
    c.roundRect(x + 3, y - 3, w, h, radius, fill=1, stroke=0)
    
    # Box
    c.setFillColor(colors.white)
    c.setStrokeColor(HexColor("#d1d5db"))
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    
    # Header Bar
    header_h = 24
    p = c.beginPath()
    p.roundRect(x, y, w, h, radius)
    c.clipPath(p, stroke=0)
    
    c.setFillColor(HexColor(accent_color))
    c.rect(x, y + h - header_h, w, header_h, fill=1, stroke=0)
    
    # Title Text (Hindi Image)
    draw_hindi(c, x + 10, y + h - 17, title, 10, "#FFFFFF") # White Text
    
    # Marks (Hindi Image)
    draw_hindi(c, x + w - 10, y + h - 17, marks, 10, "#FFFFFF", align="right")
    
    c.restoreState()

def draw_math_vertical(c, x, y, num1, op, num2):
    c.saveState()
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(x + 40, y, num1)
    c.drawRightString(x + 40, y - 18, num2)
    c.drawString(x - 5, y - 18, op)
    c.setLineWidth(1.5)
    c.line(x - 5, y - 24, x + 45, y - 24)
    c.restoreState()

def draw_watermark(c, width, height):
    if os.path.exists(WATERMARK_IMG):
        c.saveState()
        c.setFillAlpha(0.08)
        wm_size = 450
        c.drawImage(WATERMARK_IMG, (width - wm_size)/2, (height - wm_size)/2, 
                    width=wm_size, height=wm_size, mask='auto', preserveAspectRatio=True)
        c.restoreState()

def draw_footer(c, width, page_num):
    c.saveState()
    y = 20
    c.setStrokeColor(HexColor(COLOR_ACCENT))
    c.setLineWidth(2)
    c.line(0, y + 15, width, y + 15)
    
    # Circle Page Num
    c.setFillColor(HexColor(COLOR_PRIMARY))
    c.circle(30, y + 6, 12, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(30, y + 3, str(page_num))
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 9)
    c.drawCentredString(width/2, y + 3, "Shri Classes & DBG Gurukulam (by IITian Golu Sir)")
    
    c.setFillColor(HexColor(COLOR_PRIMARY))
    c.drawRightString(width - 20, y + 3, "https://dbggurukulam.com")
    c.restoreState()

# --- MAIN CONTENT ---

def create_paper():
    c = canvas.Canvas(OUTPUT_FILENAME, pagesize=A4)
    width, height = A4
    
    # ================= PAGE 1 =================
    draw_watermark(c, width, height)
    cursor_y = draw_modern_header(c, width, height, 1)
    
    # Layout
    MARGIN = 20
    GAP = 15
    col_width = (width - (3 * MARGIN)) / 2
    col1 = MARGIN
    col2 = MARGIN + col_width + MARGIN
    
    # Q1 & Q2
    h_row1 = 120
    draw_card(c, col1, cursor_y - h_row1, col_width, h_row1, "प्र. 1: शब्दों में लिखें (Words)", "[5 अंक]")
    for i, q in enumerate(["(a) 75 :", "(b) 89 :", "(c) 46 :", "(d) 99 :", "(e) 29 :"]):
        y_pos = cursor_y - 35 - (i * 18)
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        c.drawString(col1 + 10, y_pos, q)
        c.setLineWidth(0.5)
        c.setStrokeColor(colors.grey)
        c.line(col1 + 50, y_pos - 2, col1 + col_width - 10, y_pos - 2)

    draw_card(c, col2, cursor_y - h_row1, col_width, h_row1, "प्र. 2: स्थानीय मान (Place Value)", "[5 अंक]")
    qs_q2 = ["(a) 540 में 5 का मान:", "(b) 892 में 9 का मान:", "(c) 1000 में 1 का मान:", "(d) 607 में 7 का मान:", "(e) 4550 में 0 का मान:"]
    for i, q in enumerate(qs_q2):
        y_pos = cursor_y - 35 - (i * 18)
        draw_hindi(c, col2 + 10, y_pos, q, 10)
        c.setLineWidth(0.5)
        c.setStrokeColor(colors.grey)
        c.line(col2 + 125, y_pos - 2, col2 + col_width - 10, y_pos - 2)

    cursor_y -= (h_row1 + GAP)

    # Q3 & Q4 (Math Cards)
    h_math = 80
    draw_card(c, col1, cursor_y - h_math, width - 40, h_math, "प्र. 3: जोड़ें (Addition)", "[5 अंक]", COLOR_ACCENT)
    math_y = cursor_y - 55
    spacing = (width - 80) / 4
    start_x = col1 + 50
    draw_math_vertical(c, start_x, math_y, "4230", "+", "1540")
    draw_math_vertical(c, start_x + spacing, math_y, "6525", "+", "2354")
    draw_math_vertical(c, start_x + spacing*2, math_y, "5005", "+", "4990")
    draw_math_vertical(c, start_x + spacing*3, math_y, "1234", "+", "4321")

    cursor_y -= (h_math + GAP)

    draw_card(c, col1, cursor_y - h_math, width - 40, h_math, "प्र. 4: घटाएँ (Subtraction)", "[5 अंक]", COLOR_ACCENT)
    math_y = cursor_y - 55
    draw_math_vertical(c, start_x, math_y, "8956", "-", "4523")
    draw_math_vertical(c, start_x + spacing, math_y, "5640", "-", "2310")
    draw_math_vertical(c, start_x + spacing*2, math_y, "9000", "-", "1000")
    draw_math_vertical(c, start_x + spacing*3, math_y, "7550", "-", "2550")

    cursor_y -= (h_math + GAP)

    # Q5 & Q6
    h_row3 = 130
    draw_card(c, col1, cursor_y - h_row3, col_width, h_row3, "प्र. 5: विस्तारित रूप (Expanded Form)", "[5 अंक]")
    q5_list = ["(a) 5426 = 5000 + 400 + 20 + 6", "(b) 3250 = ___ + ___ + ___ + 0", "(c) 7085 = ___ + 00 + ___ + 5", "(d) 1200 = 1000 + ___ + 00 + 0", "(e) 4040 = ___ + 0 + ___ + 0"]
    for i, q in enumerate(q5_list):
        c.setFont("Helvetica", 9)
        c.drawString(col1 + 10, cursor_y - 35 - (i*19), q)

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
    draw_hindi(c, col1 + 15, cursor_y - 35, "4500 [  ] 5400", 11)
    draw_hindi(c, col1 + 150, cursor_y - 35, "8000 [  ] 8000", 11)
    draw_hindi(c, col1 + 15, cursor_y - 55, "2020 [  ] 2002", 11)
    draw_hindi(c, col1 + 150, cursor_y - 55, "500 [  ] 50", 11)
    draw_hindi(c, col1 + 15, cursor_y - 75, "1010 [  ] 1001", 11)

    draw_card(c, col2, cursor_y - h_row4, col_width, h_row4, "प्र. 8: भाग दें (Division)", "[5 अंक]")
    c.setFont("Helvetica", 10)
    c.drawString(col2 + 10, cursor_y - 35, "(a) 20 / 2 = ___")
    c.drawString(col2 + 120, cursor_y - 35, "(b) 15 / 3 = ___")
    c.drawString(col2 + 10, cursor_y - 55, "(c) 16 / 4 = ___")
    c.drawString(col2 + 120, cursor_y - 55, "(d) 10 / 5 = ___")
    c.drawString(col2 + 10, cursor_y - 75, "(e) 30 / 3 = ___")

    draw_footer(c, width, 1)
    c.showPage()

    # ================= PAGE 2 =================
    draw_watermark(c, width, height)
    cursor_y = draw_modern_header(c, width, height, 2)
    P2_GAP = 18

    # Q9 & Q10
    h_p2_r1 = 110
    draw_card(c, col1, cursor_y - h_p2_r1, col_width, h_p2_r1, "प्र. 9: बढ़ते क्रम (Increasing Order)", "[5 अंक]")
    draw_hindi(c, col1 + 10, cursor_y - 35, "(a) 500, 200, 800, 100", 10)
    c.setFont("Helvetica", 10)
    c.drawString(col1 + 10, cursor_y - 50, "     -> ____, ____, ____, ____")
    draw_hindi(c, col1 + 10, cursor_y - 70, "(b) 10, 50, 30, 20, 40", 10)
    c.drawString(col1 + 10, cursor_y - 85, "     -> ____, ____, ____, ____, ____")

    draw_card(c, col2, cursor_y - h_p2_r1, col_width, h_p2_r1, "प्र. 10: घटते क्रम (Decreasing Order)", "[5 अंक]")
    draw_hindi(c, col2 + 10, cursor_y - 35, "(a) 45, 90, 12, 65", 10)
    c.drawString(col2 + 10, cursor_y - 50, "     -> ____, ____, ____, ____")
    draw_hindi(c, col2 + 10, cursor_y - 70, "(b) 88, 11, 55, 33, 77", 10)
    c.drawString(col2 + 10, cursor_y - 85, "     -> ____, ____, ____, ____, ____")

    cursor_y -= (h_p2_r1 + P2_GAP)

    # Q11 & Q12
    h_p2_r2 = 110
    draw_card(c, col1, cursor_y - h_p2_r2, col_width, h_p2_r2, "प्र. 11: पहले और बाद की संख्या", "[5 अंक]")
    c.drawString(col1 + 10, cursor_y - 35, "(a) ____ <- 500 -> ____")
    c.drawString(col1 + 10, cursor_y - 55, "(b) ____ <- 1000 -> ____")
    draw_hindi(c, col1 + 10, cursor_y - 75, "(c) 99 के बाद: ________", 10)
    draw_hindi(c, col1 + 10, cursor_y - 95, "(d) 50 से पहले: ________", 10)

    draw_card(c, col2, cursor_y - h_p2_r2, col_width, h_p2_r2, "प्र. 12: पहाड़ा और पैटर्न (Tables)", "[5 अंक]")
    draw_hindi(c, col2 + 10, cursor_y - 35, "(a) 12 का पहाड़ा: 12, 24, ___, 48", 10)
    draw_hindi(c, col2 + 10, cursor_y - 55, "(b) 15 का पहाड़ा: 15, 30, ___, 60", 10)
    draw_hindi(c, col2 + 10, cursor_y - 75, "(c) 2 का पहाड़ा: 2, 4, 6, ___, 10", 10)
    c.drawString(col2 + 10, cursor_y - 95, "(d) 10, 20, 30, ___, 50")

    cursor_y -= (h_p2_r2 + P2_GAP)

    # Q13 & Q14 Word Problems
    h_p2_r3 = 150
    draw_card(c, col1, cursor_y - h_p2_r3, col_width, h_p2_r3, "प्र. 13: हल करें (Word Problem)", "[5 अंक]", COLOR_ACCENT)
    draw_hindi(c, col1 + 10, cursor_y - 40, "राम के पास 2500 रुपये, श्याम के पास", 10)
    draw_hindi(c, col1 + 10, cursor_y - 60, "1200 रुपये और मोहन के पास 100 रुपये हैं।", 10)
    draw_hindi(c, col1 + 10, cursor_y - 80, "तीनों के पास कुल कितने रुपये हैं?", 10)
    draw_hindi(c, col1 + 10, cursor_y - 120, "उत्तर: ______________________", 11)

    draw_card(c, col2, cursor_y - h_p2_r3, col_width, h_p2_r3, "प्र. 14: हल करें (Word Problem)", "[5 अंक]", COLOR_ACCENT)
    draw_hindi(c, col2 + 10, cursor_y - 40, "एक स्कूल में 4500 बच्चे हैं। आज 500", 10)
    draw_hindi(c, col2 + 10, cursor_y - 60, "बच्चे नहीं आए (Absent)। बताइये आज", 10)
    draw_hindi(c, col2 + 10, cursor_y - 80, "स्कूल में कितने बच्चे उपस्थित हैं?", 10)
    draw_hindi(c, col2 + 10, cursor_y - 120, "उत्तर: ______________________", 11)

    cursor_y -= (h_p2_r3 + P2_GAP)

    # Q15 & Q16
    h_p2_r4 = 120
    draw_card(c, col1, cursor_y - h_p2_r4, col_width, h_p2_r4, "प्र. 15: पैटर्न पूरा करें", "[5 अंक]")
    c.setFont("Helvetica", 10)
    for i, p in enumerate(["(a) 100, 200, 300, ____, 500", "(b) 5, 10, 15, ____, 25", "(c) A, B, C, ____, E", "(d) 2, 4, 8, 16, ____", "(e) 11, 22, 33, ____, 55"]):
        c.drawString(col1 + 10, cursor_y - 35 - (i*18), p)

    draw_card(c, col2, cursor_y - h_p2_r4, col_width, h_p2_r4, "प्र. 16: दिमागी कसरत (Mental Math)", "[5 अंक]")
    draw_hindi(c, col2 + 10, cursor_y - 35, "(a) 100 + 50 = ______", 10)
    draw_hindi(c, col2 + 10, cursor_y - 53, "(b) 500 में 1 जोड़ने पर? ______", 10)
    draw_hindi(c, col2 + 10, cursor_y - 71, "(c) 1 सप्ताह में कितने दिन? ______", 10)
    draw_hindi(c, col2 + 10, cursor_y - 89, "(d) 20 के 3 नोट = ______ रु", 10)
    draw_hindi(c, col2 + 10, cursor_y - 107, "(e) 10 में से 10 गया = ______", 10)

    # Good Luck
    draw_hindi(c, width/2, cursor_y - h_p2_r4 - 30, "*** परीक्षा समाप्त (Good Luck) ***", 12, COLOR_PRIMARY, align="center")

    draw_footer(c, width, 2)
    c.save()
    print(f"Success! Created: {OUTPUT_FILENAME}")

if __name__ == "__main__":
    create_paper()