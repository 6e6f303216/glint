import chess
import chess.engine
from config.categories import categorize
from config.constants import get_color_for_score

def evaluate_move(board, move_uci, engine):
    current_turn = board.turn
    move = chess.Move.from_uci(move_uci)
    piece_captured = board.piece_at(move.to_square)

    info_before = engine.analyse(board, chess.engine.Limit(depth=10))
    eval_before = info_before["score"].white().score(mate_score=10000) or 0
    best_move = info_before.get("pv", [None])[0]

    board.push(move)
    info_after = engine.analyse(board, chess.engine.Limit(depth=10))
    eval_after = info_after["score"].white().score(mate_score=10000) or 0
    board.pop()

    score_diff = (eval_after - eval_before) if current_turn == chess.WHITE else (eval_before - eval_after)
    score_diff += 50
    
    if piece_captured is not None and score_diff > 150:
        score_diff = min(score_diff, 89)

    if board.is_checkmate():
        score_diff = min(score_diff, 89)

    category = categorize(score_diff)
    return score_diff, category, best_move.uci() if best_move else "N/A"
