from PyQt6.QtGui import QColor

COLOR_BRILLIANT = QColor("#adadeb")
COLOR_EXCELLENT = QColor("#adc6eb")
COLOR_GREAT = QColor("#addeeb")
COLOR_GOOD = QColor("#adebde")
COLOR_OK = QColor("#adebc6")
COLOR_REASONABLE = QColor("#adebad")
COLOR_INACCURACY = QColor("#c6ebad")
COLOR_MISTAKE = QColor("#deebad")
COLOR_BLUNDER = QColor("#ebadad")

COLOR_CORE = QColor("#1A1E22")
COLOR_BACKGROUND = QColor("#23272C")
COLOR_SURFACE = QColor("#2D333A")
COLOR_SUPER = QColor("#59636E")
COLOR_TEXT = QColor("#F0F4FA")
COLOR_SUBTEXT = QColor("#D4DCE7")
COLOR_OPPOSITE_TEXT = QColor("#adadeb")

LIGHT_TILE = COLOR_SURFACE
DARK_TILE = COLOR_CORE

UNICODE_PIECES = {
    "P": "♟", "N": "♞", "B": "♝", "R": "♜", "Q": "♛", "K": "♚",
    "p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚"
}

def get_color_for_score(score_diff):
    if score_diff >= 150:
        return COLOR_BRILLIANT
    elif score_diff >= 90:
        return COLOR_EXCELLENT
    elif score_diff >= 50:
        return COLOR_GREAT
    elif score_diff >= 20:
        return COLOR_GOOD
    elif score_diff >= 5:
        return COLOR_OK
    elif score_diff >= 0:
        return COLOR_REASONABLE
    elif score_diff >= -50:
        return COLOR_INACCURACY
    elif score_diff >= -150:
        return COLOR_MISTAKE
    else:
        return COLOR_BLUNDER

from gui.stockfish_loader import StockfishLoaderWindow

def show_stockfish_loader():
    loader = StockfishLoaderWindow()
    loader.exec()