import os
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw, ImageFont # Requires pip install Pillow

# --- CONFIGURATION ---
OUTPUT_FILENAME = "Class_1_Perfect_Exam.pdf"
LOGO_LEFT = "DBG-logo.png"
LOGO_RIGHT = "DBM-logo.png"
WATERMARK_IMG = "DBG-logo.png"

# COLORS
COLOR_PRIMARY = "#154c79"   # Navy
COLOR_ACCENT = "#e08d3c"    # Orange/Gold
COLOR_TEXT = "#000000"      # Black
COLOR_BG_HEADER = "#f4f6f9" # Light Grey

# FONT CONFIG
# Windows usually handles Hindi shaping better with 'Nirmala UI' or 'Mangal' via PIL
FONT_PATH = "C:\\Windows\\Fonts\\Nirmala.ttf" 
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:\\Windows\\Fonts\\mangal.ttf" # Fallback
if not os.path.exists(FONT_PATH):
    # Fallback to local file if system font missing
    FONT_PATH = "Nirmala.ttf" 

# --- TEXT RENDERING ENGINE (The "Thinking Hard" Solution) ---

def render_text_as_image(text, size, color_hex, max_width=None):
    """
    Renders text to a high-res transparent PNG using Pillow.
    This preserves complex Hindi shaping (Sanyuktakshars).
    """
    if not text: return None, 0, 0

    # 1. Setup Font (Scale up 4x for crisp PDF rendering)
    scale_factor = 4 
    try:
        pil_font = ImageFont.truetype(FONT_PATH, size * scale_factor)
    except:
        # Fallback default
        pil_font = ImageFont.load_default()

    # 2. Calculate Size
    dummy_img = Image.new('RGBA', (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), text, font=pil_font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1] + (5 * scale_factor) # Add padding for Matras (top/bottom)

    # 3. Draw Text
    img = Image.new('RGBA', (w, h), (255, 255, 255, 0)) # Transparent
    draw = ImageDraw.Draw(img)
    
    # Convert Hex color to RGB
    c_rgb = colors.HexColor(color_hex).rgb()
    c_tuple = (int(c_rgb[0]*255), int(c_rgb[1]*255), int(c_rgb[2]*255))
    
    draw.text((0, 0), text, font=pil_font, fill=c_tuple)
    
    # 4. Return as ReportLab Image
    return ImageReader(img), w / scale_factor, h / scale_factor

def draw_text(c, text, x, y, size=10, color=COLOR_TEXT, align="left"):
    """
    Wrapper to place the rendered text image onto the PDF canvas.
    align: 'left', 'center', 'right'
    """
    img_obj, w, h = render_text_as_image(text, size, color)
    if not img_obj: return

    # Adjust Y because images draw from bottom-left, but text baselines vary
    # We approximate baseline correction
    y_adj = y - (h * 0.75) 

    if align == "center":
        x_adj = x - (w / 2)
    elif align == "right":
        x_adj = x - w
    else:
        x_adj = x
        
    c.drawImage(img_obj, x_adj, y_adj, width=w, height=h, mask='auto')

# --- LAYOUT COMPONENTS ---

