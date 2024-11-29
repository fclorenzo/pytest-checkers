#test_board.py
import pytest
from board import Board
from piece import Piece

# 1. Teste de inicialização do tabuleiro
def test_board_initialization():
    pieces = [Piece(f"{i}WN") for i in range(12)] + [Piece(f"{i}BN") for i in range(20, 32)]
    board = Board(pieces, "W")
    assert len(board.get_pieces()) == 24, "O tabuleiro deve ter 24 peças no início"
    assert board.get_color_up() == "W", "A cor de quem está subindo deve ser 'W'"

# 2. Teste de movimentação válida de uma peça
def test_move_piece_valid():
    pieces = [Piece("12WN"), Piece("16BN")]
    board = Board(pieces, "W")
    board.move_piece(0, 17)  # Move a peça 12WN para a posição 17
    assert board.get_piece_by_index(0).get_position() == "17", "A peça não foi movida corretamente"
    assert board.get_piece_by_index(1).get_position() == "16BN", "A peça do adversário não foi movida"

# 3. Teste de movimento inválido (fora dos limites do tabuleiro)
def test_move_piece_invalid():
    pieces = [Piece("12WN")]
    board = Board(pieces, "W")
    with pytest.raises(ValueError):
        board.move_piece(0, 32)  # Movimento inválido para uma posição fora do tabuleiro

# 4. Teste de peça capturada (movimento de captura)
def test_capture_piece():
    piece1 = Piece("12WN")
    piece2 = Piece("16BN")  # Peça adversária
    board = Board([piece1, piece2], "W")
    board.move_piece(0, 23)  # A peça branca captura a preta
    assert len(board.get_pieces()) == 1, "A peça adversária não foi removida após a captura"
    assert board.get_piece_by_index(0).get_position() == "23", "A peça não foi movida corretamente após a captura"

# 5. Teste de borda do tabuleiro (movimento nas bordas)
def test_board_edge_behavior():
    piece = Piece("0WN")  # Posição inicial (extremo do tabuleiro)
    board = Board([piece], "W")
    moves = piece.get_moves(board)
    assert all(0 <= int(move["position"]) <= 31 for move in moves), "Os movimentos não devem sair do tabuleiro"

# 6. Teste de movimento na borda do tabuleiro (primeira linha)
def test_move_piece_at_edge():
    pieces = [Piece("0WN"), Piece("4BN")]
    board = Board(pieces, "W")
    board.move_piece(0, 4)  # Move a peça branca para a posição 4
    assert board.get_piece_by_index(0).get_position() == "4", "A peça não foi movida corretamente"
    assert board.get_piece_by_index(1).get_position() == "4BN", "A peça adversária não foi movida"

# 7. Teste de verificação de vencedor (condição de vitória)
def test_get_winner():
    piece1 = Piece("12WN")
    piece2 = Piece("16BN")
    board = Board([piece1, piece2], "W")
    assert board.get_winner() is None, "Não deve haver vencedor ainda"
    
    # Simula um cenário de vitória
    board.move_piece(0, 16)  # Movimento que poderia causar a vitória
    assert board.get_winner() == "W", "O vencedor não foi detectado corretamente"

# 8. Teste de verificação de peça no tabuleiro
def test_has_piece():
    piece1 = Piece("12WN")
    piece2 = Piece("16BN")
    board = Board([piece1, piece2], "W")
    assert board.has_piece(12) is True, "O tabuleiro deveria ter uma peça na posição 12"
    assert board.has_piece(20) is False, "O tabuleiro não deveria ter uma peça na posição 20"

# 9. Teste de movimentação com erro de peça
def test_move_piece_with_invalid_piece():
    piece1 = Piece("12WN")
    piece2 = Piece("16BN")
    board = Board([piece1, piece2], "W")
    
    # Tenta mover a peça 12WN para a posição de uma peça inimiga
    with pytest.raises(ValueError):
        board.move_piece(0, 20)  # Não pode mover para a posição já ocupada pela peça 16BN

# 10. Teste de movimento em uma peça no meio do tabuleiro (meio do tabuleiro)
def test_move_piece_middle():
    pieces = [Piece("12WN"), Piece("16BN"), Piece("24WN")]
    board = Board(pieces, "W")
    
    # Teste movendo a peça 12WN para uma posição do meio do tabuleiro
    board.move_piece(0, 18)
    assert board.get_piece_by_index(0).get_position() == "18", "A peça não foi movida corretamente para o meio do tabuleiro"

# 11. Teste de movimento de peças nas extremidades do tabuleiro
def test_move_piece_extreme_positions():
    pieces = [Piece("0WN"), Piece("31BN")]
    board = Board(pieces, "W")
    
    # Teste movendo a peça 0WN para o limite inferior do tabuleiro
    board.move_piece(0, 4)
    assert board.get_piece_by_index(0).get_position() == "4", "A peça não foi movida corretamente para o limite inferior"

# 12. Teste de movimento de peças em colunas diferentes
def test_move_piece_different_columns():
    pieces = [Piece("0WN"), Piece("4BN")]
    board = Board(pieces, "W")
    
    # Teste movendo a peça 0WN para a coluna 1 (diferente da inicial)
    board.move_piece(0, 5)
    assert board.get_piece_by_index(0).get_position() == "5", "A peça não foi movida corretamente para a coluna diferente"
    assert board.get_piece_by_index(1).get_position() == "4BN", "A peça adversária não foi movida"

# 13. Teste de peça no início do tabuleiro
def test_piece_at_start():
    piece = Piece("0WN")
    board = Board([piece], "W")
    assert board.get_piece_by_index(0).get_position() == "0", "A peça não está na posição inicial correta"
    
# 14. Teste de captura obrigatória (movimento que força a captura)
def test_forced_capture():
    piece1 = Piece("12WN")
    piece2 = Piece("16BN")
    piece3 = Piece("24BN")
    board = Board([piece1, piece2, piece3], "W")
    
    # Simula uma captura obrigatória
    board.move_piece(0, 20)  # A peça branca deve capturar a peça preta
    assert board.get_piece_by_index(0).get_position() == "20", "A peça branca não fez a captura corretamente"
    assert len(board.get_pieces()) == 2, "A captura não foi realizada corretamente, a peça adversária não foi removida"
