import os
import base64

# --- CONFIGURATION ---
OUTPUT_FILE = "Class_1_Exam_Final.html"
LOGO_LEFT = "DBG-logo.png"
LOGO_RIGHT = "DBM-logo.png"
WATERMARK = "DBG-logo.png"

# Helper to load images as Base64 so they are embedded in the HTML
def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
    return ""

# Load Images
img_left = get_base64_image(LOGO_LEFT)
img_right = get_base64_image(LOGO_RIGHT)
img_watermark = get_base64_image(WATERMARK)

# --- HTML CONTENT ---
html_content = f"""
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <title>Class 1 Exam Paper</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;700&display=swap');
        
        body {{
            font-family: 'Noto Sans Devanagari', 'Nirmala UI', sans-serif;
            margin: 0;
            padding: 0;
            background: white;
            -webkit-print-color-adjust: exact; /* Force print colors */
            print-color-adjust: exact;
        }}

        /* A4 Paper Setup */
        .page {{
            width: 210mm;
            height: 296mm;
            padding: 15mm;
            box-sizing: border-box;
            position: relative;
            margin: 0 auto;
            page-break-after: always;
            overflow: hidden; /* Prevent spillover */
        }}

        /* Watermark */
        .watermark {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 400px;
            opacity: 0.1;
            z-index: 0;
            pointer-events: none;
        }}

        /* Header */
        .header {{
            position: relative;
            text-align: center;
            z-index: 2;
            margin-bottom: 10px;
        }}
        .logo {{
            position: absolute;
            top: 0;
            width: 70px;
            height: 70px;
            object-fit: contain;
        }}
        .logo.left {{ left: 0; }}
        .logo.right {{ right: 0; }}
        
        h1 {{ margin: 0; font-size: 24px; text-transform: uppercase; }}
        .sub-header {{ margin: 5px 0; font-size: 12px; font-weight: bold; }}
        
        .student-info {{
            border: 1px solid black;
            padding: 5px 10px;
            margin-top: 10px;
            font-size: 11px;
            display: flex;
            justify-content: space-between;
        }}

        .marks-row {{
            border-bottom: 1px solid black;
            padding: 5px 0;
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            font-weight: bold;
            margin-bottom: 10px;
        }}

        /* Grid Layout for Questions */
        .grid-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            z-index: 2;
            position: relative;
        }}

        .full-width {{
            grid-column: span 2;
        }}

        /* Question Box Styling */
        .q-box {{
            border: 1px solid black;
            border-radius: 6px;
            overflow: hidden; /* Clips content to corners */
            background: white;
            font-size: 11px;
            height: fit-content;
        }}

        .q-header {{
            background-color: #ececec;
            border-top: 1px solid black; /* Styling trick for bottom header */
            padding: 4px 8px;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            border-bottom: none; /* We put header at bottom in design? No, usually top. */
        }}
        
        /* Replicating the specific design: Header is actually at the BOTTOM of the box in standard HTML flow, 
           but visually usually at top. Let's stick to standard Top Header for cleaner HTML, 
           OR use Flexbox to push it to bottom if strictly needed. 
           Based on screenshot, Header is at TOP with Marks. */
           
        .q-header {{
            background-color: #e0e0e0;
            border-bottom: 1px solid black;
            padding: 5px 10px;
        }}

        .q-content {{
            padding: 10px;
            min-height: 80px;
        }}

        .math-row {{
            display: flex;
            justify-content: space-around;
            font-size: 14px;
            font-family: sans-serif; /* Aligns numbers better */
        }}
        
        .math-item {{
            text-align: right;
            width: 50px;
        }}
        
        .math-line {{
            border-top: 1.5px solid black;
            margin-top: 2px;
        }}

        .footer {{
            position: absolute;
            bottom: 15mm;
            left: 15mm;
            right: 15mm;
            border-top: 1px solid #ccc;
            padding-top: 5px;
            display: flex;
            justify-content: space-between;
            font-size: 10px;
            color: #333;
        }}
        
        a {{ color: blue; text-decoration: none; }}

    </style>
</head>
<body>

    <!-- PAGE 1 -->
    <div class="page">
        <img src="{img_watermark}" class="watermark">
        
        <div class="header">
            <img src="{img_left}" class="logo left">
            <h1>DBG Gurukulam</h1>
            <div class="sub-header">कक्षा : 1 (First) &nbsp;&nbsp;|&nbsp;&nbsp; विषय: गणित (Maths) &nbsp;&nbsp;|&nbsp;&nbsp; समय: 2 घंटे</div>
            <img src="{img_right}" class="logo right">
            
            <div class="student-info">
                <span>नाम: _____________________________</span>
                <span>रोल नं: _______</span>
                <span>दिनांक: _______</span>
            </div>
            
            <div class="marks-row">
                <span>Total Questions: 16</span>
                <span>पूर्णांक (Max Marks): 80</span>
            </div>
        </div>

        <div class="grid-container">
            
            <!-- Q1 -->
            <div class="q-box">
                <div class="q-header">
                    <span>प्र. 1: शब्दों में लिखें (Words)</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content">
                    (a) 75 : ______________________<br><br>
                    (b) 89 : ______________________<br><br>
                    (c) 46 : ______________________<br><br>
                    (d) 99 : ______________________<br><br>
                    (e) 29 : ______________________
                </div>
            </div>

            <!-- Q2 -->
            <div class="q-box">
                <div class="q-header">
                    <span>प्र. 2: स्थानीय मान (Place Value)</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content">
                    (a) 540 में 5 का मान: _________<br><br>
                    (b) 892 में 9 का मान: _________<br><br>
                    (c) 1000 में 1 का मान: ________<br><br>
                    (d) 607 में 7 का मान: _________<br><br>
                    (e) 4550 में 0 का मान: ________
                </div>
            </div>

            <!-- Q3 -->
            <div class="q-box full-width">
                <div class="q-header">
                    <span>प्र. 3: जोड़ें (Addition)</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content math-row">
                    <div class="math-item">4230<br>+ 1540<div class="math-line"></div></div>
                    <div class="math-item">6525<br>+ 2354<div class="math-line"></div></div>
                    <div class="math-item">5005<br>+ 4990<div class="math-line"></div></div>
                    <div class="math-item">1234<br>+ 4321<div class="math-line"></div></div>
                </div>
            </div>

            <!-- Q4 -->
            <div class="q-box full-width">
                <div class="q-header">
                    <span>प्र. 4: घटाएँ (Subtraction)</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content math-row">
                    <div class="math-item">8956<br>- 4523<div class="math-line"></div></div>
                    <div class="math-item">5640<br>- 2310<div class="math-line"></div></div>
                    <div class="math-item">9000<br>- 1000<div class="math-line"></div></div>
                    <div class="math-item">7550<br>- 2550<div class="math-line"></div></div>
                </div>
            </div>

            <!-- Q5 -->
            <div class="q-box">
                <div class="q-header">
                    <span>प्र. 5: विस्तारित रूप (Expanded Form)</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content">
                    (a) 5426 = 5000 + 400 + 20 + 6<br><br>
                    (b) 3250 = ____ + ____ + ____ + 0<br><br>
                    (c) 7085 = ____ + 00 + ____ + 5<br><br>
                    (d) 1200 = 1000 + ____ + 00 + 0<br><br>
                    (e) 4040 = ____ + 0 + ____ + 0
                </div>
            </div>

            <!-- Q6 -->
            <div class="q-box">
                <div class="q-header">
                    <span>प्र. 6: गुणा करें (Multiply)</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content math-row" style="padding-top:20px;">
                    <div class="math-item">24<br>x 2<div class="math-line"></div></div>
                    <div class="math-item">33<br>x 3<div class="math-line"></div></div>
                    <div class="math-item">12<br>x 4<div class="math-line"></div></div>
                    <div class="math-item">40<br>x 2<div class="math-line"></div></div>
                </div>
            </div>

            <!-- Q7 -->
            <div class="q-box">
                <div class="q-header">
                    <span>प्र. 7: चिन्ह लगाएँ (<, >, =)</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content" style="display: flex; flex-wrap: wrap; justify-content: space-between;">
                    <div style="width:48%; margin-bottom:10px;">4500 [___] 5400</div>
                    <div style="width:48%; margin-bottom:10px;">8000 [___] 8000</div>
                    <div style="width:48%; margin-bottom:10px;">2020 [___] 2002</div>
                    <div style="width:48%; margin-bottom:10px;">500 [___] 50</div>
                    <div style="width:100%;">1010 [___] 1001</div>
                </div>
            </div>

            <!-- Q8 -->
            <div class="q-box">
                <div class="q-header">
                    <span>प्र. 8: भाग दें (Division)</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content" style="line-height: 1.8;">
                    (a) 20 ÷ 2 = ______ &nbsp;&nbsp; (b) 15 ÷ 3 = ______<br>
                    (c) 16 ÷ 4 = ______ &nbsp;&nbsp; (d) 10 ÷ 5 = ______<br>
                    (e) 30 ÷ 3 = ______
                </div>
            </div>
        </div>

        <div class="footer">
            <span>Page 1</span>
            <span>Shri Classes & DBG Gurukulam (by IITian Golu Sir)</span>
            <a href="https://dbggurukulam.com">https://dbggurukulam.com</a>
        </div>
    </div>

    <!-- PAGE 2 -->
    <div class="page">
        <img src="{img_watermark}" class="watermark">

        <div class="header">
            <h2>DBG Gurukulam</h2>
            <div class="sub-header">गणित - भाग 2 (Page 2)</div>
            <hr>
        </div>

        <div class="grid-container">
            
            <!-- Q9 -->
            <div class="q-box">
                <div class="q-header">
                    <span>प्र. 9: बढ़ते क्रम (Increasing Order)</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content">
                    (a) 500, 200, 800, 100<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&rarr; ____, ____, ____, ____<br><br>
                    (b) 10, 50, 30, 20, 40<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&rarr; ____, ____, ____, ____, ____
                </div>
            </div>

            <!-- Q10 -->
            <div class="q-box">
                <div class="q-header">
                    <span>प्र. 10: घटते क्रम (Decreasing Order)</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content">
                    (a) 45, 90, 12, 65<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&rarr; ____, ____, ____, ____<br><br>
                    (b) 88, 11, 55, 33, 77<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&rarr; ____, ____, ____, ____, ____
                </div>
            </div>

            <!-- Q11 -->
            <div class="q-box">
                <div class="q-header">
                    <span>प्र. 11: पहले और बाद की संख्या</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content">
                    (a) ____ &larr; 500 &rarr; ____<br><br>
                    (b) ____ &larr; 1000 &rarr; ____<br><br>
                    (c) 99 के बाद: _____________<br><br>
                    (d) 50 से पहले: ____________
                </div>
            </div>

            <!-- Q12 -->
            <div class="q-box">
                <div class="q-header">
                    <span>प्र. 12: पहाड़ा और पैटर्न (Tables)</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content">
                    (a) 12 का पहाड़ा: 12, 24, ____, 48<br><br>
                    (b) 15 का पहाड़ा: 15, 30, ____, 60<br><br>
                    (c) 2 का पहाड़ा: 2, 4, 6, ____, 10<br><br>
                    (d) 10, 20, 30, ____, 50
                </div>
            </div>

            <!-- Q13 -->
            <div class="q-box">
                <div class="q-header">
                    <span>प्र. 13: हल करें (Word Problem)</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content">
                    राम के पास 2500 रुपये, श्याम के पास 1200 रुपये और मोहन के पास 100 रुपये हैं।<br>
                    तीनों के पास कुल कितने रुपये हैं?
                    <br><br><br>
                    <b>उत्तर:</b> ___________________________
                </div>
            </div>

            <!-- Q14 -->
            <div class="q-box">
                <div class="q-header">
                    <span>प्र. 14: हल करें (Word Problem)</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content">
                    एक स्कूल में 4500 बच्चे हैं। आज 500 बच्चे नहीं आए (Absent)। बताइये आज स्कूल में कितने बच्चे उपस्थित हैं?
                    <br><br><br>
                    <b>उत्तर:</b> ___________________________
                </div>
            </div>

            <!-- Q15 -->
            <div class="q-box">
                <div class="q-header">
                    <span>प्र. 15: पैटर्न पूरा करें</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content">
                    (a) 100, 200, 300, ______, 500<br><br>
                    (b) 5, 10, 15, ______, 25<br><br>
                    (c) A, B, C, ______, E<br><br>
                    (d) 2, 4, 8, 16, ______
                </div>
            </div>

            <!-- Q16 -->
            <div class="q-box">
                <div class="q-header">
                    <span>प्र. 16: दिमागी कसरत (Mental Math)</span>
                    <span>[5 अंक]</span>
                </div>
                <div class="q-content">
                    (a) 100 + 50 = ________<br><br>
                    (b) 500 में 1 जोड़ने पर? ________<br><br>
                    (c) 1 सप्ताह में कितने दिन? ________<br><br>
                    (d) 20 के 3 नोट = ________ रु
                </div>
            </div>

        </div>
        
        <div style="text-align: center; margin-top: 20px; font-weight: bold; font-size: 14px;">
            *** परीक्षा समाप्त (Good Luck) ***
        </div>

        <div class="footer">
            <span>Page 2</span>
            <span>Shri Classes & DBG Gurukulam (by IITian Golu Sir)</span>
            <a href="https://dbggurukulam.com">https://dbggurukulam.com</a>
        </div>
    </div>

</body>
</html>
"""

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully created: {OUTPUT_FILE}")
print("INSTRUCTIONS:")
print("1. Open this HTML file in Google Chrome or Microsoft Edge.")
print("2. Right-Click > Print (or Ctrl+P).")
print("3. Set Destination to 'Save as PDF'.")
print("4. IMPORTANT: Expand 'More Settings' and Check 'Background graphics'.")
print("5. Save. Your PDF will have perfect Hindi and layout.")