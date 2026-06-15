import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QRadioButton, QButtonGroup,
    QListWidget, QListWidgetItem, QFileDialog,
    QMessageBox, QGroupBox, QLineEdit, QSplitter,
    QStatusBar, QFrame
)
from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QIcon, QFont, QColor

from app.config import APP_NAME, APP_VERSION, CONVERSION_MAP, DEFAULT_OUTPUT_DIR
from app.ui.drop_zone import DropZone
from app.utils.file_utils import get_extension, open_folder

# for icon
from main import get_resource_path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.output_dir = DEFAULT_OUTPUT_DIR
        self.worker = None
        self._init_window()
        self._init_ui()
        self._apply_stylesheet()

    # ── Window setup ──────────────────────────────────────────────────────────

    def _init_window(self):
        # I dont want to show the version with the name at this point    
        # self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}") 
        self.setWindowTitle(f"{APP_NAME}")
        self.setMinimumSize(860, 620)
        self.resize(980, 700)

    # ── UI Layout ─────────────────────────────────────────────────────────────

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)

        # Header
        root_layout.addWidget(self._build_header())

        # Main splitter: left panel + right panel
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._build_left_panel())
        splitter.addWidget(self._build_right_panel())
        splitter.setSizes([480, 460])
        root_layout.addWidget(splitter)

        # Bottom bar
        root_layout.addWidget(self._build_bottom_bar())

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready — drop files or click the drop zone to browse.")

    def _build_header(self) -> QWidget:
        frame = QFrame()
        frame.setObjectName("headerFrame")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)  # Keeps a clean gap between logo and text

        # 1. Create a dedicated label for your custom logo image
        logo_label = QLabel()
        logo_label.setObjectName("appLogo")
        
        # ── FIX: Use the secret finder to get the safe path to your icon ──
        icon_path = get_resource_path("assets/icon.ico")
        
        from PyQt6.QtGui import QPixmap
        if os.path.exists(icon_path):
            # Load the icon and scale it perfectly to match a clean font height (e.g., 24x24 pixels)
            pixmap = QPixmap(icon_path)
            scaled_pixmap = pixmap.scaled(46, 46, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        else:
            # Fallback text placeholder if the asset path is broken temporarily
            logo_label.setText("📁")
        # 2. Rebuild the app title without the raw string emoji
        title = QLabel(APP_NAME)
        title.setObjectName("appTitle")
        
        subtitle = QLabel("Convert PDF · DOCX · PPTX · JPG · PNG · JPEG")
        subtitle.setObjectName("appSubtitle")

        # Assemble the new components layout cleanly
        layout.addWidget(logo_label)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(subtitle)
        return frame

    def _build_left_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 8, 0)
        layout.setSpacing(10)

        # Drop zone
        drop_group = QGroupBox("Input Files")
        drop_layout = QVBoxLayout(drop_group)
        self.drop_zone = DropZone()
        self.drop_zone.files_dropped.connect(self._on_files_added)
        drop_layout.addWidget(self.drop_zone)
        layout.addWidget(drop_group)

        # File list
        list_group = QGroupBox("Selected Files")
        list_layout = QVBoxLayout(list_group)
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.file_list.setAlternatingRowColors(True)
        list_layout.addWidget(self.file_list)

        list_btns = QHBoxLayout()
        self.btn_remove = QPushButton("Remove Selected")
        self.btn_remove.setObjectName("secondaryBtn")
        self.btn_remove.clicked.connect(self._remove_selected)
        self.btn_clear = QPushButton("Clear All")
        self.btn_clear.setObjectName("dangerBtn")
        self.btn_clear.clicked.connect(self._clear_all)
        list_btns.addWidget(self.btn_remove)
        list_btns.addWidget(self.btn_clear)
        list_layout.addLayout(list_btns)
        layout.addWidget(list_group)

        return panel

    def _build_right_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 0, 0, 0)
        layout.setSpacing(10)

        # Conversion options
        opt_group = QGroupBox("Conversion Options")
        opt_layout = QVBoxLayout(opt_group)
        opt_layout.setContentsMargins(14, 14, 14, 14)
        opt_layout.setSpacing(10)

        fmt_label = QLabel("Convert To:")
        fmt_label.setObjectName("fieldLabel")
        opt_layout.addWidget(fmt_label)

        # Container using a clean horizontal flow/layout style to show options at once
        self.radio_container = QWidget()
        self.radio_container.setObjectName("radioContainer")
        self.radio_layout = QHBoxLayout(self.radio_container)
        self.radio_layout.setContentsMargins(0, 4, 0, 4)
        self.radio_layout.setSpacing(16)
        
        self.radio_group = QButtonGroup(self)
        self.radio_group.buttonClicked.connect(self._update_convert_button)

        opt_layout.addWidget(self.radio_container)
        
        # Initialize default state
        self._set_radio_placeholder("— select a file first —", enabled=False)
        layout.addWidget(opt_group)

        # Output directory
        out_group = QGroupBox("Output Directory")
        out_layout = QVBoxLayout(out_group)
        dir_row = QHBoxLayout()
        self.output_dir_edit = QLineEdit(self.output_dir)
        self.output_dir_edit.setReadOnly(True)
        self.btn_browse_dir = QPushButton("Browse")
        self.btn_browse_dir.setObjectName("secondaryBtn")
        self.btn_browse_dir.clicked.connect(self._browse_output_dir)
        dir_row.addWidget(self.output_dir_edit)
        dir_row.addWidget(self.btn_browse_dir)
        out_layout.addLayout(dir_row)

        self.btn_open_output = QPushButton("Open Output Folder")
        self.btn_open_output.setObjectName("secondaryBtn")
        self.btn_open_output.clicked.connect(lambda: open_folder(self.output_dir))
        out_layout.addWidget(self.btn_open_output)
        layout.addWidget(out_group)

        # Progress
        prog_group = QGroupBox("Progress")
        prog_layout = QVBoxLayout(prog_group)
        self.progress_label = QLabel("Idle")
        self.progress_label.setObjectName("progressLabel")
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        prog_layout.addWidget(self.progress_label)
        prog_layout.addWidget(self.progress_bar)
        layout.addWidget(prog_group)

        # Log
        log_group = QGroupBox("Conversion Log")
        log_layout = QVBoxLayout(log_group)
        self.log_list = QListWidget()
        self.log_list.setAlternatingRowColors(True)
        log_layout.addWidget(self.log_list)
        layout.addWidget(log_group)

        return panel

    def _build_bottom_bar(self) -> QWidget:
        frame = QFrame()
        frame.setObjectName("bottomBar")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)

        self.btn_convert = QPushButton("Convert")
        self.btn_convert.setObjectName("primaryBtn")
        self.btn_convert.setMinimumHeight(42)
        self.btn_convert.setEnabled(False)
        self.btn_convert.clicked.connect(self._start_conversion)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setObjectName("dangerBtn")
        self.btn_cancel.setMinimumHeight(42)
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.clicked.connect(self._cancel_conversion)

        layout.addStretch()
        layout.addWidget(self.btn_cancel)
        layout.addWidget(self.btn_convert)
        return frame

    # ── File handling ─────────────────────────────────────────────────────────

    def _on_files_added(self, paths: list):
        added = False
        for path in paths:
            if path not in self.selected_files:
                self.selected_files.append(path)
                ext = get_extension(path)
                item = QListWidgetItem(f"[{ext}]  {os.path.basename(path)}")
                item.setData(Qt.ItemDataRole.UserRole, path)
                item.setToolTip(path)
                self.file_list.addItem(item)
                added = True

        if added:
            self._refresh_format_radios()
            self._update_convert_button()
            self.status_bar.showMessage(f"{len(self.selected_files)} file(s) selected.")

    def _remove_selected(self):
        selected_items = self.file_list.selectedItems()

        if not selected_items:
            return

        for item in selected_items:
            path = item.data(Qt.ItemDataRole.UserRole)
            if path in self.selected_files:
                self.selected_files.remove(path)
            self.file_list.takeItem(self.file_list.row(item))

        self._refresh_format_radios()
        self._update_convert_button()
        self.status_bar.showMessage(f"{len(self.selected_files)} file(s) selected.")

    def _clear_all(self):
        if not self.selected_files and self.file_list.count() == 0:
            return

        self.selected_files.clear()
        self.file_list.clear()
        self._refresh_format_radios()
        self._update_convert_button()
        self.status_bar.showMessage("No files selected.")

    # ── Radio Button Management Helpers ────────────────────────────────────────

    def _clear_radio_group(self):
        for btn in self.radio_group.buttons():
            self.radio_group.removeButton(btn)
        
        while self.radio_layout.count():
            item = self.radio_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _set_radio_placeholder(self, text: str, enabled: bool = False):
        self._clear_radio_group()
        lbl = QLabel(text)
        lbl.setEnabled(enabled)
        lbl.setStyleSheet("color: #666666; font-style: italic;")
        self.radio_layout.addWidget(lbl)
        self.radio_layout.addStretch()
        self.radio_container.setEnabled(enabled)

    def _get_current_selected_format(self) -> str:
        checked_button = self.radio_group.checkedButton()
        if checked_button:
            return checked_button.text()
        return ""

    def _refresh_format_radios(self):
        if not self.selected_files:
            self._set_radio_placeholder("— select a file first —", enabled=False)
            return

        common_targets = None
        for path in self.selected_files:
            ext = get_extension(path)
            targets = set(CONVERSION_MAP.get(ext, []))
            common_targets = targets if common_targets is None else common_targets & targets

        previous_selection = self._get_current_selected_format()
        self._clear_radio_group()

        if common_targets:
            self.radio_container.setEnabled(True)
            sorted_formats = sorted(common_targets)
            
            for index, fmt in enumerate(sorted_formats):
                rad = QRadioButton(fmt)
                rad.setCursor(Qt.CursorShape.PointingHandCursor)
                self.radio_group.addButton(rad, index)
                self.radio_layout.addWidget(rad)
                
                if fmt == previous_selection:
                    rad.setChecked(True)
            
            if not self.radio_group.checkedButton() and self.radio_group.buttons():
                self.radio_group.buttons()[0].setChecked(True)
                
            self.radio_layout.addStretch()
        else:
            self._set_radio_placeholder("— no common format —", enabled=False)

    def _update_convert_button(self):
        has_selection = self._get_current_selected_format() != ""
        can_convert = (
            bool(self.selected_files)
            and self.radio_container.isEnabled()
            and has_selection
        )
        self.btn_convert.setEnabled(can_convert)

    # ── Output directory ──────────────────────────────────────────────────────

    def _browse_output_dir(self):
        path = QFileDialog.getExistingDirectory(self, "Select Output Directory", self.output_dir)
        if path:
            self.output_dir = path
            self.output_dir_edit.setText(path)

    # ── Conversion ────────────────────────────────────────────────────────────

    def _start_conversion(self):
        target_format = self._get_current_selected_format()
        if not target_format or target_format.startswith("—"):
            QMessageBox.warning(self, "No Format", "Please select a target format.")
            return

        self.log_list.clear()
        self.progress_bar.setValue(0)
        self.btn_convert.setEnabled(False)
        self.btn_cancel.setEnabled(True)
        self.progress_label.setText("Converting…")
        self.status_bar.showMessage("Conversion in progress…")

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
            self.progress_label.setText("Cancelling…")
            self.status_bar.showMessage("Cancellation requested…")

    # ── Worker signals ────────────────────────────────────────────────────────

    def _on_progress(self, value: int):
        self.progress_bar.setValue(value)

    def _on_file_done(self, input_path: str, output_paths: list):
        name = os.path.basename(input_path)
        for out in output_paths:
            item = QListWidgetItem(f"✔  {name}  →  {os.path.basename(out)}")
            item.setForeground(QColor("#4caf50"))
            self.log_list.addItem(item)
        self.log_list.scrollToBottom()

    def _on_file_error(self, input_path: str, error: str):
        name = os.path.basename(input_path)
        item = QListWidgetItem(f"✘  {name}  —  {error}")
        item.setForeground(QColor("#f44336"))
        self.log_list.addItem(item)
        self.log_list.scrollToBottom()

    def _on_finished(self, success: int, failed: int):
        self.btn_convert.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        self.progress_bar.setValue(100)
        self.progress_label.setText(f"Done — {success} succeeded, {failed} failed.")
        self.status_bar.showMessage(f"Conversion complete: {success} succeeded, {failed} failed.")

        if failed == 0:
            QMessageBox.information(
                self, "Done",
                f"All {success} file(s) converted successfully.\n\nOutput: {self.output_dir}"
            )
        else:
            QMessageBox.warning(
                self, "Completed with Errors",
                f"{success} succeeded, {failed} failed.\nCheck the log for details."
            )

    # ── Stylesheet ────────────────────────────────────────────────────────────

    def _apply_stylesheet(self):
        self.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #f0f4ff;
            color: #1a1a2e;
            font-family: "Segoe UI";
            font-size: 13px;
        }

        /* ── Sidebar-style left panel ── */
        QSplitter {
            background-color: transparent;
        }
        QSplitter::handle {
            background-color: #dce6f7;
            width: 1px;
        }

        /* ── Group boxes ── */
        QGroupBox {
            background-color: rgba(255, 255, 255, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.9);
            border-radius: 16px;
            margin-top: 12px;
            padding: 14px;
            font-weight: 600;
            font-size: 13px;
            color: #2a2a5a;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 14px;
            padding: 0 6px;
            color: #3a5bd9;
        }

        /* ── File list ── */
        QListWidget {
            background-color: rgba(255, 255, 255, 0.5);
            border: 1px solid rgba(200, 215, 255, 0.7);
            border-radius: 12px;
            color: #1a1a2e;
            alternate-background-color: rgba(240, 244, 255, 0.5);
            outline: none;
        }
        QListWidget::item {
            padding: 6px 10px;
            border-radius: 8px;
        }
        QListWidget::item:selected {
            background-color: rgba(58, 91, 217, 0.15);
            color: #1a1a2e;
        }
        QListWidget::item:hover {
            background-color: rgba(58, 91, 217, 0.08);
        }

        /* ── ComboBox ── */
        QComboBox {
            background-color: rgba(255, 255, 255, 0.7);
            border: 1.5px solid rgba(58, 91, 217, 0.4);
            border-radius: 10px;
            padding: 8px 14px;
            color: #1a1a2e;
            min-height: 36px;
            min-width: 200px;
            selection-background-color: #3a5bd9;
        }
        QComboBox:disabled {
            color: #aaaacc;
            border-color: #dce6f7;
            background-color: rgba(240, 244, 255, 0.4);
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border-left: 1px solid rgba(58, 91, 217, 0.3);
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
        }
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid #3a5bd9;
            width: 0;
            height: 0;
        }
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            border: 1.5px solid rgba(58, 91, 217, 0.4);
            border-radius: 0px;
            outline: none;
            color: #1a1a2e;
            selection-background-color: rgba(58, 91, 217, 0.12);
            selection-color: #1a1a2e;
            show-decoration-selected: 1;
        }
        QComboBox QAbstractItemView::item {
            min-height: 32px;
            padding-left: 12px;
            border: none;
        }
        QComboBox QAbstractItemView::item:hover {
            background-color: rgba(58, 91, 217, 0.10);
            color: #1a1a2e;
        }
        QComboBox QAbstractItemView::item:selected {
            background-color: rgba(58, 91, 217, 0.15);
            color: #1a1a2e;
        }

        /* ── Line edit ── */
        QLineEdit {
            background-color: rgba(255, 255, 255, 0.6);
            border: 1.5px solid rgba(58, 91, 217, 0.25);
            border-radius: 10px;
            padding: 8px 12px;
            color: #1a1a2e;
        }
        QLineEdit:focus {
            border-color: #3a5bd9;
            background-color: rgba(255, 255, 255, 0.9);
        }

        /* ── Progress bar ── */
        QProgressBar {
            background-color: rgba(220, 230, 247, 0.6);
            border: none;
            border-radius: 8px;
            text-align: center;
            color: #3a5bd9;
            font-weight: 600;
            min-height: 22px;
        }
        QProgressBar::chunk {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #3a5bd9, stop:1 #6a8fff
            );
            border-radius: 8px;
        }

        /* ================================================================= */
        /* ── BUTTONS SYSTEM (LIGHT HYPER-GLOW THEME) ────────────────────── */
        /* ================================================================= */
        QPushButton {
            border-radius: 10px;
            padding: 10px 22px;
            font-family: "SF Pro Display", "Segoe UI";
            font-size: 13px;
            font-weight: 600;
            border: 1px solid transparent; /* Keeps layout perfectly stable */
        }

        /* ── Primary Action Button (Convert) ── */
        QPushButton#primaryBtn {
            background-color: #e6f2ff;     /* Ice Blue - Crisp Light Base */
            color: #007aff;                /* Vivid Core Accent Blue */
        }
        QPushButton#primaryBtn:hover {
            background-color: #f0f7ff;     /* Lights up brighter on hover */
            /* Intense Electric Blue Glowing 1px Edge Border */
            border: 1px solid #007aff;     
        }
        QPushButton#primaryBtn:pressed {
            background-color: #ccdfff;
        }
        QPushButton#primaryBtn:disabled {
            background-color: #f2f2f7;
            color: #aeaeb2;
            border: none;
        }

        /* ── Danger Action Buttons (Clear All, Cancel) ── */
        QPushButton#dangerBtn {
            background-color: #ffebe6;     /* Soft Rose - Light Base */
            color: #ff3b30;                /* Sharp Red Indicator Text */
        }
        QPushButton#dangerBtn:hover {
            background-color: #fff2f0;     /* Lights up brighter on hover */
            /* Vivid Coral Crimson Glowing 1px Edge Border */
            border: 1px solid #ff3b30;     
        }
        QPushButton#dangerBtn:pressed {
            background-color: #ffd1c7;
        }
        QPushButton#dangerBtn:disabled {
            background-color: #f2f2f7;
            color: #aeaeb2;
            border: none;
        }

        /* ── Secondary Buttons (Browse, Remove Selected, Open Folder) ── */
        QPushButton#secondaryBtn {
            background-color: #ffffff;     /* Sharp Pure White Base */
            color: #48484a;                /* Charcoal Neutral Text */
            border: 1px solid #d1d1d6;     
        }
        QPushButton#secondaryBtn:hover {
            background-color: #fafafa;
            /* Luminous Cyan-Blue Glowing 1px Edge Border */
            border: 1px solid #5ac8fa;     
            color: #007aff;
        }
        QPushButton#secondaryBtn:pressed {
            background-color: #e5e5ea;
        }

        /*# /* ── Buttons base ── */
        # QPushButton {
        #     border-radius: 10px;
        #     padding: 8px 20px;
        #     font-size: 13px;
        #     font-weight: 500;
        # }

        # /* Primary */
        # QPushButton#primaryBtn {
        #     background-color: qlineargradient(
        #         x1:0, y1:0, x2:1, y2:0,
        #         stop:0 #3a5bd9, stop:1 #5b7fff
        #     );
        #     color: #ffffff;
        #     border: none;
        #     font-weight: 700;
        #     min-width: 130px;
        # }
        # QPushButton#primaryBtn:hover {
        #     background-color: qlineargradient(
        #         x1:0, y1:0, x2:1, y2:0,
        #         stop:0 #2a4bc9, stop:1 #4a6fff
        #     );
        #     border: 1.5px solid rgba(90, 130, 255, 0.6);
        # }
        # QPushButton#primaryBtn:disabled {
        #     background-color: #c5d0f0;
        #     color: #8899cc;
        # }

        # /* Secondary */
        # QPushButton#secondaryBtn {
        #     background-color: rgba(255, 255, 255, 0.65);
        #     color: #3a5bd9;
        #     border: 1.5px solid rgba(58, 91, 217, 0.35);
        #     backdrop-filter: blur(8px);
        # }
        # QPushButton#secondaryBtn:hover {
        #     background-color: rgba(255, 255, 255, 0.9);
        #     border: 1.5px solid rgba(58, 91, 217, 0.8);
        #     color: #2a4bc9;
        # }

        # /* Danger */
        # QPushButton#dangerBtn {
        #     background-color: rgba(255, 255, 255, 0.65);
        #     color: #cc3333;
        #     border: 1.5px solid rgba(204, 51, 51, 0.35);
        # }
        # QPushButton#dangerBtn:hover {
        #     background-color: rgba(255, 235, 235, 0.85);
        #     border: 1.5px solid rgba(204, 51, 51, 0.7);
        #     color: #aa2222;
        # }
        # QPushButton#dangerBtn:disabled {
        #     background-color: rgba(240, 240, 240, 0.4);
        #     color: #ccaaaa;
        #     border-color: #e0cccc;
        # } */

        /* ── Labels ── */
        QLabel#appTitle {
            font-size: 20px;
            font-weight: 700;
            color: #3a5bd9;
        }
        QLabel#appSubtitle {
            font-size: 12px;
            color: #8899bb;
        }
        QLabel#fieldLabel {
            color: #556699;
            font-size: 12px;
            font-weight: 600;
        }
        QLabel#progressLabel {
            color: #556699;
            font-size: 12px;
        }

        /* ── Status bar ── */
        QStatusBar {
            background-color: rgba(255, 255, 255, 0.5);
            color: #8899bb;
            border-top: 1px solid rgba(58, 91, 217, 0.12);
            font-size: 12px;
        }

        /* ── Scrollbar ── */
        QScrollBar:vertical {
            background: rgba(220, 230, 247, 0.4);
            width: 6px;
            border-radius: 3px;
        }
        QScrollBar::handle:vertical {
            background: rgba(58, 91, 217, 0.35);
            border-radius: 3px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background: rgba(58, 91, 217, 0.6);
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

        /* ── Radio buttons ── */
        QRadioButton {
            color: #1a1a2e;
            spacing: 6px;
        }
        QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: 2px solid rgba(58, 91, 217, 0.5);
            background-color: white;
        }
        QRadioButton::indicator:checked {
            background-color: #3a5bd9;
            border-color: #3a5bd9;
        }
        QRadioButton::indicator:hover {
            border-color: #3a5bd9;
        }
    """)