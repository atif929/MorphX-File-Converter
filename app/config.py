import os
import sys

APP_NAME = "MorphX"
APP_VERSION = "1.1.0"
APP_AUTHOR = "Atif"

SUPPORTED_FORMATS = ["PDF", "DOCX", "PPTX", "PPT", "JPG", "PNG", "JPEG", "WEBP", "BMP", "TIFF", "GIF", "ICO"]

CONVERSION_MAP = {
    "PDF":  ["DOCX", "PPTX", "JPG", "PNG", "JPEG"],
    "DOCX": ["PDF", "PPTX", "JPG", "PNG", "JPEG"],
    "PPTX": ["PDF", "DOCX", "JPG", "PNG", "JPEG"],
    "PPT":  ["PDF", "DOCX", "JPG", "PNG", "JPEG"],
    "JPG":  ["PNG", "JPEG", "PDF", "DOCX", "PPTX", "WEBP", "BMP", "TIFF"],
    "PNG":  ["JPG", "JPEG", "PDF", "DOCX", "PPTX", "WEBP", "BMP", "TIFF", "ICO"],
    "JPEG": ["JPG", "PNG", "PDF", "DOCX", "PPTX", "WEBP", "BMP", "TIFF"],
    "WEBP": ["PNG", "JPG", "JPEG", "BMP", "TIFF"],
    "BMP":  ["PNG", "JPG", "JPEG", "WEBP", "TIFF"],
    "TIFF": ["PNG", "JPG", "JPEG", "WEBP", "BMP"],
    "GIF":  ["PNG", "JPG", "JPEG"],
    "ICO":  ["PNG"],
}

DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "MorphX_Output")
DEFAULT_IMAGE_DPI = 200
DEFAULT_IMAGE_QUALITY = 95

if getattr(sys, 'frozen', False):
    _BASE = sys._MEIPASS
else:
    _BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

POPPLER_PATH = os.path.join(_BASE, "poppler_bin")