def draw_header(c, width, height, page_num):
    c.saveState()
    
    # Background
    header_h = 115
    c.setFillColor(HexColor(COLOR_BG_HEADER))
    c.rect(0, height - header_h, width, header_h, fill=1, stroke=0)
    c.setStrokeColor(HexColor(COLOR_PRIMARY))
    c.setLineWidth(3)
    c.line(0, height - header_h, width, height - header_h)
    
    # Logos
    logo_size = 70
    margin = 25
    logo_y = height - 95
    if os.path.exists(LOGO_LEFT):
        c.drawImage(LOGO_LEFT, margin, logo_y, width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)
    if os.path.exists(LOGO_RIGHT):
        c.drawImage(LOGO_RIGHT, width - margin - logo_size, logo_y, width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)
        
    # Main Title
    draw_text(c, "DBG GURUKULAM", width/2, height - 45, size=26, color=COLOR_PRIMARY, align="center")
    
    if page_num == 1:
        # Sub Title
        sub = "कक्षा : 1 (First)   |   विषय: गणित (Maths)   |   समय: 2 घंटे"
        draw_text(c, sub, width/2, height - 75, size=12, color=COLOR_TEXT, align="center")
        
        # Student Box
        box_y = height - 150
        c.setStrokeColor(HexColor("#999999"))
        c.setLineWidth(1)
        c.roundRect(20, box_y, width - 40, 30, 5, fill=0, stroke=1)
        
        details = "नाम: ___________________________   रोल नं: _________   दिनांक: _________"
        draw_text(c, details, width/2, box_y + 10, size=11, color=COLOR_TEXT, align="center")
        
        # Marks
        marks_y = box_y - 20
        draw_text(c, "Total Questions: 16", 20, marks_y, size=10, color=COLOR_PRIMARY, align="left")
        draw_text(c, "पूर्णांक (Max Marks): 80", width - 20, marks_y, size=10, color=COLOR_PRIMARY, align="right")
        
        return marks_y - 20
    else:
        draw_text(c, "गणित - भाग 2 (Page 2)", width/2, height - 75, size=12, color=COLOR_TEXT, align="center")
        return height - 120

    c.restoreState()

def draw_card(c, x, y, w, h, title, marks, accent=COLOR_PRIMARY):
    c.saveState()
    radius = 8
    
    # Shadow
    c.setFillColor(HexColor("#e5e7eb"))
    c.roundRect(x+3, y-3, w, h, radius, fill=1, stroke=0)
    
    # Box
    c.setFillColor(colors.white)
    c.setStrokeColor(HexColor("#d1d5db"))
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    
    # Header Bar
    head_h = 25
    # Clip top corners
    p = c.beginPath()
    p.roundRect(x, y, w, h, radius)
    c.clipPath(p, stroke=0)
    
    c.setFillColor(HexColor(accent))
    c.rect(x, y + h - head_h, w, head_h, fill=1, stroke=0)
    
    # Title Texts
    # We explicitly draw these on top of the color
    draw_text(c, title, x + 10, y + h - 18, size=10, color="#FFFFFF", align="left")
    draw_text(c, marks, x + w - 10, y + h - 18, size=10, color="#FFFFFF", align="right")
    
    c.restoreState()

def draw_watermark(c, width, height):
    if os.path.exists(WATERMARK_IMG):
        c.saveState()
        c.setFillAlpha(0.08)
        wm_size = 450
        c.drawImage(WATERMARK_IMG, (width-wm_size)/2, (height-wm_size)/2, width=wm_size, height=wm_size, mask='auto', preserveAspectRatio=True)
        c.restoreState()

def draw_footer(c, width, page_num):
    c.saveState()
    y = 20
    c.setStrokeColor(HexColor(COLOR_ACCENT))
    c.setLineWidth(2)
    c.line(0, y + 15, width, y + 15)
    
    # Page Circle
    c.setFillColor(HexColor(COLOR_PRIMARY))
    c.circle(30, y + 6, 12, fill=1, stroke=0)
    draw_text(c, str(page_num), 30, y + 2, size=10, color="#FFFFFF", align="center")
    
    draw_text(c, "Shri Classes & DBG Gurukulam (by IITian Golu Sir)", width/2, y + 3, size=9, align="center")
    draw_text(c, "https://dbggurukulam.com", width - 20, y + 3, size=9, color=COLOR_PRIMARY, align="right")
    c.restoreState()

def draw_math_vertical(c, x, y, num1, op, num2):
    # Align numbers to the right
    draw_text(c, num1, x + 40, y, size=14, align="right")
    draw_text(c, num2, x + 40, y - 18, size=14, align="right")
    draw_text(c, op, x - 5, y - 18, size=14, align="left")
    
    c.setLineWidth(1.5)
    c.line(x - 5, y - 25, x + 45, y - 25)

# --- MAIN ---

