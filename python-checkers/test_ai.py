#test_ai.py
import pytest
from ai import AI
from board import Board
from piece import Piece

# 1. Teste de Inicialização da IA
def test_ai_initialization():
    ai = AI("B")  # IA jogando com a cor preta
    assert ai.color == "B", "A cor da IA deve ser 'B'"

# 2. Teste do algoritmo Minimax
@pytest.mark.parametrize("depth, expected_value", [
    (0, 2),  # Profundidade 0 (máxima), deve retornar o valor do tabuleiro
    (1, 1),  # Profundidade 1, IA pode avaliar a jogada inicial
    (2, 0),  # Profundidade 2, uma avaliação mais profunda
])
def test_minimax(depth, expected_value):
    # Prepara as peças para um cenário simples
    pieces = [Piece("12WN"), Piece("16BN")]  # Uma peça branca e uma preta
    board = Board(pieces, "W")  # Tabuleiro com peças
    ai = AI("B")  # IA preta
    value = ai.minimax(board, True, depth, "B")  # Chama o minimax
    assert value == expected_value, f"Esperado {expected_value}, mas obteve {value}"

# 3. Teste de escolha de movimento pela IA
def test_ai_move():
    # Criação de peças para um cenário simples
    pieces = [Piece("12WN"), Piece("16BN"), Piece("24WN"), Piece("20BN")]
    board = Board(pieces, "W")  # Tabuleiro com 4 peças
    ai = AI("B")  # IA preta

    # A IA deve avaliar o tabuleiro e escolher o melhor movimento
    move = ai.get_move(board)

    # O movimento deve ter as chaves "position_from" e "position_to"
    assert "position_from" in move, "O movimento deve ter a chave 'position_from'"
    assert "position_to" in move, "O movimento deve ter a chave 'position_to'"

    # Verifica se o movimento retornado é válido
    start_pos = int(move["position_from"])
    end_pos = int(move["position_to"])

    # Verifica que a posição de destino está no intervalo válido do tabuleiro (0-31)
    assert 0 <= start_pos <= 31, f"A posição de início ({start_pos}) deve estar entre 0 e 31"
    assert 0 <= end_pos <= 31, f"A posição de destino ({end_pos}) deve estar entre 0 e 31"

# 4. Teste de Escolha de Movimento quando há múltiplas opções boas
def test_ai_multiple_good_moves():
    pieces = [Piece("12WN"), Piece("16BN"), Piece("24WN"), Piece("20BN")]
    board = Board(pieces, "W")
    ai = AI("B")  # IA preta

    # A IA deve ser capaz de avaliar várias opções de movimento e escolher a melhor
    move = ai.get_move(board)

    # A IA deve devolver um movimento válido
    assert "position_from" in move and "position_to" in move

    # Simulação de um cenário com múltiplos bons movimentos
    # Aqui, você pode querer implementar mais verificações dependendo da lógica
    # de movimentos válidos do jogo, mas já estamos checando se o movimento é viável

# 5. Teste de Movimento da IA com Captura
def test_ai_move_with_capture():
    # Criação de peças, incluindo uma peça que pode ser capturada
    pieces = [Piece("12WN"), Piece("16BN"), Piece("24WN"), Piece("20BN")]
    board = Board(pieces, "W")
    ai = AI("B")  # IA preta

    # A IA deve preferir capturar se houver uma captura possível
    move = ai.get_move(board)
    
    # Se o movimento inclui uma captura, o valor de "eats_piece" deve ser True
    assert "eats_piece" in move, "O movimento deve conter a chave 'eats_piece'"
    assert move["eats_piece"] == True, "A IA deve realizar uma captura quando possível"

# 6. Teste de Profundidade no Minimax
@pytest.mark.parametrize("depth, expected_value", [
    (0, 2),
    (1, 1),
    (2, -1),  # A IA deve preferir movimentos que favorecem sua posição
])
def test_minimax_with_depth(depth, expected_value):
    pieces = [Piece("12WN"), Piece("16BN"), Piece("24WN"), Piece("20BN")]
    board = Board(pieces, "W")
    ai = AI("B")
    result = ai.minimax(board, True, depth, "B")
    assert result == expected_value, f"Esperado {expected_value} para profundidade {depth}, mas obteve {result}"

# 7. Teste de Simulação de Jogo com IA
def test_ai_in_game():
    pieces = [Piece("12WN"), Piece("16BN"), Piece("24WN"), Piece("20BN")]
    board = Board(pieces, "W")
    ai = AI("B")
    ai_move = ai.get_move(board)

    # Simula o movimento da IA
    start_pos = int(ai_move["position_from"])
    end_pos = int(ai_move["position_to"])

    # Move a peça no tabuleiro
    board.move_piece(start_pos, end_pos)

    # Verifica se a IA fez uma jogada válida
    moved_piece = board.get_piece_by_index(start_pos)
    assert moved_piece.get_position() == str(end_pos), f"Peça não se moveu corretamente de {start_pos} para {end_pos}"

# 8. Teste de Exceção para Movimento Inválido
def test_ai_invalid_move():
    pieces = [Piece("12WN"), Piece("16BN"), Piece("24WN"), Piece("20BN")]
    board = Board(pieces, "W")
    ai = AI("B")  # IA preta

    # Simula um movimento inválido (fora do tabuleiro)
    move = ai.get_move(board)
    assert move["position_from"] != move["position_to"], "A IA não deve retornar um movimento inválido"

# 9. Teste de Tabuleiro Vazio (Borda)
def test_ai_empty_board():
    board = Board([], "W")  # Tabuleiro vazio
    ai = AI("B")
    
    # A IA não deve fazer movimento se não houver peças no tabuleiro
    move = ai.get_move(board)
    assert move is None, "A IA não deve tentar mover quando não houver peças no tabuleiro"

# 10. Teste de Profundidade Maior no Minimax
def test_minimax_depth_3():
    pieces = [Piece("12WN"), Piece("16BN"), Piece("24WN"), Piece("20BN")]
    board = Board(pieces, "W")
    ai = AI("B")
    result = ai.minimax(board, True, 3, "B")
    assert isinstance(result, int), "O resultado do minimax deve ser um valor inteiro"

# 11. Teste de Minimax com Vencedor
def test_minimax_with_winner():
    pieces = [Piece("12WN"), Piece("16BN")]
    board = Board(pieces, "W")
    ai = AI("B")
    # Simula uma condição de vencedor
    board.move_piece(0, 16)  # Movimento que pode causar a vitória
    result = ai.minimax(board, True, 2, "B")
    assert result != 2, "A IA deve reconhecer a vitória e parar de avaliar o jogo"
