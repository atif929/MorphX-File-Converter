import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar,
    QListWidget, QListWidgetItem, QFileDialog, QPlainTextEdit,
    QMessageBox, QLineEdit, QSplitter,
    QStatusBar, QFrame, QMenu, QApplication, QSizePolicy,
    QButtonGroup, QScrollArea, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap

from app.config import APP_NAME, APP_VERSION, CONVERSION_MAP, DEFAULT_OUTPUT_DIR
from app.ui.drop_zone import DropZone
from app.ui.flow_layout import FlowLayout
from app.utils.file_utils import get_extension, open_folder
from main import get_resource_path

from PyQt6.QtWidgets import QStyledItemDelegate, QStyle
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPainter, QTextOption

from PyQt6.QtCore import QRectF # new import for wrap around function



class FormatChip(QPushButton):
    def __init__(self, label: str, parent=None):
        super().__init__(label, parent)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("formatChip")
        self.setFixedHeight(28)





from PyQt6.QtWidgets import QStyledItemDelegate, QStyle
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPainter, QTextOption

class WrappingItemDelegate(QStyledItemDelegate):
    """Allows QListWidget items to wrap text onto multiple lines."""

    def paint(self, painter: QPainter, option, index):
        painter.save()

        # Draw selection/hover background
        self.initStyleOption(option, index)
        style = option.widget.style()
        style.drawPrimitive(
            QStyle.PrimitiveElement.PE_PanelItemViewItem,
            option, painter, option.widget
        )

        # Draw wrapped text
        text = index.data(Qt.ItemDataRole.DisplayRole) or ""
        text_rect = option.rect.adjusted(6, 5, -6, -5)
        painter.setPen(option.palette.color(option.palette.ColorRole.Text)
                       if not (option.state & QStyle.StateFlag.State_Selected)
                       else option.palette.color(option.palette.ColorRole.HighlightedText))

        text_option = QTextOption()
        text_option.setWrapMode(QTextOption.WrapMode.WordWrap)
        # painter.drawText(text_rect, text, text_option)
        painter.drawText(QRectF(text_rect), text, text_option)

        painter.restore()

    def sizeHint(self, option, index):
        self.initStyleOption(option, index)
        text = index.data(Qt.ItemDataRole.DisplayRole) or ""
        width = option.rect.width() if option.rect.width() > 0 else 300

        from PyQt6.QtGui import QFontMetrics
        fm = QFontMetrics(option.font)
        # Calculate wrapped height
        text_width = width - 12
        bounding = fm.boundingRect(
            0, 0, text_width, 10000,
            int(Qt.TextFlag.TextWordWrap),
            text
        )
        height = max(bounding.height() + 14, 34)
        return QSize(width, height)





