import os
from PIL import Image
from app.utils.file_utils import build_output_path, ensure_output_dir
from app.config import DEFAULT_IMAGE_QUALITY
from pptx import Presentation
from pptx.util import Inches


def image_to_image(input_path: str, output_path: str, target_format: str) -> str:
    fmt = target_format.upper()
    pil_format = "JPEG" if fmt in ("JPG", "JPEG") else fmt

    with Image.open(input_path) as img:
        if pil_format == "JPEG" and img.mode in ("RGBA", "P", "LA"):
            img = img.convert("RGB")
        img.save(output_path, format=pil_format, quality=DEFAULT_IMAGE_QUALITY)

    return output_path


def image_to_pdf(input_path: str, output_path: str) -> str:
    with Image.open(input_path) as img:
        if img.mode in ("RGBA", "P", "LA"):
            img = img.convert("RGB")
        img.save(output_path, format="PDF", resolution=DEFAULT_IMAGE_QUALITY)
    return output_path


def image_to_pptx(input_path: str, output_path: str) -> str:
    prs = Presentation()
    prs.slide_width  = Inches(10)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.shapes.add_picture(input_path, Inches(0), Inches(0), Inches(10), Inches(7.5))
    prs.save(output_path)
    return output_path


def image_to_docx(input_path: str, output_path: str) -> str:
    from docx import Document
    from docx.shared import Inches as DocxInches
    doc = Document()
    doc.add_picture(input_path, width=DocxInches(6))
    doc.save(output_path)
    return output_path