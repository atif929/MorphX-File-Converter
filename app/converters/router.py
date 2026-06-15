import os
from app.config import CONVERSION_MAP
from app.utils.file_utils import (
    get_extension,
    build_output_path,
    ensure_output_dir,
    validate_file,
)


def get_supported_targets(input_path: str) -> list[str]:
    ext = get_extension(input_path)
    return CONVERSION_MAP.get(ext, [])


def convert(input_path: str, target_format: str, output_dir: str) -> list[str]:
    valid, err = validate_file(input_path)
    if not valid:
        raise FileNotFoundError(err)

    ensure_output_dir(output_dir)
    src_fmt = get_extension(input_path)
    tgt_fmt = target_format.upper()

    if tgt_fmt not in CONVERSION_MAP.get(src_fmt, []):
        raise ValueError(f"Conversion from {src_fmt} to {tgt_fmt} is not supported.")

    # ── PDF source ────────────────────────────────────────────────────────────
    if src_fmt == "PDF":
        if tgt_fmt == "DOCX":
            from app.converters.pdf_converter import pdf_to_docx
            out = build_output_path(input_path, tgt_fmt, output_dir)
            return [pdf_to_docx(input_path, out)]

        elif tgt_fmt == "PPTX":
            from app.converters.pdf_converter import pdf_to_pptx
            out = build_output_path(input_path, tgt_fmt, output_dir)
            return [pdf_to_pptx(input_path, out)]

        elif tgt_fmt in ("JPG", "PNG", "JPEG"):
            from app.converters.pdf_converter import pdf_to_images
            return pdf_to_images(input_path, output_dir, tgt_fmt)

    # ── DOCX source ───────────────────────────────────────────────────────────
    elif src_fmt == "DOCX":
        if tgt_fmt == "PDF":
            from app.converters.office_converter import docx_to_pdf
            out = build_output_path(input_path, tgt_fmt, output_dir)
            return [docx_to_pdf(input_path, out)]

        elif tgt_fmt == "PPTX":
            from app.converters.office_converter import docx_to_pptx
            out = build_output_path(input_path, tgt_fmt, output_dir)
            return [docx_to_pptx(input_path, out)]

        elif tgt_fmt in ("JPG", "PNG", "JPEG"):
            from app.converters.office_converter import docx_to_images
            return docx_to_images(input_path, output_dir, tgt_fmt)

    # ── PPTX source ───────────────────────────────────────────────────────────
    elif src_fmt == "PPTX":
        if tgt_fmt == "PDF":
            from app.converters.office_converter import pptx_to_pdf
            out = build_output_path(input_path, tgt_fmt, output_dir)
            return [pptx_to_pdf(input_path, out)]

        elif tgt_fmt == "DOCX":
            from app.converters.office_converter import pptx_to_docx
            out = build_output_path(input_path, tgt_fmt, output_dir)
            return [pptx_to_docx(input_path, out)]

        elif tgt_fmt in ("JPG", "PNG", "JPEG"):
            from app.converters.office_converter import pptx_to_images
            return pptx_to_images(input_path, output_dir, tgt_fmt)

    # ── Image source ──────────────────────────────────────────────────────────
    elif src_fmt in ("JPG", "PNG", "JPEG"):
        if tgt_fmt == "PDF":
            from app.converters.image_converter import image_to_pdf
            out = build_output_path(input_path, tgt_fmt, output_dir)
            return [image_to_pdf(input_path, out)]

        elif tgt_fmt == "PPTX":
            from app.converters.image_converter import image_to_pptx
            out = build_output_path(input_path, tgt_fmt, output_dir)
            return [image_to_pptx(input_path, out)]

        elif tgt_fmt == "DOCX":
            from app.converters.image_converter import image_to_docx
            out = build_output_path(input_path, tgt_fmt, output_dir)
            return [image_to_docx(input_path, out)]

        elif tgt_fmt in ("JPG", "PNG", "JPEG"):
            from app.converters.image_converter import image_to_image
            out = build_output_path(input_path, tgt_fmt, output_dir)
            return [image_to_image(input_path, out, tgt_fmt)]

    raise ValueError(f"Unhandled conversion: {src_fmt} → {tgt_fmt}")