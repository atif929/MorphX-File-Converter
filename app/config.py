import os
<<<<<<< HEAD
import sys

APP_NAME = "MorphX"
APP_VERSION = "1.0.0"
=======

APP_NAME = "MorphX"
APP_VERSION = " "
>>>>>>> d26ac61649f2aceacca66d74e9b1b5fe3600d0f0
APP_AUTHOR = "Atif"

SUPPORTED_FORMATS = ["PDF", "DOCX", "PPTX", "JPG", "PNG", "JPEG"]

CONVERSION_MAP = {
    "PDF":  ["DOCX", "PPTX", "JPG", "PNG", "JPEG"],
    "DOCX": ["PDF", "PPTX", "JPG", "PNG", "JPEG"],
    "PPTX": ["PDF", "DOCX", "JPG", "PNG", "JPEG"],
    "JPG":  ["PNG", "JPEG", "PDF", "DOCX", "PPTX"],
    "PNG":  ["JPG", "JPEG", "PDF", "DOCX", "PPTX"],
    "JPEG": ["JPG", "PNG", "PDF", "DOCX", "PPTX"],
}

<<<<<<< HEAD
DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "MorphX_Output")
DEFAULT_IMAGE_DPI = 200
DEFAULT_IMAGE_QUALITY = 95

# Dynamically resolve Poppler path — works both in dev and inside .exe
if getattr(sys, 'frozen', False):
    _BASE = sys._MEIPASS
else:
    _BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

POPPLER_PATH = os.path.join(_BASE, "poppler_bin")
=======
DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "FileConverter_Output")
DEFAULT_IMAGE_DPI = 200
DEFAULT_IMAGE_QUALITY = 95

POPPLER_PATH = r"E:\Python\AdvancePython\poppler-26.02.0\Library\bin"
>>>>>>> d26ac61649f2aceacca66d74e9b1b5fe3600d0f0
