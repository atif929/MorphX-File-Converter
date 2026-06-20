import os
from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QDragLeaveEvent
from app.config import SUPPORTED_FORMATS


class DropZone(QLabel):
    files_dropped = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(140)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._set_idle_style()

    def _set_idle_style(self):
        self.setText("Drop files here\n\nor click to browse")
        self.setStyleSheet("""
            QLabel {
                border: 1.5px dashed #3A3D41;
                border-radius: 8px;
                background-color: #252526;
                color: #A9B1BA;
                font-size: 13px;
                font-family: "Segoe UI";
                padding: 20px;
            }
        """)

    def _set_hover_style(self):
        self.setText("Release to add files")
        self.setStyleSheet("""
            QLabel {
                border: 1.5px dashed #4F8CFF;
                border-radius: 8px;
                background-color: #1a2a3a;
                color: #4F8CFF;
                font-size: 13px;
                font-family: "Segoe UI";
                font-weight: 600;
                padding: 20px;
            }
        """)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self._set_hover_style()
        else:
            event.ignore()

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self._set_idle_style()

    def dropEvent(self, event: QDropEvent):
        self._set_idle_style()
        urls = event.mimeData().urls()
        paths = []
        for url in urls:
            path = url.toLocalFile()
            ext = os.path.splitext(path)[1].lstrip(".").upper()
            if ext in SUPPORTED_FORMATS and os.path.isfile(path):
                paths.append(path)
        if paths:
            self.files_dropped.emit(paths)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            from PyQt6.QtWidgets import QFileDialog
            exts = " ".join(f"*.{f.lower()}" for f in SUPPORTED_FORMATS)
            files, _ = QFileDialog.getOpenFileNames(
                self, "Select Files", "",
                f"Supported Files ({exts});;All Files (*)"
            )
            if files:
                self.files_dropped.emit(files)