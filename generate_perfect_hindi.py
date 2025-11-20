import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from PIL import Image, ImageDraw, ImageFont
import textwrap

# --- CONFIGURATION ---
OUTPUT_FILENAME = "Class_1_Maths_Perfect.pdf"
LOGO_LEFT = "DBG-logo.png"
LOGO_RIGHT = "DBM-logo.png"
WATERMARK_IMG = "DBG-logo.png"

# Font Config: Prioritize Windows Hindi Fonts
FONT_PATH = "C:\\Windows\\Fonts\\Nirmala.ttf"
if not os.path.exists(FONT_PATH):
    # Fallback if Nirmala is missing
    FONT_PATH = "C:\\Windows\\Fonts\\arialuni.ttf" 

# --- TEXT RENDERING ENGINE (The Magic Fix) ---
def draw_text(c, text, x, y, fontsize=10, color=(0,0,0), align='left', bold=False):
    """
    Renders text using PIL to handle Hindi Sanyuktakshars (Conjuncts) perfectly.
    """
    if not text: return

    # 1. Setup High-Res Image for Crisp Text
    scale_factor = 4 # Render 4x larger than needed for sharpness
    pil_font_size = int(fontsize * scale_factor)
    
    try:
        font = ImageFont.truetype(FONT_PATH, pil_font_size)
    except:
        # Emergency fallback
        font = ImageFont.load_default()

    # 2. Calculate Text Size
    # We add 'Ay' to ensure height covers ascenders/descenders
    bbox = font.getbbox(text + "Ay") 
    text_width = font.getlength(text)
    text_height = bbox[3] - bbox[1]
    
    # Padding to prevent cutting off matras
    h_pad = int(pil_font_size * 0.3)
    w_pad = int(pil_font_size * 0.1)
    
    img_w = int(text_width + w_pad * 2)
    img_h = int(text_height + h_pad)

    # 3. Create Transparent Image
    img = Image.new('RGBA', (img_w, img_h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw text in black (or requested color)
    draw.text((w_pad, 0), text, font=font, fill=color + (255,))

    # 4. Calculate PDF Coordinates
    pdf_w = img_w / scale_factor
    pdf_h = img_h / scale_factor
    
    # Handle Alignment
    final_x = x
    if align == 'right':
        final_x = x - pdf_w + (w_pad/scale_factor)
    elif align == 'center':
        final_x = x - (pdf_w / 2)

    # Adjust Y to match Baseline (Approximate descent adjustment)
    # PDF Y is bottom-up. We draw the image slightly down so 'y' is the baseline
    final_y = y - (pdf_h * 0.75) 

    # 5. Draw on Canvas
    c.drawInlineImage(img, final_x, final_y, width=pdf_w, height=pdf_h, preserveAspectRatio=True)

# --- LAYOUT HELPERS ---

def draw_watermark(c, width, height):
    if os.path.exists(WATERMARK_IMG):
        c.saveState()
        c.setFillAlpha(0.1) # 10% opacity
        wm_size = 350
        c.drawImage(WATERMARK_IMG, (width - wm_size)/2, (height - wm_size)/2, 
                    width=wm_size, height=wm_size, mask='auto', preserveAspectRatio=True)
        c.restoreState()

def draw_header(c, width, height, page_text):
    c.saveState()
    
    # Logos
    logo_size = 60
    if os.path.exists(LOGO_LEFT):
        c.drawImage(LOGO_LEFT, 25, height - 75, width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)
    if os.path.exists(LOGO_RIGHT):
        c.drawImage(LOGO_RIGHT, width - 25 - logo_size, height - 75, width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)

    # Title
    draw_text(c, "DBG GURUKULAM", width/2, height - 45, fontsize=22, align='center')
    
    if page_text == "Page 1":
        # Line 1
        info = "कक्षा : 1 (First)      विषय: गणित (Maths)      समय: 2 घंटे"
        draw_text(c, info, width/2, height - 68, fontsize=11, align='center')
        
        # Name Box
        box_top = height - 85
        c.setLineWidth(1)
        c.rect(20, box_top - 22, width - 40, 22)
        
        name_line = "नाम: ___________________________   रोल नं: _______   दिनांक: _______"
        draw_text(c, name_line, 28, box_top - 15, fontsize=10)
        
        # Marks Line
        c.line(20, box_top - 28, width - 20, box_top - 28) # Separator
        draw_text(c, "Total Questions: 16", 20, box_top - 42, fontsize=10)
        draw_text(c, "पूर्णांक (Max Marks): 80", width - 20, box_top - 42, fontsize=10, align='right')
        c.line(20, box_top - 47, width - 20, box_top - 47) # Bottom line
        
        return box_top - 55
    else:
        draw_text(c, "गणित - भाग 2 (Page 2)", width/2, height - 68, fontsize=12, align='center')
        c.setLineWidth(1)
        c.line(20, height - 75, width - 20, height - 75)
        return height - 85

    c.restoreState()

def draw_box(c, x, y, w, h, title, marks):
    """Draws rounded box with Grey Header"""
    radius = 6
    
    # 1. Box Background
    c.saveState()
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    
    # 2. Header Background (Clipped)
    header_h = 22
    p = c.beginPath()
    p.roundRect(x, y, w, h, radius)
    c.clipPath(p, stroke=0)
    
    c.setFillColor(colors.Color(0.92, 0.92, 0.92)) # Light Grey
    c.rect(x, y + h - header_h, w, header_h, fill=1, stroke=0)
    c.restoreState() # Restore clipping
    
    # 3. Header Line & Text
    c.setLineWidth(1)
    c.line(x, y + h - header_h, x + w, y + h - header_h)
    
    # Re-draw border on top to clean up
    c.setStrokeColor(colors.black)
    c.roundRect(x, y, w, h, radius, fill=0, stroke=1)
    
    # Text (Using PIL for Hindi)
    draw_text(c, title, x + 8, y + h - 16, fontsize=10)
    draw_text(c, marks, x + w - 8, y + h - 16, fontsize=10, align='right')

def draw_math_vertical(c, x, y, n1, op, n2):
    """Maths numbers are fine as standard text (Better alignment)"""
    c.setFont("Helvetica", 14) # Standard font aligns numbers better
    c.drawRightString(x + 40, y, n1)
    c.drawRightString(x + 40, y - 18, n2)
    c.drawString(x - 5, y - 18, op)
    c.setLineWidth(1.5)
    c.line(x - 5, y - 22, x + 45, y - 22)

def draw_footer(c, width, page_num):
    y = 20
    c.setLineWidth(0.5)
    c.line(20, y + 12, width - 20, y + 12)
    
    draw_text(c, f"Page {page_num}", 25, y, fontsize=9)
    draw_text(c, "Shri Classes & DBG Gurukulam (by IITian Golu Sir)", width/2, y, fontsize=9, align='center')
    draw_text(c, "https://dbggurukulam.com", width - 25, y, fontsize=9, color=(0,0,255), align='right')

# --- MAIN GENERATION ---

def create_paper():
    c = canvas.Canvas(OUTPUT_FILENAME, pagesize=A4)
    width, height = A4
    
    # ================= PAGE 1 =================
    draw_watermark(c, width, height)
    curr_y = draw_header(c, width, height, "Page 1")
    
    # Setup Columns
    margin = 20
    gap = 10
    col_w = (width - (margin*2) - gap) / 2
    c1 = margin
    c2 = margin + col_w + gap
    
    # Q1 & Q2
    h1 = 100
    draw_box(c, c1, curr_y - h1, col_w, h1, "प्र. 1: शब्दों में लिखें (Words)", "[5 अंक]")
    qy = curr_y - 25
    for line in ["(a) 75 : _______________", "(b) 89 : _______________", "(c) 46 : _______________", "(d) 99 : _______________", "(e) 29 : _______________"]:
        draw_text(c, line, c1 + 10, qy, fontsize=10)
        qy -= 16
        
    draw_box(c, c2, curr_y - h1, col_w, h1, "प्र. 2: स्थानीय मान (Place Value)", "[5 अंक]")
    qy = curr_y - 25
    q2_lines = ["(a) 540 में 5 का मान: ______", "(b) 892 में 9 का मान: ______", "(c) 1000 में 1 का मान: _____", "(d) 607 में 7 का मान: ______", "(e) 4550 में 0 का मान: _____"]
    for line in q2_lines:
        draw_text(c, line, c2 + 10, qy, fontsize=10)
        qy -= 16
        
    curr_y -= (h1 + 10)
    
    # Q3 Addition
    h2 = 70
    draw_box(c, c1, curr_y - h2, width - 40, h2, "प्र. 3: जोड़ें (Addition)", "[5 अंक]")
    mx = c1 + 50
    my = curr_y - 40
    step = (width - 100)/3
    draw_math_vertical(c, mx, my, "4230", "+", "1540")
    draw_math_vertical(c, mx + step, my, "6525", "+", "2354")
    draw_math_vertical(c, mx + step*2, my, "5005", "+", "4990")
    draw_math_vertical(c, mx + step*3, my, "1234", "+", "4321")
    
    curr_y -= (h2 + 10)
    
    # Q4 Subtraction
    draw_box(c, c1, curr_y - h2, width - 40, h2, "प्र. 4: घटाएँ (Subtraction)", "[5 अंक]")
    my = curr_y - 40
    draw_math_vertical(c, mx, my, "8956", "-", "4523")
    draw_math_vertical(c, mx + step, my, "5640", "-", "2310")
    draw_math_vertical(c, mx + step*2, my, "9000", "-", "1000")
    draw_math_vertical(c, mx + step*3, my, "7550", "-", "2550")
    
    curr_y -= (h2 + 10)
    
    # Q5 & Q6
    h3 = 115
    draw_box(c, c1, curr_y - h3, col_w, h3, "प्र. 5: विस्तारित रूप (Expanded Form)", "[5 अंक]")
    qy = curr_y - 25
    q5_lines = [
        "(a) 5426 = 5000 + 400 + 20 + 6", 
        "(b) 3250 = ____ + ____ + ____ + 0",
        "(c) 7085 = ____ + 00 + ____ + 5",
        "(d) 1200 = 1000 + ____ + 00 + 0",
        "(e) 4040 = ____ + 0 + ____ + 0"
    ]
    for line in q5_lines:
        draw_text(c, line, c1 + 8, qy, fontsize=9)
        qy -= 18
        
    draw_box(c, c2, curr_y - h3, col_w, h3, "प्र. 6: गुणा करें (Multiply)", "[5 अंक]")
    mmx = c2 + 20
    mmy = curr_y - 55
    mstep = col_w / 4
    draw_math_vertical(c, mmx, mmy, "24", "x", "2")
    draw_math_vertical(c, mmx + mstep + 10, mmy, "33", "x", "3")
    draw_math_vertical(c, mmx + (mstep+10)*2, mmy, "12", "x", "4")
    draw_math_vertical(c, mmx + (mstep+10)*3, mmy, "40", "x", "2")
    
    curr_y -= (h3 + 10)
    
    # Q7 & Q8
    h4 = 90
    draw_box(c, c1, curr_y - h4, col_w, h4, "प्र. 7: चिन्ह लगाएँ (<, >, =)", "[5 अंक]")
    qy = curr_y - 30
    draw_text(c, "4500 [___] 5400", c1 + 10, qy, fontsize=10)
    draw_text(c, "8000 [___] 8000", c1 + 130, qy, fontsize=10)
    draw_text(c, "2020 [___] 2002", c1 + 10, qy - 20, fontsize=10)
    draw_text(c, "500 [___] 50", c1 + 130, qy - 20, fontsize=10)
    draw_text(c, "1010 [___] 1001", c1 + 10, qy - 40, fontsize=10)
    
    draw_box(c, c2, curr_y - h4, col_w, h4, "प्र. 8: भाग दें (Division)", "[5 अंक]")
    qy = curr_y - 25
    draw_text(c, "(a) 20 ÷ 2 = ___    (b) 15 ÷ 3 = ___", c2 + 10, qy, fontsize=10)
    draw_text(c, "(c) 16 ÷ 4 = ___    (d) 10 ÷ 5 = ___", c2 + 10, qy - 22, fontsize=10)
    draw_text(c, "(e) 30 ÷ 3 = ___", c2 + 10, qy - 44, fontsize=10)
    
    draw_footer(c, width, 1)
    c.showPage()
    
    # ================= PAGE 2 =================
    draw_watermark(c, width, height)
    curr_y = draw_header(c, width, height, "Page 2")
    curr_y -= 5
    
    # Q9 & Q10
    h_p2 = 85
    draw_box(c, c1, curr_y - h_p2, col_w, h_p2, "प्र. 9: बढ़ते क्रम (Increasing Order)", "[5 अंक]")
    qy = curr_y - 25
    draw_text(c, "(a) 500, 200, 800, 100", c1 + 10, qy, fontsize=10)
    draw_text(c, "     → ____, ____, ____, ____", c1 + 10, qy - 15, fontsize=10)
    draw_text(c, "(b) 10, 50, 30, 20, 40", c1 + 10, qy - 35, fontsize=10)
    draw_text(c, "     → ____, ____, ____, ____, ____", c1 + 10, qy - 50, fontsize=10)
    
    draw_box(c, c2, curr_y - h_p2, col_w, h_p2, "प्र. 10: घटते क्रम (Decreasing Order)", "[5 अंक]")
    draw_text(c, "(a) 45, 90, 12, 65", c2 + 10, qy, fontsize=10)
    draw_text(c, "     → ____, ____, ____, ____", c2 + 10, qy - 15, fontsize=10)
    draw_text(c, "(b) 88, 11, 55, 33, 77", c2 + 10, qy - 35, fontsize=10)
    draw_text(c, "     → ____, ____, ____, ____, ____", c2 + 10, qy - 50, fontsize=10)
    
    curr_y -= (h_p2 + 10)
    
    # Q11 & Q12
    h_p2_2 = 100
    draw_box(c, c1, curr_y - h_p2_2, col_w, h_p2_2, "प्र. 11: पहले और बाद की संख्या", "[5 अंक]")
    qy = curr_y - 25
    draw_text(c, "(a) ____ ← 500 → ____", c1 + 10, qy, fontsize=10)
    draw_text(c, "(b) ____ ← 1000 → ____", c1 + 10, qy - 20, fontsize=10)
    draw_text(c, "(c) 99 के बाद: _________", c1 + 10, qy - 40, fontsize=10)
    draw_text(c, "(d) 50 से पहले: ________", c1 + 10, qy - 60, fontsize=10)
    
    draw_box(c, c2, curr_y - h_p2_2, col_w, h_p2_2, "प्र. 12: पहाड़ा और पैटर्न (Tables)", "[5 अंक]")
    draw_text(c, "(a) 12 का पहाड़ा: 12, 24, __, 48", c2 + 10, qy, fontsize=10)
    draw_text(c, "(b) 15 का पहाड़ा: 15, 30, __, 60", c2 + 10, qy - 20, fontsize=10)
    draw_text(c, "(c) 2 का पहाड़ा: 2, 4, 6, __, 10", c2 + 10, qy - 40, fontsize=10)
    draw_text(c, "(d) 10, 20, 30, __, 50", c2 + 10, qy - 60, fontsize=10)
    
    curr_y -= (h_p2_2 + 10)
    
    # Q13 & Q14 Word Problems
    h_p2_3 = 115
    draw_box(c, c1, curr_y - h_p2_3, col_w, h_p2_3, "प्र. 13: हल करें (Word Problem)", "[5 अंक]")
    qy = curr_y - 25
    t1 = "राम के पास 2500 रुपये, श्याम के पास"
    t2 = "1200 रुपये और मोहन के पास 100 रुपये हैं।"
    t3 = "तीनों के पास कुल कितने रुपये हैं?"
    draw_text(c, t1, c1 + 6, qy, fontsize=10)
    draw_text(c, t2, c1 + 6, qy - 15, fontsize=10)
    draw_text(c, t3, c1 + 6, qy - 30, fontsize=10)
    draw_text(c, "उत्तर: ___________________________", c1 + 6, qy - 65, fontsize=10)
    
    draw_box(c, c2, curr_y - h_p2_3, col_w, h_p2_3, "प्र. 14: हल करें (Word Problem)", "[5 अंक]")
    t1 = "एक स्कूल में 4500 बच्चे हैं। आज 500"
    t2 = "बच्चे नहीं आए (Absent)। बताइये आज"
    t3 = "स्कूल में कितने बच्चे उपस्थित हैं?"
    draw_text(c, t1, c2 + 6, qy, fontsize=10)
    draw_text(c, t2, c2 + 6, qy - 15, fontsize=10)
    draw_text(c, t3, c2 + 6, qy - 30, fontsize=10)
    draw_text(c, "उत्तर: ___________________________", c2 + 6, qy - 65, fontsize=10)
    
    curr_y -= (h_p2_3 + 10)
    
    # Q15 & Q16
    h_p2_4 = 110
    draw_box(c, c1, curr_y - h_p2_4, col_w, h_p2_4, "प्र. 15: पैटर्न पूरा करें", "[5 अंक]")
    qy = curr_y - 25
    draw_text(c, "(a) 100, 200, 300, _____, 500", c1 + 10, qy, fontsize=10)
    draw_text(c, "(b) 5, 10, 15, _____, 25", c1 + 10, qy - 16, fontsize=10)
    draw_text(c, "(c) A, B, C, _____, E", c1 + 10, qy - 32, fontsize=10)
    draw_text(c, "(d) 2, 4, 8, 16, ______", c1 + 10, qy - 48, fontsize=10)
    draw_text(c, "(e) 11, 22, 33, _____, 55", c1 + 10, qy - 64, fontsize=10)
    
    draw_box(c, c2, curr_y - h_p2_4, col_w, h_p2_4, "प्र. 16: दिमागी कसरत (Mental Math)", "[5 अंक]")
    draw_text(c, "(a) 100 + 50 = ______", c2 + 10, qy, fontsize=10)
    draw_text(c, "(b) 500 में 1 जोड़ने पर? ______", c2 + 10, qy - 16, fontsize=10)
    draw_text(c, "(c) 1 सप्ताह में कितने दिन? ______", c2 + 10, qy - 32, fontsize=10)
    draw_text(c, "(d) 20 के 3 नोट = ______ रु", c2 + 10, qy - 48, fontsize=10)
    draw_text(c, "(e) 10 में से 10 गया = ______", c2 + 10, qy - 64, fontsize=10)
    
    draw_text(c, "*** परीक्षा समाप्त (Good Luck) ***", width/2, curr_y - h_p2_4 - 25, fontsize=11, align='center')
    
    draw_footer(c, width, 2)
    c.save()
    print(f"Created: {OUTPUT_FILENAME}")

if __name__ == "__main__":
    create_paper()