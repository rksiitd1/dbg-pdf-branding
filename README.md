# DBG Gurukulam - PDF Automation & Exam Paper Generator

This repository contains a collection of Python scripts designed to automate the branding of existing educational PDFs and generate high-quality exam papers (Maths, Hindi, English) from scratch. 

The project focuses on precise layout control, automated watermarking, and solving complex text rendering issues with Indic scripts (Hindi Sanyuktakshars) in Python.

## 🚀 Features

### 1. PDF Branding Automation
*   **Watermarking:** Adds a centered, semi-transparent logo watermark behind the content on every page.
*   **Header Injection:** Places dual logos ("DBG Gurukulam" and "Divya Bihar Mission") on the top corners of specific pages.
*   **Footer Injection:** Adds page numbers, copyright text, and website links automatically to every page.
*   **Transparency Handling:** Uses pixel-level alpha manipulation to ensure watermarks do not obscure existing text.

### 2. Exam Paper Generation
*   **Dynamic Layouts:** Generates A4 exam papers with 2-column layouts, rounded question boxes, and grey headers.
*   **Maths Alignment:** Automatically aligns vertical addition, subtraction, and multiplication problems.
*   **Hindi Support:** Multiple approaches implemented to handle Hindi font rendering, including complex conjuncts (Sanyuktakshars).

## 📂 Repository Structure

```text
├── assets/
│   ├── DBG-logo.png               # Primary Logo / Watermark
│   ├── DBM-logo.png               # Secondary Logo
│   ├── Nirmala.ttf                # Windows Hindi Font
│   └── NotoSansDevanagari.ttf     # Google Hindi Font (Recommended)
├── branding/
│   └── branding_v2.py             # Script to brand existing PDFs (LKG/UKG/Class 4)
├── generators/
│   ├── generate_class1_final.py   # ReportLab vector-based PDF generator
│   ├── generate_perfect_hindi.py  # PIL-based image generation for crisp Hindi
│   └── generate_html_paper.py     # HTML-to-PDF generator (Best for Hindi)
├── branded_output/                # Folder where branded PDFs are saved
└── README.md                      # Project Documentation
```

## 🛠️ Installation & Prerequisites

This project requires Python 3.x. Install the dependencies using pip:

```bash
pip install pymupdf reportlab Pillow
```

*   **PyMuPDF (fitz):** Used for manipulating existing PDFs (Branding).
*   **ReportLab:** Used for drawing PDFs from scratch.
*   **Pillow (PIL):** Used for image processing and advanced text rendering.

## 📖 Usage Guide

### 1. Branding Existing PDFs
Use this script to add headers, footers, and watermarks to existing PDF files (e.g., `Maths Bodh Manthan II Class 4.pdf`).

1.  Place your source PDFs in the root directory.
2.  Run the script:
    ```bash
    python branding/branding_v2.py
    ```
3.  The branded files will appear in the `branded_output` folder.

### 2. Generating Exam Papers (The Hindi Challenge)
We implemented three approaches to generate the Class 1 Math Paper due to Hindi rendering complexity.

#### Approach A: ReportLab (Vector)
*   **Script:** `generate_class1_final.py`
*   **Pros:** Small file size, selectable text.
*   **Cons:** Standard libraries often struggle with Hindi "Matras" and "Halants".
*   **Run:** `python generators/generate_class1_final.py`

#### Approach B: Pillow (Image-based Text)
*   **Script:** `generate_perfect_hindi.py`
*   **Pros:** Renders Hindi exactly like Windows/Word (No broken Sanyuktakshars).
*   **Cons:** Text is not selectable (it is an image pasted onto the PDF).
*   **Run:** `python generators/generate_perfect_hindi.py`

#### Approach C: HTML to PDF (⭐ Recommended)
*   **Script:** `generate_html_paper.py`
*   **Pros:** **Perfect** Hindi rendering, perfect layout, easiest to style with CSS.
*   **How to use:**
    1.  Run `python generators/generate_html_paper.py`.
    2.  Open the generated `.html` file in **Google Chrome** or **Edge**.
    3.  Press `Ctrl + P` (Print).
    4.  Select **"Save as PDF"**.
    5.  **Important:** Under "More Settings", check **"Background graphics"** to see the grey headers.

## 🐛 Known Issues & Solved Challenges

### 1. The "Invisible Text" Issue
*   **Problem:** In ReportLab, text inside filled boxes was invisible.
*   **Solution:** The fill color was set to white for the box background but not reset to black for the text. Added `c.setFillColor(colors.black)` before writing text.

### 2. The "Unnecessary Halant" (Sanyuktakshar) Issue
*   **Problem:** `क्ष` rendering as `क`+`्`+`ष`.
*   **Reason:** Python's PDF libraries often lack complex text shaping engines.
*   **Solution:** The HTML-to-PDF approach delegates rendering to the web browser, which handles Indic scripts perfectly.

### 3. Watermark Opacity
*   **Problem:** Drawing a white box with opacity over a logo obscured the text underneath.
*   **Solution:** Used `Pillow` to modify the Alpha channel of the PNG image itself (making it 15% visible) before inserting it into the PDF.

## 👨‍🏫 Credits

*   **Organization:** DBG Gurukulam & Shri Classes
*   **Developer:** @rksiitd1 and gemini 3 pro
*   **Website:** [dbggurukulam.com](https://dbggurukulam.com)

---
*Note: Ensure required fonts (Nirmala.ttf or Noto Sans) are present in the root directory for the Python scripts to function correctly.*