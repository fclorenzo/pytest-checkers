#test_checkers.py
import pytest
import pygame
from checkers import main
from game_control import GameControl
from board import Board
from piece import Piece

# Inicializa o pygame (necessário para a interface gráfica)
@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()

# 1. Teste de inicialização do jogo no modo "pvp" (Player vs Player)
def test_game_initialization_pvp():
    pieces = [Piece("12WN"), Piece("16BN")]
    board = Board(pieces, "W")
    game_control = GameControl("W", False)  # Player vs Player, sem IA

    assert game_control.get_turn() == "W", "O turno inicial deve ser do jogador 'W'"
    assert isinstance(game_control.board, Board), "O tabuleiro não foi inicializado corretamente"
    assert len(game_control.board.get_pieces()) == 24, "O número de peças no tabuleiro está incorreto"

# 2. Teste de inicialização do jogo no modo "cpu" (Player vs Computer)
def test_game_initialization_cpu():
    pieces = [Piece("12WN"), Piece("16BN")]
    board = Board(pieces, "W")
    game_control = GameControl("W", True)  # Player vs IA, IA joga com a cor 'B'

    assert game_control.get_turn() == "W", "O turno inicial deve ser do jogador 'W'"
    assert game_control.ai_control is not None, "A IA não foi inicializada corretamente"
    assert game_control.get_winner() is None, "Não deve haver vencedor ainda"

# 3. Teste de alternância de turnos no modo "pvp"
def test_turn_change_pvp():
    pieces = [Piece("12WN"), Piece("16BN")]
    board = Board(pieces, "W")
    game_control = GameControl("W", False)  # Player vs Player

    assert game_control.get_turn() == "W", "O turno inicial deve ser do jogador 'W'"
    game_control.release_piece()  # Simula a liberação de uma peça
    assert game_control.get_turn() == "B", "O turno não foi alterado corretamente após o movimento"

# 4. Teste de movimento de peça no modo "pvp"
def test_move_piece_pvp():
    pieces = [Piece("12WN"), Piece("16BN")]
    board = Board(pieces, "W")
    game_control = GameControl("W", False)  # Player vs Player

    # Verifica a posição inicial
    assert board.get_piece_by_index(0).get_position() == "12", "A peça não está na posição inicial correta"
    
    # Simula o movimento da peça
    game_control.hold_piece((50, 50))  # Simula o clique na peça
    game_control.release_piece()  # Simula o movimento
    assert board.get_piece_by_index(0).get_position() == "16", "A peça não foi movida corretamente"

# 5. Teste de detecção de vencedor (Player vs Player)
def test_winner_detection_pvp():
    pieces = [Piece("12WN"), Piece("16BN")]
    board = Board(pieces, "W")
    game_control = GameControl("W", False)  # Player vs Player
    
    # Verifica que ainda não há vencedor
    assert game_control.get_winner() is None, "Deve ser None antes de qualquer movimento"
    
    # Simula uma condição de vitória
    board.move_piece(0, 16)  # O jogador 'W' faz uma jogada que pode resultar em vitória
    game_control.release_piece()
    assert game_control.get_winner() == "W", "O vencedor não foi detectado corretamente"

# 6. Teste de movimento no modo "cpu" (Player vs Computer)
def test_move_piece_cpu():
    pieces = [Piece("12WN"), Piece("16BN")]
    board = Board(pieces, "W")
    game_control = GameControl("W", True)  # Player vs IA, IA joga com a cor 'B'
    
    # O turno inicial é do jogador
    assert game_control.get_turn() == "W", "O turno inicial deve ser do jogador 'W'"
    
    # Simula o movimento do jogador
    game_control.hold_piece((50, 50))  # Simula o clique na peça
    game_control.release_piece()  # Simula o movimento
    
    # Agora, é a vez da IA jogar
    assert game_control.get_turn() == "B", "O turno da IA não foi alterado após o movimento do jogador"
    
    # A IA deve realizar um movimento válido
    ai_move = game_control.ai_control.get_move(game_control.board)
    assert ai_move is not None, "A IA não fez um movimento válido"
    assert ai_move["position_from"] != ai_move["position_to"], "A IA não deve escolher um movimento inválido"

# 7. Teste de movimento e captura no modo "cpu" (Player vs Computer)
def test_capture_piece_cpu():
    pieces = [Piece("12WN"), Piece("16BN"), Piece("24WN"), Piece("20BN")]
    board = Board(pieces, "W")
    game_control = GameControl("W", True)  # Player vs IA
    
    # O turno inicial é do jogador
    assert game_control.get_turn() == "W", "O turno inicial deve ser do jogador 'W'"
    
    # Simula o movimento do jogador
    game_control.hold_piece((50, 50))  # Simula o clique na peça
    game_control.release_piece()  # Simula o movimento

    # Agora, é a vez da IA jogar
    game_control.move_ai()  # IA faz a jogada
    ai_move = game_control.ai_control.get_move(game_control.board)
    
    # Verifica se a IA realizou uma captura
    assert "eats_piece" in ai_move, "A IA não fez uma captura quando havia uma disponível"
    assert ai_move["eats_piece"] == True, "A IA deveria ter feito uma captura"

# 8. Teste de fim de jogo (game over)
def test_game_over():
    pieces = [Piece("12WN"), Piece("16BN")]
    board = Board(pieces, "W")
    game_control = GameControl("W", False)  # Player vs Player
    
    # Simula o jogo até o fim
    board.move_piece(0, 16)  # Um movimento que pode terminar o jogo
    game_control.release_piece()
    
    assert game_control.get_winner() == "W", "O jogo não terminou corretamente com a vitória de 'W'"
    game_control.release_piece()  # A partida já deve ter terminado

# 9. Teste de movimentação inválida (em borda do tabuleiro)
def test_invalid_move():
    pieces = [Piece("12WN"), Piece("16BN")]
    board = Board(pieces, "W")
    game_control = GameControl("W", False)  # Player vs Player
    
    # Tentando mover para uma posição inválida
    with pytest.raises(ValueError):
        game_control.board.move_piece(0, 32)  # Posição fora do tabuleiro (inválida)
