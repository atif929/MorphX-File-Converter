import os
import shutil
from app.config import DEFAULT_OUTPUT_DIR


def ensure_output_dir(path: str = DEFAULT_OUTPUT_DIR) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def get_extension(filepath: str) -> str:
    return os.path.splitext(filepath)[1].lstrip(".").upper()


def get_filename_without_ext(filepath: str) -> str:
    return os.path.splitext(os.path.basename(filepath))[0]


def build_output_path(input_path: str, target_format: str, output_dir: str) -> str:
    name = get_filename_without_ext(input_path)
    ext = target_format.lower()
    output_path = os.path.join(output_dir, f"{name}.{ext}")
    counter = 1
    while os.path.exists(output_path):
        output_path = os.path.join(output_dir, f"{name}_{counter}.{ext}")
        counter += 1
    return output_path


def build_output_path_multi(input_path: str, target_format: str, output_dir: str, index: int) -> str:
    name = get_filename_without_ext(input_path)
    ext = target_format.lower()
    return os.path.join(output_dir, f"{name}_page{index}.{ext}")


def validate_file(filepath: str) -> tuple[bool, str]:
    if not filepath:
        return False, "No file path provided."
    if not os.path.exists(filepath):
        return False, f"File not found: {filepath}"
    if not os.path.isfile(filepath):
        return False, f"Path is not a file: {filepath}"
    if os.path.getsize(filepath) == 0:
        return False, f"File is empty: {filepath}"
    return True, ""


def open_folder(path: str) -> None:
    import subprocess
    subprocess.Popen(f'explorer "{os.path.normpath(path)}"')