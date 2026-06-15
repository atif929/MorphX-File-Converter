import os
import comtypes.client
from app.utils.file_utils import build_output_path, ensure_output_dir
from app.config import DEFAULT_IMAGE_DPI, DEFAULT_IMAGE_QUALITY, POPPLER_PATH
from pdf2image import convert_from_path
from PIL import Image
from app.utils.file_utils import build_output_path_multi


def _abs(path: str) -> str:
    return os.path.abspath(path)


# ── DOCX conversions ──────────────────────────────────────────────────────────

def docx_to_pdf(input_path: str, output_path: str) -> str:
    word = comtypes.client.CreateObject("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(_abs(input_path))
        doc.SaveAs(_abs(output_path), FileFormat=17)
        doc.Close()
    finally:
        word.Quit()
    return output_path


def docx_to_pptx(input_path: str, output_path: str) -> str:
    # DOCX → PDF → PPTX (each page becomes a slide image)
    tmp_pdf = _abs(input_path).replace(".docx", "_tmp.pdf")
    docx_to_pdf(input_path, tmp_pdf)
    result = _pdf_to_pptx_internal(tmp_pdf, output_path)
    if os.path.exists(tmp_pdf):
        os.remove(tmp_pdf)
    return result


def docx_to_images(input_path: str, output_dir: str, target_format: str) -> list[str]:
    ensure_output_dir(output_dir)
    tmp_pdf = _abs(input_path).replace(".docx", "_tmp.pdf")
    docx_to_pdf(input_path, tmp_pdf)
    result = _pdf_to_images_internal(tmp_pdf, input_path, output_dir, target_format)
    if os.path.exists(tmp_pdf):
        os.remove(tmp_pdf)
    return result


# ── PPTX conversions ──────────────────────────────────────────────────────────

def pptx_to_pdf(input_path: str, output_path: str) -> str:
    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    powerpoint.Visible = 1
    try:
        prs = powerpoint.Presentations.Open(_abs(input_path), WithWindow=False)
        prs.SaveAs(_abs(output_path), 32)
        prs.Close()
    finally:
        powerpoint.Quit()
    return output_path


def pptx_to_docx(input_path: str, output_path: str) -> str:
    # PPTX → PDF → DOCX via Word COM (best fidelity available without paid API)
    tmp_pdf = _abs(input_path).replace(".pptx", "_tmp.pdf")
    pptx_to_pdf(input_path, tmp_pdf)
    result = _pdf_to_docx_internal(tmp_pdf, output_path)
    if os.path.exists(tmp_pdf):
        os.remove(tmp_pdf)
    return result


def pptx_to_images(input_path: str, output_dir: str, target_format: str) -> list[str]:
    ensure_output_dir(output_dir)
    tmp_pdf = _abs(input_path).replace(".pptx", "_tmp.pdf")
    pptx_to_pdf(input_path, tmp_pdf)
    result = _pdf_to_images_internal(tmp_pdf, input_path, output_dir, target_format)
    if os.path.exists(tmp_pdf):
        os.remove(tmp_pdf)
    return result


# ── Shared internal helpers ───────────────────────────────────────────────────

def _pdf_to_images_internal(
    pdf_path: str,
    original_input: str,
    output_dir: str,
    target_format: str
) -> list[str]:
    images = convert_from_path(pdf_path, dpi=DEFAULT_IMAGE_DPI, poppler_path=POPPLER_PATH)
    saved = []
    fmt = target_format.upper()
    pil_format = "JPEG" if fmt in ("JPG", "JPEG") else fmt

    for i, img in enumerate(images, start=1):
        out_path = build_output_path_multi(original_input, target_format, output_dir, i)
        if pil_format == "JPEG":
            img = img.convert("RGB")
        img.save(out_path, format=pil_format, quality=DEFAULT_IMAGE_QUALITY)
        saved.append(out_path)

    return saved


def _pdf_to_pptx_internal(pdf_path: str, output_path: str) -> str:
    from pptx import Presentation
    from pptx.util import Inches

    images = convert_from_path(pdf_path, dpi=DEFAULT_IMAGE_DPI, poppler_path=POPPLER_PATH)
    prs = Presentation()
    prs.slide_width  = Inches(10)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    for i, img in enumerate(images):
        slide = prs.slides.add_slide(blank_layout)
        tmp_img = pdf_path + f"_slide{i}.png"
        img.save(tmp_img, format="PNG")
        slide.shapes.add_picture(tmp_img, Inches(0), Inches(0), Inches(10), Inches(7.5))
        os.remove(tmp_img)

    prs.save(output_path)
    return output_path


def _pdf_to_docx_internal(pdf_path: str, output_path: str) -> str:
    from pdf2docx import Converter as DocxConverter
    cv = DocxConverter(pdf_path)
    cv.convert(output_path, start=0, end=None)
    cv.close()
    return output_path