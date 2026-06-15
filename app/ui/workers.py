from PyQt6.QtCore import QThread, pyqtSignal
from app.converters.router import convert


class ConversionWorker(QThread):
    progress = pyqtSignal(int)
    file_done = pyqtSignal(str, list)
    file_error = pyqtSignal(str, str)
    finished = pyqtSignal(int, int)

    def __init__(self, files: list, target_format: str, output_dir: str, parent=None):
        super().__init__(parent)
        self.files = files
        self.target_format = target_format
        self.output_dir = output_dir
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        total = len(self.files)
        success = 0
        failed = 0

        for i, input_path in enumerate(self.files):
            if self._cancelled:
                break

            try:
                output_paths = convert(
                    input_path=input_path,
                    target_format=self.target_format,
                    output_dir=self.output_dir
                )
                success += 1
                self.file_done.emit(input_path, output_paths)
            except Exception as e:
                failed += 1
                self.file_error.emit(input_path, str(e))

            progress_value = int(((i + 1) / total) * 100)
            self.progress.emit(progress_value)

        self.finished.emit(success, failed)