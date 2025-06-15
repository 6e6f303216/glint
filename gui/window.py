import base64
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsTextItem
)
from PyQt6.QtGui import QColor, QBrush, QFont, QPen, QFontDatabase, QPainter
from PyQt6.QtCore import Qt, QByteArray, QBuffer, QIODeviceBase, QUrl
from PyQt6.QtMultimedia import QSoundEffect
from pathlib import Path

from assets.fonts_data import JETBRAINS_MONO
from logic.chess_logic import evaluate_move, get_color_for_score
from logic.player_model import PlayerModel
from config.constants import *
from config.categories import CATEGORIES
import chess
import chess.engine

from . import load_styles

BUTTON_STYLE = load_styles()


class ChessBoardGUI(QMainWindow):
    def __init__(self, stockfish_path: str):
        super().__init__()
        self.setWindowTitle("Glint")
        self.resize(700, 750)
        self.last_move = None
        self.last_move_category = None
        self.last_move_by_player = False
        STOCKFISH_PATH = stockfish_path

        self.board = chess.Board()
        self.player_model = PlayerModel()
        self.selected_square = None

        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHints(QPainter.RenderHint.Antialiasing)
        layout.addWidget(self.view)

        self.status_label = QLabel("", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.reset_button = QPushButton("x")
        self.undo_button = QPushButton("<")

        nerd_font = QFont("JetBrainsMono Nerd Font", 36)
        for btn in (self.reset_button, self.undo_button):
            btn.setFont(nerd_font)
            btn.setFixedSize(60, 60)
            btn.setStyleSheet(BUTTON_STYLE)

        self.reset_button.setToolTip("Reset Board")
        self.undo_button.setToolTip("Undo Move")
        self.reset_button.clicked.connect(self.reset_board)
        self.undo_button.clicked.connect(self.undo_move)

        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.undo_button)
        layout.addLayout(button_layout)
        layout.addWidget(self.status_label)

        sound_dir = Path(__file__).parent.parent / "assets" / "sounds"
        print(sound_dir)

        self.move_sound = QSoundEffect()
        self.move_sound.setSource(QUrl.fromLocalFile(str(sound_dir / "move.wav")))
        self.move_sound.setVolume(0.25)

        self.excellent_sound = QSoundEffect()
        self.excellent_sound.setSource(QUrl.fromLocalFile(str(sound_dir / "excellent.wav")))
        self.excellent_sound.setVolume(0.5)


        try:
            font_data = base64.b64decode(JETBRAINS_MONO)
            byte_array = QByteArray(font_data)
            buffer = QBuffer(byte_array)
            buffer.open(QIODeviceBase.OpenModeFlag.ReadOnly)

            font_id = QFontDatabase.addApplicationFontFromData(buffer.data())
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    font = QFont(families[0], 16)
                    self.setFont(font)
        except Exception as e:
            print(e)

        self.setStyleSheet(f"background-color: {COLOR_BACKGROUND.name()}; color: {COLOR_TEXT.name()};")
        self.view.setStyleSheet(f"background-color: {COLOR_BACKGROUND.name()};")
        self.status_label.setStyleSheet(f"color: {COLOR_SUBTEXT.name()};")

        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        self.draw_board()

    def reset_board(self):
        self.board.reset()
        self.selected_square = None
        self.last_move = None
        self.last_move_category = None
        self.status_label.setText("Board reset.")
        self.draw_board()

    def undo_move(self):
        if self.board.move_stack:
            self.board.pop()
            if self.board.move_stack:
                self.board.pop()
            self.selected_square = None
            self.last_move = None
            self.last_move_category = None
            self.status_label.setText("Move undone.")
            self.draw_board()
        else:
            self.status_label.setText("No moves to undo.")



    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def highlight_moves(self, square):
        piece = self.board.piece_at(square)
        if not piece:
            return

        for move in self.board.legal_moves:
            if move.from_square == square:
                to_sq = move.to_square
                file = chess.square_file(to_sq)
                rank = 7 - chess.square_rank(to_sq)
                ellipse = self.scene.addEllipse(
                    file * 75 + 25, rank * 75 + 25, 25, 25,
                    brush=QBrush(COLOR_SUBTEXT)
                )


    def draw_board(self):
        self.scene.clear()

        tile_size = 75

        for rank in range(8):
            for file in range(8):
                square = chess.square(file, 7 - rank)
                rect = QGraphicsRectItem(file * tile_size, rank * tile_size, tile_size, tile_size)
                color = LIGHT_TILE if (rank + file) % 2 == 0 else DARK_TILE
                rect.setBrush(QBrush(color))
                self.scene.addItem(rect)

                piece = self.board.piece_at(square)
                if piece:
                    text = QGraphicsTextItem(UNICODE_PIECES[piece.symbol()])
                    text.setFont(QFont("Arial", 36))

                    if self.last_move_by_player and self.last_move and square in [self.last_move.from_square, self.last_move.to_square]:
                        if self.last_move_category:
                            for threshold, category_text in CATEGORIES:
                                if category_text == self.last_move_category:
                                    color = get_color_for_score(threshold)
                                    break
                            else:
                                color = COLOR_TEXT
                        else:
                            color = COLOR_TEXT
                    else:
                        color = COLOR_TEXT if piece.color else COLOR_OPPOSITE_TEXT


                    text.setDefaultTextColor(color)
                    
                    bounding = text.boundingRect()
                    center_x = file * tile_size + (tile_size - bounding.width()) / 2
                    center_y = rank * tile_size + (tile_size - bounding.height()) / 2
                    text.setPos(center_x, center_y)

                    self.scene.addItem(text)

        self.scene.mousePressEvent = self.handle_click

    def handle_click(self, event):
        pos = event.scenePos()
        file = int(pos.x() // 75)
        rank = 7 - int(pos.y() // 75)
        square = chess.square(file, rank)

        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == chess.WHITE:
                self.selected_square = square
                self.draw_board()
                self.highlight_moves(square)
        else:
            move = chess.Move(self.selected_square, square)
            self.selected_square = None
            if move in self.board.legal_moves:
                move_uci = move.uci()
                board_copy = self.board.copy()
                score_diff, category, best_move = evaluate_move(board_copy, move_uci, self.engine)
                self.board.push(move)
                self.player_model.update(score_diff)
                self.last_move = move
                self.last_move_category = category
                self.last_move_by_player = True
                avg_score = self.player_model.average_score_diff()
                self.status_label.setText(f"{category} (Δ {score_diff}) | Average: {avg_score:+.1f}")


                if score_diff >= 50:
                    self.excellent_sound.play()
                else:
                    self.move_sound.play()

                color = get_color_for_score(score_diff)
                self.status_label.setStyleSheet(f"color: {color.name()}; font-weight: bold;")
                font = QFont()
                font.setPointSize(14)
                self.status_label.setFont(font)

                self.draw_board()

                if not self.board.is_game_over():
                    level = self.player_model.get_engine_level()
                    result = self.engine.play(self.board, chess.engine.Limit(depth=level))
                    self.board.push(result.move)
                    self.last_move = None
                    self.last_move_category = None
                    self.draw_board()
            else:
                self.status_label.setText("Illegal move.")
                self.draw_board()

    def closeEvent(self, event):
        self.engine.quit()
        event.accept()