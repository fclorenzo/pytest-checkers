#test_piece.py
import pytest
from piece import Piece
from board import Board

# 1. Teste de inicialização básica
def test_piece_initialization():
    piece = Piece("12WN")
    assert piece.get_position() == "12"
    assert piece.get_color() == "W"
    assert not piece.is_king()

# 2. Teste de movimentação válida
@pytest.mark.parametrize("position,color,moves_count", [
    ("12WN", "W", 2),  # Movimento simples
    ("0WN", "W", 1),   # Posição mínima
    ("31WN", "W", 0)   # Posição máxima
])
def test_piece_moves(position, color, moves_count):
    piece = Piece(position)
    board = Board([piece], color_up=color)
    moves = piece.get_moves(board)
    assert len(moves) == moves_count

# 3. Teste de captura básica
def test_piece_capture():
    piece = Piece("12WN")
    opponent = Piece("17BN")
    board = Board([piece, opponent], color_up="W")
    moves = piece.get_moves(board)
    capture_moves = [move for move in moves if move["eats_piece"]]
    assert len(capture_moves) == 1
    assert capture_moves[0]["position"] == "23"

# 4. Teste de promoção a dama
def test_piece_promotion():
    piece = Piece("28WN")
    piece.set_is_king(True)
    assert piece.is_king()

# 5. Teste de comportamento inválido
@pytest.mark.parametrize("invalid_position", ["-1", "32", "99"])
def test_piece_invalid_positions(invalid_position):
    piece = Piece(f"{invalid_position}WN")
    with pytest.raises(ValueError):
        piece.get_moves(Board([], color_up="W"))

# 6. Teste de borda do tabuleiro
def test_piece_edge_behavior():
    piece = Piece("0WN")  # Posição inicial
    board = Board([piece], color_up="W")
    moves = piece.get_moves(board)
    assert all(0 <= int(move["position"]) <= 31 for move in moves)

# 7. Teste de captura obrigatória
def test_piece_forced_capture():
    piece = Piece("12WN")
    opponent1 = Piece("16BN")
    opponent2 = Piece("17BN")
    board = Board([piece, opponent1, opponent2], color_up="W")
    moves = piece.get_moves(board)
    capture_moves = [move for move in moves if move["eats_piece"]]
    assert len(capture_moves) == 1  # Deve capturar apenas o oponente na diagonal

# 8. Teste de múltiplas capturas consecutivas
def test_piece_multiple_captures():
    piece = Piece("12WN")
    opponent1 = Piece("16BN")
    opponent2 = Piece("23BN")
    board = Board([piece, opponent1, opponent2], color_up="W")
    moves = piece.get_moves(board)
    capture_moves = [move for move in moves if move["eats_piece"]]
    assert len(capture_moves) == 1
    # Simula o movimento e verifica se a segunda captura está disponível
    board.move_piece(0, 23)  # Move peça branca para capturar a primeira preta
    moves_after_capture = piece.get_moves(board)
    assert any(move["eats_piece"] for move in moves_after_capture)  # Deve ter nova captura disponível

# 9. Teste de peças cercadas por outras da mesma cor
def test_piece_surrounded_by_same_color():
    piece = Piece("12WN")
    surrounding_pieces = [Piece(f"{pos}WN") for pos in ["7", "8", "16", "17"]]
    board = Board([piece] + surrounding_pieces, color_up="W")
    moves = piece.get_moves(board)
    assert len(moves) == 0  # Não deve haver movimentos disponíveis

# 10. Teste de dama movendo-se em múltiplas direções
def test_king_moves_multiple_directions():
    piece = Piece("12WY")  # Dama branca
    board = Board([piece], color_up="W")
    moves = piece.get_moves(board)
    assert len(moves) > 2  # Deve haver mais de 2 movimentos disponíveis
