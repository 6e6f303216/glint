from PyQt6.QtWidgets import QApplication, QMessageBox
import sys
from gui.window import ChessBoardGUI
from gui.stockfish_loader import StockfishLoaderWindow
from config.config import read_timer_config, write_timer_config

def main():
    app = QApplication(sys.argv)
    
    config = read_timer_config()
    engine = config.get("engine")
    if engine == "":
        loader = StockfishLoaderWindow()
        stockfish_path = loader.exec()
        write_timer_config({
            "engine": stockfish_path
        })
    else:
        stockfish_path = engine

    if not stockfish_path:
        QMessageBox.critical(None, "Error", "Couldn't load Stockfish engine.")
        sys.exit(1)

    gui = ChessBoardGUI(stockfish_path)
    gui.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
