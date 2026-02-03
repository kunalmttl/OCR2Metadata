import os
import shutil

import piexif
import piexif.helper
from paddleocr import PaddleOCR
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from tqdm import tqdm

# ==========================================
#        USER CONFIGURATION AREA
# ==========================================

# 1. PATH TO SCAN
# Replace the path below with the folder containing your images.
# Example: r"C:\Users\John\Pictures\WhatsApp Images"
INPUT_FOLDER_PATH = r"C:\Path\To\Your\Images"

# 2. SEARCH TARGETS
# The bike number or keywords you are looking for
BIKE_NUMBER = "AN01J 8844"
WATCHLIST = [
    "registration",
    "certificate",
    "chassis",
    "engine",
    "owner",
    "form 23",
    "transport",
]

# 3. SETTINGS
# Set to True if you want to re-scan images that already have metadata
FORCE_REPROCESS = False

# ==========================================
#      END CONFIGURATION (DO NOT EDIT)
# ==========================================

# --- SYSTEM FIXES FOR PADDLEOCR ---
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"
os.environ["FLAGS_enable_pir_api"] = (
    "0"  # Disables experimental engine (prevents crashes)
)
os.environ["FLAGS_use_mkldnn"] = "0"  # Disables C++ accelerator conflicts

# Setup Output Path
BASE_DIR = os.getcwd()
FOUND_FOLDER = os.path.join(BASE_DIR, "Found_Documents")

# Initialize OCR Engine
# Using specific flags for stability on Windows
ocr = PaddleOCR(lang="en", use_angle_cls=True, enable_mkldnn=False, show_log=False)


def has_existing_metadata(img_path):
    """Checks if file already has OCR data to skip it."""
    if FORCE_REPROCESS:
        return False
    try:
        img = Image.open(img_path)
        if img_path.lower().endswith(".png"):
            if "Description" in img.info or "Comment" in img.info:
                return True
        elif "exif" in img.info:
            exif_dict = piexif.load(img.info["exif"])
            if exif_dict["Exif"].get(piexif.ExifIFD.UserComment):
                return True
    except:
        pass
    return False


def process_images():
    valid_extensions = (".jpg", ".jpeg", ".png")

    if not os.path.exists(INPUT_FOLDER_PATH):
        print(f"[ERROR] The folder path does not exist: {INPUT_FOLDER_PATH}")
        print("Please edit 'INPUT_FOLDER_PATH' inside app.py")
        return

    if not os.path.exists(FOUND_FOLDER):
        os.makedirs(FOUND_FOLDER)

    all_files = []
    print(f"[INFO] Scanning folder: {INPUT_FOLDER_PATH}")
    for root, dirs, files in os.walk(INPUT_FOLDER_PATH):
        for file in files:
            if file.lower().endswith(valid_extensions):
                all_files.append(os.path.join(root, file))

    if not all_files:
        print("[ERROR] No images found. Check your path.")
        return

    print(f"[INFO] Found {len(all_files)} images. Processing...")

    for img_path in tqdm(all_files, desc="OCR Scan", unit="img"):
        file_name = os.path.basename(img_path)

        if has_existing_metadata(img_path):
            continue

        try:
            # 1. OCR
            result = ocr.ocr(img_path)
            if not result or not result[0]:
                continue

            extracted_text = " ".join([line[1][0] for line in result[0]])
            clean_text = extracted_text.lower()

            # 2. SEARCH
            searchable_bike = BIKE_NUMBER.lower().replace(" ", "")
            searchable_content = clean_text.replace(" ", "")

            is_match = False
            if searchable_bike in searchable_content:
                is_match = True
            elif any(word in clean_text for word in WATCHLIST):
                is_match = True

            if is_match:
                shutil.copy(img_path, os.path.join(FOUND_FOLDER, f"MATCH_{file_name}"))

            # 3. WRITE METADATA
            temp_path = img_path + ".tmp"
            img = Image.open(img_path)

            if img_path.lower().endswith(".png"):
                metadata = PngInfo()
                metadata.add_text("Description", extracted_text)
                metadata.add_text("Comment", extracted_text)
                img.save(temp_path, "PNG", pnginfo=metadata)

            elif img_path.lower().endswith((".jpg", ".jpeg")):
                user_comment = piexif.helper.UserComment.dump(
                    extracted_text, encoding="unicode"
                )
                try:
                    exif_dict = piexif.load(img.info.get("exif", b""))
                except:
                    exif_dict = {
                        "0th": {},
                        "Exif": {},
                        "GPS": {},
                        "1st": {},
                        "thumbnail": None,
                    }

                exif_dict["Exif"][piexif.ExifIFD.UserComment] = user_comment
                exif_bytes = piexif.dump(exif_dict)
                img.save(temp_path, "JPEG", exif=exif_bytes, quality=95)

            img.close()
            os.replace(temp_path, img_path)

        except Exception as e:
            # print(f"[ERROR] Failed on {file_name}: {e}")
            continue


if __name__ == "__main__":
    process_images()
    print("\n" + "=" * 50)
    print("DONE! Check the 'Found_Documents' folder.")
    print("=" * 50)
    input("Press Enter to exit...")
