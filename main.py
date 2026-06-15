import os
import sys
import multiprocessing

if getattr(sys, 'frozen', False):
    os.environ['COMTYPES_CACHE_DIR'] = os.path.join(
        os.path.expanduser("~"), "AppData", "Local", "MorphX", "comtypes_cache"
    )
    os.makedirs(os.environ['COMTYPES_CACHE_DIR'], exist_ok=True)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor, QIcon
from app.config import APP_NAME
from app.utils.file_utils import ensure_output_dir


def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    if sys.platform == "win32":
        import ctypes
        myappid = "mycompany.morphx.converter.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    ensure_output_dir()

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 244, 255))
    app.setPalette(palette)

    icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    from app.ui.main_window import MainWindow
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()