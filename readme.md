# OCR2Metadata

**OCR2Metadata** is a local Python utility that transforms your static image collection into a fully searchable database directly within Windows File Explorer.

By recursively scanning folders and embedding Optical Character Recognition (OCR) data directly into image files, this tool allows you to find documents, screenshots, and photos simply by typing keywords into your PC's search bar.

## What It Does

* **Recursive Scanning:** detailed scan of a specified directory and all its sub-folders for image files (`.jpg`, `.jpeg`, `.png`).
* **AI-Powered OCR:** Uses PaddleOCR to perform high-accuracy text recognition on each image.
* **Metadata Embedding:** Automatically saves the extracted text into the image's metadata (the "Comments" field for JPEGs and "Description" for PNGs).
* **Search Integration:** Once processed, you can find any image by searching for its text content (names, dates, ID numbers) using the standard Windows File Explorer search.

## Features
* **Privacy First:** Runs 100% locally on your machine. No images are uploaded to the cloud.
* **Smart Resume:** Automatically skips images that have already been processed to save time.
* **Auto-Organize:** If you are looking for specific keywords (like "Registration" or "Invoice"), the script can automatically copy matches to a `Found_Documents` folder for quick access.
* **Windows Compatible:** Specifically formatted to ensure metadata is readable by the Windows operating system.

## Prerequisites

1.  **Python 3.8 - 3.10** (Recommended).
    * *Note: Ensure you check "Add Python to PATH" during installation.*
2.  A folder of images you want to index.

## Installation

1.  **Clone or Download** this repository.
2.  Open a terminal (Command Prompt) inside the project folder.
3.  Install the required dependencies using the specific versions provided (crucial for stability):
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  Open `app.py` in any text editor (Notepad, VS Code, etc.).
2.  Edit the **USER CONFIGURATION** section at the top:
    ```python
    # 1. Enter the path to the folder you want to scan
    INPUT_FOLDER_PATH = r"C:\Users\YourName\Pictures\Documents"

    # 2. (Optional) Enter keywords to auto-detect important files
    WATCHLIST = ["invoice", "receipt", "insurance", "visa"]
    BIKE_NUMBER = "XX-00-1234" 
    ```
3.  Run the script:
    ```bash
    python app.py
    ```
4.  Once finished, open your folder in Windows File Explorer and try searching for text inside your images!

## Troubleshooting

* **"Unimplemented / PIR Error"**: This happens if you install the wrong version of PaddlePaddle. Please ensure you use `pip install -r requirements.txt` to get the stable, compatible versions (v2.6).
* **Can't see text in PNGs?**: Windows File Explorer often hides metadata for PNG files in the "Details" tab, but the Windows Search Indexer can still read it. For full visibility, use tools like digiKam or ExifTool.

---

### Why I Built This
I created this tool because I lost my **Bike's Registration Certificate (RC)**. I knew I had a photo of it somewhere in my backup of 2,000+ WhatsApp images, but finding it manually was impossible. I built this script to read every single image for me, and it successfully found the document in minutes.
