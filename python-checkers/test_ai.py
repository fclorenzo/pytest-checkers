import pytest
from ai import AI
from board import Board
from piece import Piece

# 1. Teste de Inicialização da IA
def test_ai_initialization():
    ai = AI("B")  # IA jogando com a cor preta
    assert ai.color == "B", "A cor da IA deve ser 'B'"

# 2. Teste do algoritmo Minimax com Profundidades Extremas
@pytest.mark.parametrize("depth, expected_value", [
    (0, 2),  # Profundidade 0
    (1, 1),  # Profundidade 1
    (10, 1), # Profundidade alta
    (-1, 0), # Profundidade negativa (tratada como caso inválido)
])
def test_minimax_with_extreme_depths(depth, expected_value):
    pieces = [Piece("12WN"), Piece("16BN")]
    board = Board(pieces, "W")
    ai = AI("B")
    value = ai.minimax(board, True, depth, "B")
    assert isinstance(value, int), "O Minimax deve retornar um valor inteiro"
    if depth >= 0:
        assert value == expected_value, f"Esperado {expected_value} para profundidade {depth}, mas obteve {value}"

# 3. Teste de Escolha de Movimento pela IA
def test_ai_move():
    pieces = [Piece("12WN"), Piece("16BN"), Piece("24WN"), Piece("20BN")]
    board = Board(pieces, "W")
    ai = AI("B")
    move = ai.get_move(board)
    assert "position_from" in move, "O movimento deve ter a chave 'position_from'"
    assert "position_to" in move, "O movimento deve ter a chave 'position_to'"
    start_pos = int(move["position_from"])
    end_pos = int(move["position_to"])
    assert 0 <= start_pos <= 31, f"A posição de início ({start_pos}) deve estar entre 0 e 31"
    assert 0 <= end_pos <= 31, f"A posição de destino ({end_pos}) deve estar entre 0 e 31"

# 4. Teste de Cenário com Movimentos Múltiplos e Iguais
def test_ai_multiple_good_moves():
    pieces = [Piece("12WN"), Piece("16BN"), Piece("24WN"), Piece("20BN")]
    board = Board(pieces, "W")
    ai = AI("B")
    move = ai.get_move(board)
    assert "position_from" in move and "position_to" in move, "A IA deve retornar um movimento válido"

# 5. Teste de Movimento com Captura
def test_ai_move_with_capture():
    pieces = [Piece("12WN"), Piece("16BN"), Piece("24WN"), Piece("20BN")]
    board = Board(pieces, "W")
    ai = AI("B")
    move = ai.get_move(board)
    assert "eats_piece" in move, "O movimento deve conter a chave 'eats_piece'"
    assert move["eats_piece"] is True, "A IA deve realizar uma captura quando possível"

# 6. Teste de Tabuleiro Vazio (Borda)
def test_ai_empty_board():
    board = Board([], "W")  # Tabuleiro vazio
    ai = AI("B")
    move = ai.get_move(board)
    assert move is None, "A IA não deve tentar mover quando não houver peças no tabuleiro"

# 7. Teste de Tabuleiro com Limite Mínimo de Peças (1 peça)
def test_ai_with_minimal_pieces():
    pieces = [Piece("12WN")]
    board = Board(pieces, "W")
    ai = AI("B")
    move = ai.get_move(board)
    assert move is None, "A IA não deve fazer nenhum movimento se não houver movimentos válidos"

# 8. Teste de Tabuleiro Cheio (Limite Máximo de Peças)
def test_ai_with_maximal_pieces():
    pieces = [Piece(f"{i}WN") for i in range(12)] + [Piece(f"{i}BN") for i in range(20, 32)]
    board = Board(pieces, "W")
    ai = AI("B")
    move = ai.get_move(board)
    assert move is not None, "A IA deve conseguir fazer um movimento com o tabuleiro cheio"

# 9. Teste de Bordas do Tabuleiro (Posições Extremas)
@pytest.mark.parametrize("position, expected_moves", [
    ("0WN", ["4"]),  # Canto superior esquerdo
    ("31BN", ["27"]), # Canto inferior direito
])
def test_ai_with_edge_positions(position, expected_moves):
    pieces = [Piece(position)]
    board = Board(pieces, "W")
    ai = AI("B")
    move = ai.get_move(board)
    assert move is not None, f"A IA não retornou um movimento válido para a peça na posição {position}"

# 10. Teste de Cenário com Nenhum Movimento Possível
def test_ai_no_possible_moves():
    pieces = [Piece("12WN"), Piece("16WN")]  # Peças bloqueadas
    board = Board(pieces, "B")  # Turno da IA preta, mas sem peças válidas
    ai = AI("B")
    move = ai.get_move(board)
    assert move is None, "A IA não deve tentar mover se não houver movimentos válidos"

# 11. Teste de Consistência em Movimentos Iguais
def test_ai_draw_with_repeated_moves():
    pieces = [Piece("12WN"), Piece("16BN")]
    board = Board(pieces, "W")
    ai = AI("B")
    move1 = ai.get_move(board)
    move2 = ai.get_move(board)
    assert move1 == move2, "A IA deve retornar movimentos consistentes para o mesmo tabuleiro"

# 12. Teste de Captura Múltipla em Sequência
def test_ai_multiple_captures():
    pieces = [Piece("12WN"), Piece("16BN"), Piece("23BN")]
    board = Board(pieces, "W")
    ai = AI("B")
    move = ai.get_move(board)
    assert "eats_piece" in move, "A IA deve realizar capturas múltiplas quando disponíveis"
