import fitz  # PyMuPDF
import os
import sys
import argparse

try:
    import tkinter as tk
    from tkinter import filedialog
except ImportError:
    tk = None
    filedialog = None

# Try to import colorama for beautiful colored output
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Fallback: no colors
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Back:
        BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""

# --- Configuration ---
APP_VERSION = "1.1"
APP_NAME = "PDF Page Reshuffling Tool"
APP_AUTHOR = "DBG Gurukulam"

def print_header():
    """Print beautiful header"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}╔{'═'*58}╗")
    print(f"{Fore.CYAN}{Style.BRIGHT}║ {APP_NAME.center(56)} ║")
    print(f"{Fore.CYAN}{Style.BRIGHT}║ {f'v{APP_VERSION} by {APP_AUTHOR}'.center(56)} ║")
    print(f"{Fore.CYAN}{Style.BRIGHT}╚{'═'*58}╝{Style.RESET_ALL}\n")

def print_success(message):
    """Print success message in green"""
    print(f"{Fore.GREEN}{Style.BRIGHT}✓ {message}{Style.RESET_ALL}")

def print_error(message):
    """Print error message in red"""
    print(f"{Fore.RED}{Style.BRIGHT}✗ ERROR: {message}{Style.RESET_ALL}")

def print_warning(message):
    """Print warning message in yellow"""
    print(f"{Fore.YELLOW}⚠ WARNING: {message}{Style.RESET_ALL}")

def print_info(message):
    """Print info message"""
    print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")

def print_prompt(message):
    """Print prompt message in magenta"""
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{message}{Style.RESET_ALL}", end="")

def display_pdf_info(doc, filepath):
    """Display PDF information"""
    file_size = os.path.getsize(filepath)
    size_mb = file_size / (1024 * 1024)
    
    print(f"{Fore.CYAN}{Style.BRIGHT}📄 PDF Information:{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}File:      {os.path.basename(filepath)}")
    print(f"   Path:      {os.path.dirname(filepath)}")
    print(f"   Pages:     {Fore.YELLOW}{Style.BRIGHT}{len(doc)}")
    print(f"   Size:      {Fore.YELLOW}{Style.BRIGHT}{size_mb:.2f} MB{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─'*30}{Style.RESET_ALL}\n")

def parse_page_sequence(sequence, total_pages):
    """
    Parse page sequence string into list of page indices (0-based).
    Supports formats:
    - Single pages: "5" or "1,3,5"
    - Ranges: "1-10" or "5-8"
    - Mixed: "1-5,10,15-20"
    - Special: "end" for last page
    """
    if not sequence or not sequence.strip():
        return None
    
    sequence = sequence.strip().lower()
    pages = []
    
    try:
        parts = sequence.split(',')
        for part in parts:
            part = part.strip()
            if not part: continue
            
            if part == 'end':
                pages.append(total_pages - 1)
            elif '-' in part:
                # Range
                range_parts = part.split('-')
                if len(range_parts) != 2:
                    raise ValueError(f"Invalid range format: {part}")
                
                start_str, end_str = range_parts
                start_str = start_str.strip()
                end_str = end_str.strip()
                
                start = int(start_str)
                if end_str == 'end':
                    end = total_pages
                else:
                    end = int(end_str)
                
                if start < 1 or end > total_pages or start > end:
                    print_error(f"Invalid range: {part} (Valid range: 1-{total_pages})")
                    return None
                
                pages.extend(range(start - 1, end))
            else:
                # Single page
                page = int(part)
                if page < 1 or page > total_pages:
                    print_error(f"Invalid page number: {page} (Valid: 1-{total_pages})")
                    return None
                pages.append(page - 1)
        
        return pages
    except ValueError as e:
        print_error(f"Invalid format in sequence: {sequence}. Use numbers, ranges (1-5), or 'end'.")
        return None

def swap_pages(doc, page1, page2):
    """Swap two pages in the PDF."""
    total_pages = len(doc)
    if not (1 <= page1 <= total_pages and 1 <= page2 <= total_pages):
        print_error(f"Page numbers must be between 1 and {total_pages}")
        return None
    
    if page1 == page2:
        print_warning("Source and target pages are the same. No change needed.")
        return doc
        
    idx1, idx2 = page1 - 1, page2 - 1
    new_doc = fitz.open()
    
    for i in range(total_pages):
        if i == idx1:
            new_doc.insert_pdf(doc, from_page=idx2, to_page=idx2)
        elif i == idx2:
            new_doc.insert_pdf(doc, from_page=idx1, to_page=idx1)
        else:
            new_doc.insert_pdf(doc, from_page=i, to_page=i)
            
    return new_doc

def reorder_pages(doc, page_sequence):
    """Reorder pages according to sequence."""
    new_doc = fitz.open()
    for idx in page_sequence:
        new_doc.insert_pdf(doc, from_page=idx, to_page=idx)
    return new_doc

def delete_pages(doc, pages_to_delete):
    """Delete specified pages."""
    delete_set = set(pages_to_delete)
    new_doc = fitz.open()
    for i in range(len(doc)):
        if i not in delete_set:
            new_doc.insert_pdf(doc, from_page=i, to_page=i)
    return new_doc

def rotate_pages(doc, pages_to_rotate, rotation):
    """Rotate specified pages."""
    rotate_set = set(pages_to_rotate)
    new_doc = fitz.open()
    for i in range(len(doc)):
        new_doc.insert_pdf(doc, from_page=i, to_page=i)
        if i in rotate_set:
            new_doc[i].set_rotation(rotation)
    return new_doc

def get_output_path(input_path, prefix="reshuffled_"):
    output_dir = os.path.dirname(input_path)
    base_name = os.path.basename(input_path)
    return os.path.join(output_dir, f"{prefix}{base_name}")

def run_interactive(input_path):
    # Open PDF
    try:
        doc = fitz.open(input_path)
    except Exception as e:
        print_error(f"Could not open PDF: {e}")
        return

    display_pdf_info(doc, input_path)
    
    while True:
        print(f"{Fore.YELLOW}{Style.BRIGHT}🔧 Select Operation:{Style.RESET_ALL}")
        print(f"   [1] {Fore.WHITE}Quick Swap (Swap two specific pages)")
        print(f"   [2] Custom Reorder (e.g. 1-5,10,6-9,11-end)")
        print(f"   [3] Delete Pages")
        print(f"   [4] Reverse All Pages")
        print(f"   [5] Rotate Pages")
        print(f"   [0] {Fore.RED}Exit{Style.RESET_ALL}")
        
        print_prompt("\nYour choice: ")
        choice = input().strip()
        
        if choice == '0': break
        
        result_doc = None
        prefix = "mod_"
        
        if choice == '1':
            print_info("\n-- Quick Swap Mode --")
            try:
                print_prompt(f"Enter first page number (1-{len(doc)}): ")
                p1 = int(input().strip())
                print_prompt(f"Enter second page number (1-{len(doc)}): ")
                p2 = int(input().strip())
                result_doc = swap_pages(doc, p1, p2)
                prefix = f"swapped_{p1}_{p2}_"
            except ValueError:
                print_error("Please enter valid numbers.")
                continue
                
        elif choice == '2':
            print_info("\n-- Custom Reorder Mode --")
            print_info("Format example: 1-10,15,12-14,11,16-end")
            print_prompt("New sequence: ")
            seq_str = input().strip()
            indices = parse_page_sequence(seq_str, len(doc))
            if indices:
                result_doc = reorder_pages(doc, indices)
                prefix = "reordered_"
                
        elif choice == '3':
            print_info("\n-- Delete Pages Mode --")
            print_prompt("Pages to delete: ")
            seq_str = input().strip()
            indices = parse_page_sequence(seq_str, len(doc))
            if indices:
                result_doc = delete_pages(doc, indices)
                prefix = "deleted_"

        elif choice == '4':
            print_info("\n-- Reversing All Pages --")
            indices = list(range(len(doc)-1, -1, -1))
            result_doc = reorder_pages(doc, indices)
            prefix = "reversed_"
            
        elif choice == '5':
            print_info("\n-- Rotate Pages Mode --")
            print_prompt("Pages to rotate: ")
            seq_str = input().strip()
            indices = parse_page_sequence(seq_str, len(doc))
            if indices:
                print_prompt("Rotation (90, 180, 270): ")
                try:
                    rot = int(input().strip())
                    if rot not in [90, 180, 270]:
                        print_error("Invalid rotation angle.")
                        continue
                    result_doc = rotate_pages(doc, indices, rot)
                    prefix = f"rotated_{rot}_"
                except ValueError:
                    print_error("Invalid input.")
                    continue
        
        if result_doc:
            output_path = get_output_path(input_path, prefix)
            print_prompt(f"Save as (Default: {os.path.basename(output_path)}): ")
            custom_name = input().strip()
            if custom_name:
                if not custom_name.lower().endswith(".pdf"): custom_name += ".pdf"
                output_path = os.path.join(os.path.dirname(input_path), custom_name)
            
            try:
                result_doc.save(output_path)
                print_success(f"File saved successfully: {output_path}")
                print_prompt("\nContinue with another operation on the ORIGINAL file? (y/n): ")
                if input().strip().lower() != 'y': break
            except Exception as e:
                print_error(f"Failed to save: {e}")
                
    doc.close()

def main():
    parser = argparse.ArgumentParser(description="Professional PDF Reshuffling Tool")
    parser.add_argument("input", nargs="?", help="Input PDF file path")
    parser.add_argument("--swap", nargs=2, type=int, metavar=("P1", "P2"), help="Swap two pages")
    parser.add_argument("--reorder", help="New page sequence (e.g. 1-10,15,12-end)")
    parser.add_argument("--output", help="Output file name")
    
    args = parser.parse_args()
    
    print_header()
    
    input_path = args.input
    
    if not input_path:
        if filedialog:
            print_info("Opening file selection dialog...")
            root = tk.Tk()
            root.withdraw()
            input_path = filedialog.askopenfilename(
                title="Select PDF File",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            root.destroy()
        
        if not input_path:
            print_prompt("Enter PDF file path: ")
            input_path = input().strip().strip('"')
            
    if not input_path or not os.path.exists(input_path):
        print_error("No valid input file provided.")
        return

    if args.swap or args.reorder:
        try:
            doc = fitz.open(input_path)
            result_doc = None
            out_prefix = "res_"
            
            if args.swap:
                p1, p2 = args.swap
                print_info(f"Swapping page {p1} and {p2}...")
                result_doc = swap_pages(doc, p1, p2)
                out_prefix = f"swapped_{p1}_{p2}_"
            elif args.reorder:
                print_info(f"Reordering pages with sequence: {args.reorder}...")
                indices = parse_page_sequence(args.reorder, len(doc))
                if indices:
                    result_doc = reorder_pages(doc, indices)
                    out_prefix = "reordered_"
            
            if result_doc:
                output_path = args.output or get_output_path(input_path, out_prefix)
                result_doc.save(output_path)
                print_success(f"Done! Saved to: {output_path}")
            doc.close()
        except Exception as e:
            print_error(f"CLI execution failed: {e}")
    else:
        run_interactive(input_path)

    print(f"\n{Fore.GREEN}{Style.BRIGHT}Thank you for using {APP_NAME}!{Style.RESET_ALL}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}")
    except Exception as e:
        print_error(f"Unexpected error: {e}")
