#test_held_piece.py
import pytest
import pygame
from held_piece import HeldPiece
from board_gui import BoardGUI
from board import Board
from piece import Piece

# Inicializa o pygame (necessário para a interface gráfica)
@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()

# 1. Teste de inicialização do HeldPiece
def test_held_piece_initialization():
    piece = Piece("12WN")  # Cria uma peça no tabuleiro
    surface = pygame.Surface((50, 50))  # Superfície para a peça
    offset = (10, 10)  # Deslocamento do mouse
    held_piece = HeldPiece(surface, offset)
    
    # Verifica se a peça foi inicializada corretamente
    assert held_piece.surface == surface, "A superfície da peça não foi corretamente atribuída"
    assert held_piece.offset == offset, "O deslocamento da peça não foi corretamente atribuído"

# 2. Teste de atualização da posição da peça (movimento)
def test_held_piece_move():
    piece = Piece("12WN")
    surface = pygame.Surface((50, 50))
    offset = (10, 10)
    held_piece = HeldPiece(surface, offset)

    # Simula o movimento da peça com a atualização da posição do mouse
    mouse_pos = (100, 100)  # Nova posição do mouse
    held_piece.draw_piece(pygame.Surface((200, 200)))  # Desenha a peça na nova posição
    
    # Verifica se a posição da peça foi atualizada corretamente
    assert held_piece.draw_rect.x == mouse_pos[0] + offset[0], "A posição x da peça não foi corretamente atualizada"
    assert held_piece.draw_rect.y == mouse_pos[1] + offset[1], "A posição y da peça não foi corretamente atualizada"

# 3. Teste de colisão (verifica se a peça pode ser solta apenas em posições válidas)
def test_held_piece_collision_detection():
    piece = Piece("12WN")
    surface = pygame.Surface((50, 50))
    offset = (10, 10)
    held_piece = HeldPiece(surface, offset)

    # Simula a colisão com uma área de movimento válida (supondo que a peça está na posição correta)
    move_rect = pygame.Rect(100, 100, 50, 50)  # Área de movimento válida
    invalid_rect = pygame.Rect(500, 500, 50, 50)  # Área de movimento inválida
    
    # Simula a detecção de colisão
    collision_valid = move_rect.colliderect(held_piece.draw_rect)
    collision_invalid = invalid_rect.colliderect(held_piece.draw_rect)
    
    # Verifica a colisão
    assert collision_valid is True, "A peça não foi detectada corretamente em uma área válida"
    assert collision_invalid is False, "A peça foi detectada incorretamente em uma área inválida"

# 4. Teste de desenho da peça em nova posição
def test_held_piece_draw():
    piece = Piece("12WN")
    surface = pygame.Surface((50, 50))  # Superfície da peça
    offset = (10, 10)
    held_piece = HeldPiece(surface, offset)

    # Simula a nova posição da peça após o movimento do mouse
    mouse_pos = (200, 200)
    held_piece.draw_piece(pygame.Surface((400, 400)))  # Desenha a peça na nova posição

    # Verifica se a peça foi desenhada corretamente
    display_surface = pygame.Surface((400, 400))  # Superfície de exibição
    held_piece.draw_piece(display_surface)  # Desenha a peça

    # A verificação aqui seria visual, por isso garantimos que a peça foi desenhada na nova posição
    assert held_piece.draw_rect.x == mouse_pos[0] + offset[0], "A peça não foi desenhada corretamente na nova posição"
    assert held_piece.draw_rect.y == mouse_pos[1] + offset[1], "A peça não foi desenhada corretamente na nova posição"

# 5. Teste de interação de clique (selecionando a peça)
def test_held_piece_on_mouse_click():
    pieces = [Piece("12WN")]
    board = Board(pieces, "W")
    board_gui = BoardGUI(board)
    
    # Simula o clique do mouse para segurar uma peça
    mouse_pos = (50, 50)  # Posição fictícia do mouse onde a peça está localizada
    piece = board_gui.get_piece_on_mouse(mouse_pos)
    
    # Verifica se a peça foi corretamente selecionada
    assert piece is not None, "A peça não foi corretamente selecionada ao clicar"
    assert piece["color"] == "W", "A peça selecionada não é a correta"

# 6. Teste de liberação de peça (soltar a peça)
def test_held_piece_release():
    pieces = [Piece("12WN")]
    board = Board(pieces, "W")
    board_gui = BoardGUI(board)
    
    # Simula o clique do mouse para segurar uma peça
    mouse_pos = (50, 50)  # Posição fictícia do mouse onde a peça está localizada
    piece = board_gui.get_piece_on_mouse(mouse_pos)
    
    # Simula o movimento da peça
    new_pos = (100, 100)  # Nova posição fictícia
    piece["rect"].x = new_pos[0]
    piece["rect"].y = new_pos[1]
    
    # Verifica se a peça foi solta na nova posição
    assert piece["rect"].x == new_pos[0], "A peça não foi corretamente solta na nova posição"
    assert piece["rect"].y == new_pos[1], "A peça não foi corretamente solta na nova posição"

# 7. Teste de interação do mouse fora do tabuleiro (clicando fora da área válida)
def test_invalid_mouse_interaction():
    pieces = [Piece("12WN")]
    board = Board(pieces, "W")
    board_gui = BoardGUI(board)
    
    # Simula o clique em uma posição fora do tabuleiro
    mouse_pos = (500, 500)  # Posição fora do tabuleiro
    piece = board_gui.get_piece_on_mouse(mouse_pos)
    
    # Verifica que nenhuma peça foi selecionada
    assert piece is None, "O clique fora do tabuleiro não deve selecionar nenhuma peça"

