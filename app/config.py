import os

APP_NAME = "MorphX"
APP_VERSION = " "
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

DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "FileConverter_Output")
DEFAULT_IMAGE_DPI = 200
DEFAULT_IMAGE_QUALITY = 95

POPPLER_PATH = r"E:\Python\AdvancePython\poppler-26.02.0\Library\bin"