from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QProgressBar, QPushButton, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from config.constants import COLOR_TEXT, COLOR_SUBTEXT, COLOR_BACKGROUND, COLOR_SUPER
from logic.engine_downloader import get_stockfish_path
import sys
import traceback

class StockfishLoaderThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def run(self):
        try:
            for i in range(1, 60):
                self.msleep(30)
                self.progress.emit(i)

            path = get_stockfish_path()
            for i in range(60, 101):
                self.msleep(15)
                self.progress.emit(i)

            self.finished.emit(path)
        except Exception:
            self.error.emit(traceback.format_exc())

class StockfishLoaderWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.path = None
        self.success = False

    def exec(self):
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.dialog = StockfishLoaderUI()
        self.dialog.ok_button.clicked.connect(self.on_ok_clicked)

        self.dialog.exec()
        return self.path if self.success else None

    def on_ok_clicked(self):
        self.path = self.dialog.path_label.text().replace("Path: ", "").strip()
        self.success = True
        self.dialog.close()


class StockfishLoaderUI(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stockfish Loader")
        self.setFixedSize(400, 220)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLOR_BACKGROUND.name()};
            }}
            QLabel {{
                color: {COLOR_TEXT.name()};
                font-size: 16px;
            }}
            QPushButton {{
                background-color: #59636E;
                color: {COLOR_TEXT.name()};
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLOR_TEXT.name()};
                color: {COLOR_BACKGROUND.name()};
            }}
        """)

        self.label = QLabel("Downloading Stockfish...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setStyleSheet(f"""
        QProgressBar {{
            background-color: {COLOR_BACKGROUND.name()};
            border: 1px solid {COLOR_SUBTEXT.name()};
            border-radius: 6px;
            text-align: center;
            color: {COLOR_TEXT.name()};
            font-family: JetBrains Mono, monospace;
            font-size: 16px;
        }}
        QProgressBar::chunk {{
            background-color: #59636E;
            border-radius: 6px;
        }}
    """)


        self.path_label = QLabel("")
        self.path_label.setWordWrap(True)
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.path_label.setStyleSheet(f"color: {COLOR_SUBTEXT.name()}; font-size: 16px;")
        self.path_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.ok_button = QPushButton("OK")
        self.ok_button.setEnabled(False)
        self.ok_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)
        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        layout.addWidget(self.path_label)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)
        self.start_download()

    def start_download(self):
        self.thread = StockfishLoaderThread()
        self.thread.progress.connect(self.progress.setValue)
        self.thread.finished.connect(self.on_finished)
        self.thread.error.connect(self.on_error)
        self.thread.start()

    def on_finished(self, path):
        self.label.setText("Stockfish successfully downloaded!")
        self.path_label.setText(f"{path}")
        self.ok_button.setEnabled(True)

    def on_error(self, error_text):
        QMessageBox.critical(self, "Download Error", f"An error occurred:\n{error_text}")
        self.label.setText("Error while downloading Stockfish")
        self.ok_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loader_ui = StockfishLoaderUI()
    loader_ui.show()
    sys.exit(app.exec())