def create_perfect_paper():
    c = canvas.Canvas(OUTPUT_FILENAME, pagesize=A4)
    width, height = A4
    
    # ================= PAGE 1 =================
    draw_watermark(c, width, height)
    cursor_y = draw_header(c, width, height, 1)
    
    # Layout Constants
    MARGIN = 20
    GAP = 15
    col_w = (width - (3*MARGIN))/2
    col1 = MARGIN
    col2 = MARGIN + col_w + MARGIN
    
    # Q1 & Q2
    h_r1 = 120
    draw_card(c, col1, cursor_y - h_r1, col_w, h_r1, "प्र. 1: शब्दों में लिखें (Words)", "[5 अंक]")
    q1s = ["(a) 75 :", "(b) 89 :", "(c) 46 :", "(d) 99 :", "(e) 29 :"]
    for i, q in enumerate(q1s):
        y = cursor_y - 32 - (i * 18)
        draw_text(c, q, col1 + 10, y, size=10)
        c.setStrokeColor(colors.grey)
        c.setLineWidth(0.5)
        c.line(col1 + 50, y - 5, col1 + col_w - 10, y - 5)

    draw_card(c, col2, cursor_y - h_r1, col_w, h_r1, "प्र. 2: स्थानीय मान (Place Value)", "[5 अंक]")
    q2s = ["(a) 540 में 5 का मान:", "(b) 892 में 9 का मान:", "(c) 1000 में 1 का मान:", "(d) 607 में 7 का मान:", "(e) 4550 में 0 का मान:"]
    for i, q in enumerate(q2s):
        y = cursor_y - 32 - (i * 18)
        draw_text(c, q, col2 + 10, y, size=10)
        c.setStrokeColor(colors.grey)
        c.setLineWidth(0.5)
        c.line(col2 + 135, y - 5, col2 + col_w - 10, y - 5)

    cursor_y -= (h_r1 + GAP)
    
    # Q3 & Q4 (Math)
    h_math = 80
    draw_card(c, col1, cursor_y - h_math, width - 40, h_math, "प्र. 3: जोड़ें (Addition)", "[5 अंक]", accent=COLOR_ACCENT)
    math_y = cursor_y - 45
    spacing = (width - 80) / 4
    sx = col1 + 50
    draw_math_vertical(c, sx, math_y, "4230", "+", "1540")
    draw_math_vertical(c, sx + spacing, math_y, "6525", "+", "2354")
    draw_math_vertical(c, sx + spacing*2, math_y, "5005", "+", "4990")
    draw_math_vertical(c, sx + spacing*3, math_y, "1234", "+", "4321")

    cursor_y -= (h_math + GAP)
    
    draw_card(c, col1, cursor_y - h_math, width - 40, h_math, "प्र. 4: घटाएँ (Subtraction)", "[5 अंक]", accent=COLOR_ACCENT)
    math_y = cursor_y - 45
    draw_math_vertical(c, sx, math_y, "8956", "-", "4523")
    draw_math_vertical(c, sx + spacing, math_y, "5640", "-", "2310")
    draw_math_vertical(c, sx + spacing*2, math_y, "9000", "-", "1000")
    draw_math_vertical(c, sx + spacing*3, math_y, "7550", "-", "2550")

    cursor_y -= (h_math + GAP)
    
    # Q5 & Q6
    h_r3 = 130
    draw_card(c, col1, cursor_y - h_r3, col_w, h_r3, "प्र. 5: विस्तारित रूप (Expanded Form)", "[5 अंक]")
    q5s = [
        "(a) 5426 = 5000 + 400 + 20 + 6",
        "(b) 3250 = ___ + ___ + ___ + 0",
        "(c) 7085 = ___ + 00 + ___ + 5",
        "(d) 1200 = 1000 + ___ + 00 + 0",
        "(e) 4040 = ___ + 0 + ___ + 0"
    ]
    for i, q in enumerate(q5s):
        draw_text(c, q, col1 + 10, cursor_y - 30 - (i*19), size=9.5)

    draw_card(c, col2, cursor_y - h_r3, col_w, h_r3, "प्र. 6: गुणा करें (Multiply)", "[5 अंक]")
    ms = col_w / 4
    mx = col2 + 15
    my = cursor_y - 55
    draw_math_vertical(c, mx, my, "24", "x", "2")
    draw_math_vertical(c, mx + ms + 5, my, "33", "x", "3")
    draw_math_vertical(c, mx + (ms+5)*2, my, "12", "x", "4")
    draw_math_vertical(c, mx + (ms+5)*3, my, "40", "x", "2")

    cursor_y -= (h_r3 + GAP)

    # Q7 & Q8
    h_r4 = 100
    draw_card(c, col1, cursor_y - h_r4, col_w, h_r4, "प्र. 7: चिन्ह लगाएँ (<, >, =)", "[5 अंक]")
    draw_text(c, "4500 [   ] 5400", col1 + 20, cursor_y - 35, size=11)
    draw_text(c, "8000 [   ] 8000", col1 + 150, cursor_y - 35, size=11)
    draw_text(c, "2020 [   ] 2002", col1 + 20, cursor_y - 58, size=11)
    draw_text(c, "500 [   ] 50", col1 + 150, cursor_y - 58, size=11)
    draw_text(c, "1010 [   ] 1001", col1 + 20, cursor_y - 81, size=11)

    draw_card(c, col2, cursor_y - h_r4, col_w, h_r4, "प्र. 8: भाग दें (Division)", "[5 अंक]")
    draw_text(c, "(a) 20 ÷ 2 = ___", col2 + 10, cursor_y - 30, size=10)
    draw_text(c, "(b) 15 ÷ 3 = ___", col2 + 120, cursor_y - 30, size=10)
    draw_text(c, "(c) 16 ÷ 4 = ___", col2 + 10, cursor_y - 52, size=10)
    draw_text(c, "(d) 10 ÷ 5 = ___", col2 + 120, cursor_y - 52, size=10)
    draw_text(c, "(e) 30 ÷ 3 = ___", col2 + 10, cursor_y - 74, size=10)
    
    draw_footer(c, width, 1)
    c.showPage()

    # ================= PAGE 2 =================
    draw_watermark(c, width, height)
    cursor_y = draw_header(c, width, height, 2)
    P2_GAP = 20
    
    # Q9 & Q10
    h_p2_r1 = 110
    draw_card(c, col1, cursor_y - h_p2_r1, col_w, h_p2_r1, "प्र. 9: बढ़ते क्रम (Increasing Order)", "[5 अंक]")
    draw_text(c, "(a) 500, 200, 800, 100", col1 + 10, cursor_y - 30, size=10)
    draw_text(c, "     -> ____, ____, ____, ____", col1 + 10, cursor_y - 45, size=10)
    draw_text(c, "(b) 10, 50, 30, 20, 40", col1 + 10, cursor_y - 65, size=10)
    draw_text(c, "     -> ____, ____, ____, ____, ____", col1 + 10, cursor_y - 80, size=10)

    draw_card(c, col2, cursor_y - h_p2_r1, col_w, h_p2_r1, "प्र. 10: घटते क्रम (Decreasing Order)", "[5 अंक]")
    draw_text(c, "(a) 45, 90, 12, 65", col2 + 10, cursor_y - 30, size=10)
    draw_text(c, "     -> ____, ____, ____, ____", col2 + 10, cursor_y - 45, size=10)
    draw_text(c, "(b) 88, 11, 55, 33, 77", col2 + 10, cursor_y - 65, size=10)
    draw_text(c, "     -> ____, ____, ____, ____, ____", col2 + 10, cursor_y - 80, size=10)

    cursor_y -= (h_p2_r1 + P2_GAP)

    # Q11 & Q12
    h_p2_r2 = 120
    draw_card(c, col1, cursor_y - h_p2_r2, col_w, h_p2_r2, "प्र. 11: पहले और बाद की संख्या", "[5 अंक]")
    draw_text(c, "(a) ____ <- 500 -> ____", col1 + 10, cursor_y - 30, size=10)
    draw_text(c, "(b) ____ <- 1000 -> ____", col1 + 10, cursor_y - 50, size=10)
    draw_text(c, "(c) 99 के बाद: ________", col1 + 10, cursor_y - 70, size=10)
    draw_text(c, "(d) 50 से पहले: ________", col1 + 10, cursor_y - 90, size=10)

    draw_card(c, col2, cursor_y - h_p2_r2, col_w, h_p2_r2, "प्र. 12: पहाड़ा और पैटर्न (Tables)", "[5 अंक]")
    draw_text(c, "(a) 12 का पहाड़ा: 12, 24, ___, 48", col2 + 10, cursor_y - 30, size=10)
    draw_text(c, "(b) 15 का पहाड़ा: 15, 30, ___, 60", col2 + 10, cursor_y - 50, size=10)
    draw_text(c, "(c) 2 का पहाड़ा: 2, 4, 6, ___, 10", col2 + 10, cursor_y - 70, size=10)
    draw_text(c, "(d) 10, 20, 30, ___, 50", col2 + 10, cursor_y - 90, size=10)

    cursor_y -= (h_p2_r2 + P2_GAP)

    # Q13 & Q14 (Word Problems - Height Fill)
    h_p2_r3 = 140
    draw_card(c, col1, cursor_y - h_p2_r3, col_w, h_p2_r3, "प्र. 13: हल करें (Word Problem)", "[5 अंक]", accent=COLOR_ACCENT)
    draw_text(c, "राम के पास 2500 रुपये, श्याम के पास", col1 + 10, cursor_y - 30, size=10)
    draw_text(c, "1200 रुपये और मोहन के पास 100 रुपये हैं।", col1 + 10, cursor_y - 48, size=10)
    draw_text(c, "तीनों के पास कुल कितने रुपये हैं?", col1 + 10, cursor_y - 66, size=10)
    draw_text(c, "उत्तर: _________________________", col1 + 10, cursor_y - 115, size=11)

    draw_card(c, col2, cursor_y - h_p2_r3, col_w, h_p2_r3, "प्र. 14: हल करें (Word Problem)", "[5 अंक]", accent=COLOR_ACCENT)
    draw_text(c, "एक स्कूल में 4500 बच्चे हैं। आज 500", col2 + 10, cursor_y - 30, size=10)
    draw_text(c, "बच्चे नहीं आए (Absent)। बताइये आज", col2 + 10, cursor_y - 48, size=10)
    draw_text(c, "स्कूल में कितने बच्चे उपस्थित हैं?", col2 + 10, cursor_y - 66, size=10)
    draw_text(c, "उत्तर: _________________________", col2 + 10, cursor_y - 115, size=11)

    cursor_y -= (h_p2_r3 + P2_GAP)

    # Q15 & Q16
    h_p2_r4 = 120
    draw_card(c, col1, cursor_y - h_p2_r4, col_w, h_p2_r4, "प्र. 15: पैटर्न पूरा करें", "[5 अंक]")
    pats = ["(a) 100, 200, 300, ____, 500", "(b) 5, 10, 15, ____, 25", "(c) A, B, C, ____, E", "(d) 2, 4, 8, 16, ____", "(e) 11, 22, 33, ____, 55"]
    for i, p in enumerate(pats):
        draw_text(c, p, col1 + 10, cursor_y - 30 - (i*18), size=10)

    draw_card(c, col2, cursor_y - h_p2_r4, col_w, h_p2_r4, "प्र. 16: दिमागी कसरत (Mental Math)", "[5 अंक]")
    mm = ["(a) 100 + 50 = ______", "(b) 500 में 1 जोड़ने पर? ______", "(c) 1 सप्ताह में कितने दिन? ______", "(d) 20 के 3 नोट = ______ रु", "(e) 10 में से 10 गया = ______"]
    for i, m in enumerate(mm):
        draw_text(c, m, col2 + 10, cursor_y - 30 - (i*18), size=10)
    
    # Good Luck
    draw_text(c, "*** परीक्षा समाप्त (Good Luck) ***", width/2, cursor_y - h_p2_r4 - 35, size=12, color=COLOR_PRIMARY, align="center")
    
    draw_footer(c, width, 2)
    c.save()
    print(f"SUCCESS: Generated {OUTPUT_FILENAME}")

if __name__ == "__main__":
    create_perfect_paper()