class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"About {APP_NAME}")
        self.setFixedSize(420, 320)
        self.setObjectName("aboutDialog")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 20)
        layout.setSpacing(12)

        title = QLabel(APP_NAME)
        title.setObjectName("aboutTitle")
        layout.addWidget(title)

        version = QLabel(f"Version {APP_VERSION}")
        version.setObjectName("aboutVersion")
        layout.addWidget(version)

        desc = QLabel("Lightweight offline file converter for Windows.\nNo internet required. No data leaves your machine.")
        desc.setObjectName("aboutDesc")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("divider")
        layout.addWidget(sep)

        fmt_title = QLabel("Supported Formats")
        fmt_title.setObjectName("aboutSection")
        layout.addWidget(fmt_title)

        fmt_text = QLabel(
            "Documents: PDF · DOCX · PPTX · PPT\n"
            "Images: JPG · PNG · JPEG · WEBP · BMP · TIFF · GIF · ICO"
        )
        fmt_text.setObjectName("aboutDesc")
        fmt_text.setWordWrap(True)
        layout.addWidget(fmt_text)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setObjectName("divider")
        layout.addWidget(sep2)

        github = QLabel('GitHub: <a href="https://github.com/atif929/MorphX-File-Converter" style="color:#4F8CFF;">atif929/MorphX-File-Converter</a>')
        github.setOpenExternalLinks(True)
        github.setObjectName("aboutDesc")
        layout.addWidget(github)

        license_lbl = QLabel("License: MIT")
        license_lbl.setObjectName("aboutDesc")
        layout.addWidget(license_lbl)

        layout.addStretch()

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        btns.accepted.connect(self.accept)
        btns.button(QDialogButtonBox.StandardButton.Ok).setObjectName("secondaryBtn")
        layout.addWidget(btns)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.output_dir = DEFAULT_OUTPUT_DIR
        self.worker = None
        self._chip_group = QButtonGroup(self)
        self._chip_group.setExclusive(True)
        self._chip_group.buttonClicked.connect(self._update_convert_button)
        self._init_window()
        self._init_ui()
        self._apply_stylesheet()

    # ── Window ────────────────────────────────────────────────────────────────

    def _init_window(self):
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(900, 620)
        self.resize(1060, 720)

    # ── UI ────────────────────────────────────────────────────────────────────

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_header())

        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 16)
        content_layout.setSpacing(16)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(1)
        splitter.addWidget(self._build_left_panel())
        splitter.addWidget(self._build_right_panel())
        splitter.setSizes([480, 520])
        content_layout.addWidget(splitter)
        root.addWidget(content, stretch=1)

        root.addWidget(self._build_bottom_bar())

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    # ── Header ────────────────────────────────────────────────────────────────

    def _build_header(self) -> QWidget:
        frame = QFrame()
        frame.setObjectName("appHeader")
        frame.setFixedHeight(52)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(0)

        # Logo
        icon_path = get_resource_path("assets/icon.ico")
        if os.path.exists(icon_path):
            logo = QLabel()
            pix = QPixmap(icon_path).scaled(
                24, 24,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo.setPixmap(pix)
            logo.setFixedSize(24, 24)
            layout.addWidget(logo)
            layout.addSpacing(10)

        # Title + tagline stacked vertically
        brand_widget = QWidget()
        brand_widget.setObjectName("brandBlock")
        brand_layout = QVBoxLayout(brand_widget)
        brand_layout.setContentsMargins(0, 0, 0, 0)
        brand_layout.setSpacing(1)

        title = QLabel(APP_NAME)
        title.setObjectName("appTitle")
        tagline = QLabel("Lightweight Offline File Converter")
        tagline.setObjectName("appTagline")

        brand_layout.addWidget(title)
        brand_layout.addWidget(tagline)
        layout.addWidget(brand_widget)

        layout.addStretch()

        btn_about = QPushButton("About")
        btn_about.setObjectName("ghostBtn")
        btn_about.setFixedHeight(28)
        btn_about.clicked.connect(self._show_about)
        layout.addWidget(btn_about)

        return frame

    def _show_about(self):
        dlg = AboutDialog(self)
        dlg.setStyleSheet(self.styleSheet())
        dlg.exec()

    # ── Left Panel ────────────────────────────────────────────────────────────

    def _build_left_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 10, 0)
        layout.setSpacing(12)

        # Drop zone
        drop_lbl = QLabel("INPUT FILES")
        drop_lbl.setObjectName("sectionLabel")
        layout.addWidget(drop_lbl)

        self.drop_zone = DropZone()
        self.drop_zone.files_dropped.connect(self._on_files_added)
        layout.addWidget(self.drop_zone)

        # File list
        files_lbl = QLabel("SELECTED FILES")
        files_lbl.setObjectName("sectionLabel")
        layout.addWidget(files_lbl)

        # edited lines for wrap around of selected files in the list widget
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.file_list.setWordWrap(True)
        self.file_list.setItemDelegate(WrappingItemDelegate(self.file_list))

        self.file_list.setObjectName("fileList")
        self.file_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self._file_list_context_menu)
        self.file_list.setMinimumHeight(120)
        layout.addWidget(self.file_list, stretch=1)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self.btn_remove = QPushButton("Remove Selected")
        self.btn_remove.setObjectName("secondaryBtn")
        self.btn_remove.clicked.connect(self._remove_selected)
        self.btn_clear = QPushButton("Clear All")
        self.btn_clear.setObjectName("dangerBtn")
        self.btn_clear.clicked.connect(self._clear_all)
        btn_row.addWidget(self.btn_remove)
        btn_row.addWidget(self.btn_clear)
        layout.addLayout(btn_row)

        return panel

    # ── Right Panel ───────────────────────────────────────────────────────────

    def _build_right_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(16)

        # ── Convert To ──
        fmt_lbl = QLabel("CONVERT TO")
        fmt_lbl.setObjectName("sectionLabel")
        layout.addWidget(fmt_lbl)

        self.chip_container = QWidget()
        self.chip_container.setObjectName("chipContainer")
        self.chip_container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self.chip_flow = FlowLayout(self.chip_container, h_spacing=8, v_spacing=8)
        layout.addWidget(self.chip_container)

        self.chip_placeholder = QLabel(
            "Drop or select a file to view available conversion formats."
        )
        self.chip_placeholder.setObjectName("placeholderLabel")
        self.chip_placeholder.setWordWrap(True)
        layout.addWidget(self.chip_placeholder)

        self._set_chip_placeholder()

        # ── Output Directory ──
        out_lbl = QLabel("OUTPUT DIRECTORY")
        out_lbl.setObjectName("sectionLabel")
        layout.addWidget(out_lbl)

        dir_row = QHBoxLayout()
        dir_row.setSpacing(6)
        self.output_dir_edit = QLineEdit(self.output_dir)
        self.output_dir_edit.setReadOnly(True)
        self.output_dir_edit.setToolTip(self.output_dir)
        self.output_dir_edit.setObjectName("pathEdit")

        self.btn_browse_dir = QPushButton("Browse")
        self.btn_browse_dir.setObjectName("secondaryBtn")
        self.btn_browse_dir.setFixedWidth(72)
        self.btn_browse_dir.clicked.connect(self._browse_output_dir)

        dir_row.addWidget(self.output_dir_edit)
        dir_row.addWidget(self.btn_browse_dir)
        layout.addLayout(dir_row)

        dir_actions = QHBoxLayout()
        dir_actions.setSpacing(6)
        self.btn_copy_path = QPushButton("Copy Path")
        self.btn_copy_path.setObjectName("secondaryBtn")
        self.btn_copy_path.clicked.connect(self._copy_output_path)

        self.btn_open_output = QPushButton("Open Folder")
        self.btn_open_output.setObjectName("secondaryBtn")
        self.btn_open_output.clicked.connect(lambda: open_folder(self.output_dir))

        dir_actions.addWidget(self.btn_copy_path)
        dir_actions.addWidget(self.btn_open_output)
        dir_actions.addStretch()
        layout.addLayout(dir_actions)

        # ── Progress ──
        prog_lbl = QLabel("PROGRESS")
        prog_lbl.setObjectName("sectionLabel")
        layout.addWidget(prog_lbl)

        prog_inner = QVBoxLayout()
        prog_inner.setSpacing(5)

        self.progress_label = QLabel("Idle")
        self.progress_label.setObjectName("progressLabel")
        prog_inner.addWidget(self.progress_label)

        bar_row = QHBoxLayout()
        bar_row.setSpacing(8)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(5)
        self.progress_pct = QLabel("0%")
        self.progress_pct.setObjectName("progressPct")
        self.progress_pct.setFixedWidth(36)
        self.progress_pct.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        bar_row.addWidget(self.progress_bar)
        bar_row.addWidget(self.progress_pct)
        prog_inner.addLayout(bar_row)
        layout.addLayout(prog_inner)

        # ── Activity Log ──
        log_lbl = QLabel("ACTIVITY LOG")
        log_lbl.setObjectName("sectionLabel")
        layout.addWidget(log_lbl)

        self.log_output = QPlainTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setObjectName("logOutput")
        self.log_output.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.log_output.customContextMenuRequested.connect(self._log_context_menu)
        self.log_output.setPlaceholderText("Activity will appear here...")
        self.log_output.setMinimumHeight(100)
        layout.addWidget(self.log_output, stretch=1)

        return panel

    # ── Bottom Bar ────────────────────────────────────────────────────────────

    def _build_bottom_bar(self) -> QWidget:
        frame = QFrame()
        frame.setObjectName("bottomBar")
        frame.setFixedHeight(54)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(8)

        layout.addStretch()

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setObjectName("dangerBtn")
        self.btn_cancel.setFixedHeight(32)
        self.btn_cancel.setFixedWidth(88)
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.clicked.connect(self._cancel_conversion)

        self.btn_convert = QPushButton("Convert")
        self.btn_convert.setObjectName("primaryBtn")
        self.btn_convert.setFixedHeight(32)
        self.btn_convert.setFixedWidth(110)
        self.btn_convert.setEnabled(False)
        self.btn_convert.clicked.connect(self._start_conversion)

        layout.addWidget(self.btn_cancel)
        layout.addWidget(self.btn_convert)
        return frame

    # ── File Handling ─────────────────────────────────────────────────────────

    def _on_files_added(self, paths: list):
        added = False
        for path in paths:
            if path not in self.selected_files:
                self.selected_files.append(path)
                ext = get_extension(path)
                name = os.path.basename(path)
                item = QListWidgetItem(f"  {name}    [{ext}]")
                item.setData(Qt.ItemDataRole.UserRole, path)
                item.setToolTip(path)
                self.file_list.addItem(item)
                added = True

        if added:
            self._refresh_chips()
            self._update_convert_button()
            n = len(self.selected_files)
            self.status_bar.showMessage(
                f"{n} file{'s' if n != 1 else ''} selected."
            )

    def _remove_selected(self):
        for item in self.file_list.selectedItems():
            path = item.data(Qt.ItemDataRole.UserRole)
            if path in self.selected_files:
                self.selected_files.remove(path)
            self.file_list.takeItem(self.file_list.row(item))
        self._refresh_chips()
        self._update_convert_button()
        n = len(self.selected_files)
        self.status_bar.showMessage(
            f"{n} file{'s' if n != 1 else ''} selected." if n else "Ready"
        )

    def _clear_all(self):
        self.selected_files.clear()
        self.file_list.clear()
        self._refresh_chips()
        self._update_convert_button()
        self.status_bar.showMessage("Ready")

    # ── Context Menus ─────────────────────────────────────────────────────────

    def _file_list_context_menu(self, pos):
        item = self.file_list.itemAt(pos)
        if not item:
            return
        path = item.data(Qt.ItemDataRole.UserRole)
        menu = QMenu(self)
        a_remove = menu.addAction("Remove File")
        a_location = menu.addAction("Open File Location")
        a_copy = menu.addAction("Copy File Path")
        action = menu.exec(self.file_list.viewport().mapToGlobal(pos))
        if action == a_remove:
            if path in self.selected_files:
                self.selected_files.remove(path)
            self.file_list.takeItem(self.file_list.row(item))
            self._refresh_chips()
            self._update_convert_button()
        elif action == a_location:
            import subprocess
            subprocess.Popen(f'explorer /select,"{os.path.normpath(path)}"')
        elif action == a_copy:
            QApplication.clipboard().setText(path)
            self.status_bar.showMessage("File path copied.")

    def _log_context_menu(self, pos):
        menu = QMenu(self)
        a_copy = menu.addAction("Copy")
        a_all = menu.addAction("Select All")
        menu.addSeparator()
        a_clear = menu.addAction("Clear Log")
        action = menu.exec(self.log_output.viewport().mapToGlobal(pos))
        if action == a_copy:
            self.log_output.copy()
        elif action == a_all:
            self.log_output.selectAll()
        elif action == a_clear:
            self.log_output.clear()

    # ── Format Chips ──────────────────────────────────────────────────────────

    def _clear_chips(self):
        for btn in self._chip_group.buttons():
            self._chip_group.removeButton(btn)
        while self.chip_flow.count():
            item = self.chip_flow.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

    def _set_chip_placeholder(self):
        self._clear_chips()
        self.chip_container.setVisible(False)
        self.chip_placeholder.setVisible(True)
        self.chip_container.setEnabled(False)

    def _get_selected_format(self) -> str:
        checked = self._chip_group.checkedButton()
        return checked.text() if checked else ""

    def _refresh_chips(self):
        if not self.selected_files:
            self._set_chip_placeholder()
            return

        common_targets = None
        for path in self.selected_files:
            ext = get_extension(path)
            targets = set(CONVERSION_MAP.get(ext, []))
            common_targets = targets if common_targets is None else common_targets & targets

        previous = self._get_selected_format()
        self._clear_chips()

        if common_targets:
            self.chip_placeholder.setVisible(False)
            self.chip_container.setVisible(True)
            self.chip_container.setEnabled(True)
            for i, fmt in enumerate(sorted(common_targets)):
                chip = FormatChip(fmt)
                self._chip_group.addButton(chip, i)
                self.chip_flow.addWidget(chip)
                if fmt == previous:
                    chip.setChecked(True)
            if not self._chip_group.checkedButton() and self._chip_group.buttons():
                self._chip_group.buttons()[0].setChecked(True)
        else:
            self.chip_container.setVisible(False)
            self.chip_placeholder.setText("No common output format available for the selected files.")
            self.chip_placeholder.setVisible(True)
            self.chip_container.setEnabled(False)

    # ── Convert Button State ──────────────────────────────────────────────────

    def _update_convert_button(self):
        self.btn_convert.setEnabled(
            bool(self.selected_files)
            and self.chip_container.isEnabled()
            and self._get_selected_format() != ""
        )

    # ── Output Directory ──────────────────────────────────────────────────────

    def _browse_output_dir(self):
        path = QFileDialog.getExistingDirectory(
            self, "Select Output Directory", self.output_dir
        )
        if path:
            self.output_dir = path
            self.output_dir_edit.setText(path)
            self.output_dir_edit.setToolTip(path)

    def _copy_output_path(self):
        QApplication.clipboard().setText(self.output_dir)
        self.status_bar.showMessage("Output path copied.")

    # ── Conversion ────────────────────────────────────────────────────────────

    def _start_conversion(self):
        target_format = self._get_selected_format()
        if not target_format:
            QMessageBox.warning(self, "No Format", "Please select a target format.")
            return

        self.log_output.clear()
        self.progress_bar.setValue(0)
        self.progress_pct.setText("0%")
        self.btn_convert.setEnabled(False)
        self.btn_cancel.setEnabled(True)
        self.progress_label.setText("Preparing conversion...")
        self.status_bar.showMessage("Converting...")

        from app.ui.workers import ConversionWorker
        self.worker = ConversionWorker(
            files=list(self.selected_files),
            target_format=target_format,
            output_dir=self.output_dir
        )
        self.worker.progress.connect(self._on_progress)
        self.worker.file_done.connect(self._on_file_done)
        self.worker.file_error.connect(self._on_file_error)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _cancel_conversion(self):
        if self.worker:
            self.worker.cancel()
            self.progress_label.setText("Cancelling...")
            self.status_bar.showMessage("Cancellation requested.")

    # ── Worker Signals ────────────────────────────────────────────────────────

    def _on_progress(self, value: int):
        self.progress_bar.setValue(value)
        self.progress_pct.setText(f"{value}%")
        if value < 100:
            self.progress_label.setText("Converting...")

    def _on_file_done(self, input_path: str, output_paths: list):
        ts = datetime.now().strftime("%H:%M:%S")
        name = os.path.basename(input_path)
        for out in output_paths:
            self.log_output.appendPlainText(
                f"[{ts}] ✔  {name}  →  {os.path.basename(out)}"
            )

    def _on_file_error(self, input_path: str, error: str):
        ts = datetime.now().strftime("%H:%M:%S")
        name = os.path.basename(input_path)
        self.log_output.appendPlainText(f"[{ts}] ✘  {name}  —  {error}")

    def _on_finished(self, success: int, failed: int):
        ts = datetime.now().strftime("%H:%M:%S")
        self.btn_convert.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        self.progress_bar.setValue(100)
        self.progress_pct.setText("100%")
        self.progress_label.setText(
            f"Done — {success} succeeded, {failed} failed."
        )
        self.status_bar.showMessage(
            f"Complete — {success} succeeded, {failed} failed."
        )
        self.log_output.appendPlainText(
            f"[{ts}] {'Complete.' if failed == 0 else f'Completed with {failed} error(s).'}"
        )

        if failed == 0:
            QMessageBox.information(
                self, "Conversion Complete",
                f"All {success} file(s) converted successfully.\n\nOutput saved to:\n{self.output_dir}"
            )
        else:
            QMessageBox.warning(
                self, "Completed with Errors",
                f"{success} succeeded, {failed} failed.\nCheck the log for details."
            )

    # ── Stylesheet ────────────────────────────────────────────────────────────

    def _apply_stylesheet(self):
        self.setStyleSheet("""

        /* ── Base ── */
        QMainWindow, QWidget {
            background-color: #1E1E1E;
            color: #E6E6E6;
            font-family: "Segoe UI";
            font-size: 12px;
        }

        /* ── Header ── */
        QFrame#appHeader {
            background-color: #252526;
            border-bottom: 1px solid #3A3D41;
        }
        QWidget#brandBlock {
            background-color: transparent;
        }
        QLabel#appTitle {
            font-size: 13px;
            font-weight: 700;
            color: #E6E6E6;
            background-color: transparent;
        }
        QLabel#appTagline {
            font-size: 10px;
            color: #6B7280;
            background-color: transparent;
        }
        QFrame#headerSep {
            color: #3A3D41;
            max-height: 18px;
        }

        /* ── Bottom Bar ── */
        QFrame#bottomBar {
            background-color: #252526;
            border-top: 1px solid #3A3D41;
        }

        /* ── Splitter ── */
        QSplitter::handle {
            background-color: #3A3D41;
            width: 1px;
        }

        /* ── Section Labels ── */
        QLabel#sectionLabel {
            font-size: 10px;
            font-weight: 700;
            color: #6B7280;
            letter-spacing: 1px;
        }

        /* ── Dividers ── */
        QFrame#divider {
            color: #3A3D41;
            max-height: 1px;
        }

        /* ── File List ── */
        QListWidget#fileList {
            background-color: #252526;
            border: 1px solid #3A3D41;
            border-radius: 6px;
            color: #E6E6E6;
            outline: none;
            font-size: 12px;
            padding: 3px;
        }
        QListWidget#fileList::item {
            padding: 7px 8px;
            border-radius: 4px;
            color: #D1D5DB;
        }
        QListWidget#fileList::item:selected {
            background-color: #1e3a5f;
            color: #4F8CFF;
        }
        QListWidget#fileList::item:hover {
            background-color: #2A2D2E;
        }

        /* ── Chip Container ── */
        QWidget#chipContainer {
            background-color: transparent;
        }

        /* ── Format Chips ── */
        QPushButton#formatChip {
            background-color: #2D2D2D;
            color: #9CA3AF;
            border: 1px solid #3A3D41;
            border-radius: 5px;
            padding: 4px 14px;
            font-size: 11px;
            font-weight: 600;
            min-width: 52px;
        }
        QPushButton#formatChip:hover {
            background-color: #1e3050;
            border-color: #4F8CFF;
            color: #93C5FD;
        }
        QPushButton#formatChip:checked {
            background-color: #1e3a6e;
            border-color: #4F8CFF;
            color: #4F8CFF;
        }

        /* ── Placeholder ── */
        QLabel#placeholderLabel {
            color: #6B7280;
            font-size: 11px;
            font-style: italic;
        }

        /* ── Path Edit ── */
        QLineEdit#pathEdit {
            background-color: #252526;
            border: 1px solid #3A3D41;
            border-radius: 5px;
            padding: 6px 10px;
            color: #D1D5DB;
            font-size: 11px;
        }
        QLineEdit#pathEdit:focus {
            border-color: #4F8CFF;
        }

        /* ── Progress ── */
        QLabel#progressLabel {
            color: #9CA3AF;
            font-size: 11px;
        }
        QLabel#progressPct {
            color: #4F8CFF;
            font-size: 10px;
            font-weight: 600;
        }
        QProgressBar {
            background-color: #3A3D41;
            border: none;
            border-radius: 2px;
        }
        QProgressBar::chunk {
            background-color: #4F8CFF;
            border-radius: 2px;
        }

        /* ── Log ── */
        QPlainTextEdit#logOutput {
            background-color: #1a1a1a;
            border: 1px solid #3A3D41;
            border-radius: 6px;
            color: #9CA3AF;
            font-family: "Consolas", "Courier New", monospace;
            font-size: 11px;
            padding: 8px;
            selection-background-color: #1e3a5f;
        }

        /* ── Primary Button ── */
        QPushButton#primaryBtn {
            background-color: #4F8CFF;
            color: #ffffff;
            border: none;
            border-radius: 5px;
            font-size: 12px;
            font-weight: 600;
            padding: 6px 16px;
        }
        QPushButton#primaryBtn:hover {
            background-color: #5B9CFF;
        }
        QPushButton#primaryBtn:pressed {
            background-color: #3a7aee;
        }
        QPushButton#primaryBtn:disabled {
            background-color: #2D2D2D;
            color: #4B5563;
            border: 1px solid #3A3D41;
        }

        /* ── Danger Button ── */
        QPushButton#dangerBtn {
            background-color: transparent;
            color: #F87171;
            border: 1px solid #3A3D41;
            border-radius: 5px;
            font-size: 12px;
            font-weight: 600;
            padding: 6px 16px;
        }
        QPushButton#dangerBtn:hover {
            background-color: #2d1a1a;
            border-color: #F85149;
            color: #F85149;
        }
        QPushButton#dangerBtn:pressed {
            background-color: #3d2020;
        }
        QPushButton#dangerBtn:disabled {
            color: #4B5563;
            border-color: #3A3D41;
        }

        /* ── Secondary Button ── */
        QPushButton#secondaryBtn {
            background-color: #2D2D2D;
            color: #D1D5DB;
            border: 1px solid #3A3D41;
            border-radius: 5px;
            font-size: 12px;
            font-weight: 500;
            padding: 6px 14px;
        }
        QPushButton#secondaryBtn:hover {
            background-color: #333333;
            border-color: #4F8CFF;
            color: #93C5FD;
        }
        QPushButton#secondaryBtn:pressed {
            background-color: #252526;
        }

        /* ── Ghost Button (About) ── */
        QPushButton#ghostBtn {
            background-color: transparent;
            color: #6B7280;
            border: 1px solid transparent;
            border-radius: 5px;
            font-size: 11px;
            font-weight: 500;
            padding: 4px 10px;
        }
        QPushButton#ghostBtn:hover {
            color: #D1D5DB;
            border-color: #3A3D41;
        }

        /* ── About Dialog ── */
        QDialog#aboutDialog {
            background-color: #252526;
        }
        QLabel#aboutTitle {
            font-size: 16px;
            font-weight: 700;
            color: #E6E6E6;
        }
        QLabel#aboutVersion {
            font-size: 11px;
            color: #4F8CFF;
        }
        QLabel#aboutSection {
            font-size: 11px;
            font-weight: 600;
            color: #9CA3AF;
            letter-spacing: 0.5px;
        }
        QLabel#aboutDesc {
            font-size: 11px;
            color: #9CA3AF;
            line-height: 1.5;
        }

        /* ── Status Bar ── */
        QStatusBar {
            background-color: #252526;
            color: #6B7280;
            border-top: 1px solid #3A3D41;
            font-size: 11px;
        }

        /* ── Scrollbar ── */
        QScrollBar:vertical {
            background: #1E1E1E;
            width: 5px;
            border-radius: 2px;
        }
        QScrollBar::handle:vertical {
            background: #3A3D41;
            border-radius: 2px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background: #4F8CFF;
        }
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical { height: 0; }

        /* ── Context Menu ── */
        QMenu {
            background-color: #252526;
            border: 1px solid #3A3D41;
            border-radius: 6px;
            padding: 4px;
            color: #E6E6E6;
            font-size: 12px;
        }
        QMenu::item {
            padding: 6px 18px;
            border-radius: 4px;
        }
        QMenu::item:selected {
            background-color: #1e3050;
            color: #93C5FD;
        }
        QMenu::separator {
            height: 1px;
            background-color: #3A3D41;
            margin: 3px 8px;
        }

        """)