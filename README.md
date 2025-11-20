# DBG Gurukulam - PDF Branding Automation

This repository contains the tools used to automate the branding of educational materials for **DBG Gurukulam**. 

**⚠️ IMPORTANT:** 
The core production script is **`branding.py`**. 
All other scripts (exam generators, HTML converters) are for **experimentation and testing purposes only**.

---

## 🚀 The Main Tool: `branding.py`

This script is the production-ready tool used to stamp existing PDFs with the official branding.

### Features
1.  **Watermarking:** Adds a semi-transparent (30% visibility) logo in the center of **every page**. It uses advanced Alpha-channel processing to ensure the watermark doesn't make text unreadable.
2.  **Header Injection:** Places the **DBG Gurukulam** logo (Left) and **Divya Bihar Mission** logo (Right) on the top corners of **every page**.
3.  **Footer Injection:** Adds a standardized footer containing:
    *   Page Numbers (`Page X of Y`)
    *   Branding Text (`Shri Classes & DBG Gurukulam...`)
    *   Website Link (`dbggurukulam.com`)

### 📂 Required File Structure
Ensure your directory looks like this before running the script:

```text
├── branding.py                # <--- THE MAIN SCRIPT
├── DBG-logo.png               # Required for Watermark & Left Header
├── DBM-logo.png               # Required for Right Header
├── input_file_1.pdf           # Your PDF to be branded
└── input_file_2.pdf           # Another PDF...
```

### 🛠️ Installation & Setup
1.  **Install Dependencies:**
    You need `PyMuPDF` (for PDF editing) and `Pillow` (for image transparency).
    ```bash
    pip install pymupdf Pillow
    ```

2.  **Configuration:**
    Open `branding.py` to adjust settings if needed:
    ```python
    TARGET_FILES = [
        "Maths Class 1.pdf", 
        "Maths Class LKG.pdf" 
    ]
    # You can add any PDF filename inside this list.
    ```

### ▶️ How to Run
1.  Open this folder in VS Code or Terminal.
2.  Run the script:
    ```bash
    python branding.py
    ```
3.  The script will process the files and create a new folder named **`branded_output/`** containing the final files.

---

## 🧪 Experimental Scripts (Reference Only)

The following scripts are **not** part of the main branding workflow. They were created to experiment with generating Exam Papers from scratch using Python code.

*   **`generate_class1_final.py`**: An attempt to generate Class 1 Math papers using the *ReportLab* library. (Status: Functional, but Hindi font rendering is complex).
*   **`generate_perfect_hindi.py`**: An experiment using *Pillow* to turn text into images to fix "Sanyuktakshar" (halant) issues in Hindi.
*   **`generate_html_paper.py`**: A method to generate papers as HTML/CSS and convert them to PDF via browser print (Recommended method for perfect Hindi rendering if building papers from scratch).

---

## 👨‍💻 Credits
*   **Developed for:** DBG Gurukulam & Shri Classes
*   **Developer:** @rksiitd1 and gemini 3 pro