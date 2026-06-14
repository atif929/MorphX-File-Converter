import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor, QIcon
from app.config import APP_NAME
from app.utils.file_utils import ensure_output_dir


def main():
    # ── 1. TASKBAR ICON FIX FOR WINDOWS ─────────────────────────────────────
    # Tell Windows to treat this process as a unique standalone application
    # This MUST run before the QApplication is initialized!
    if sys.platform == "win32":
        import ctypes
        myappid = "mycompany.morphx.converter.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    # ────────────────────────────────────────────────────────────────────────

    # 2. Ensure internal folders exist
    ensure_output_dir()

    # 3. Initialize the application object
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyle("Fusion")

    # 4. Set light-theme window palette background properties
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 244, 255))
    app.setPalette(palette)

    # 5. Load your custom icon asset
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # 6. Load and show the window
    from app.ui.main_window import MainWindow
    window = MainWindow()
    window.show()

    # 7. Start the main event loop cleanly
    sys.exit(app.exec())


if __name__ == "__main__":
    main()