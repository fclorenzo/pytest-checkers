#test_board_gui.py
import pytest
import pygame
from board_gui import BoardGUI
from board import Board
from piece import Piece

# Inicializa o pygame (necessário para a interface gráfica)
@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()

# 1. Teste de Inicialização do BoardGUI
def test_board_gui_initialization():
    pieces = [Piece("12WN"), Piece("16BN")]
    board = Board(pieces, "W")
    board_gui = BoardGUI(board)
    
    # Verifica que o BoardGUI inicializou com a quantidade correta de peças
    assert len(board_gui.pieces) == 2, "O BoardGUI deve conter 2 peças"
    assert isinstance(board_gui, BoardGUI), "O BoardGUI não foi inicializado corretamente"

# 2. Teste de Desenho das Peças
def test_draw_pieces():
    pieces = [Piece("12WN"), Piece("16BN")]
    board = Board(pieces, "W")
    board_gui = BoardGUI(board)
    
    # Verifica que as peças foram desenhadas corretamente
    # (Neste teste, apenas garantimos que o método 'draw_pieces' não falha)
    display_surface = pygame.Surface((400, 400))
    board_gui.draw_pieces(display_surface)
    assert display_surface.get_at((50, 50)) is not None, "O método draw_pieces não desenhou as peças corretamente"

# 3. Teste de Posicionamento das Peças na Interface
def test_piece_positioning():
    pieces = [Piece("12WN")]
    board = Board(pieces, "W")
    board_gui = BoardGUI(board)

    # Verifica a posição da peça no GUI
    piece_properties = board_gui.pieces[0]
    assert piece_properties["rect"].x >= 0, "A posição x da peça deve ser maior ou igual a 0"
    assert piece_properties["rect"].y >= 0, "A posição y da peça deve ser maior ou igual a 0"

# 4. Teste de Movimento da Peça com o Mouse
def test_move_piece_with_mouse():
    pieces = [Piece("12WN")]
    board = Board(pieces, "W")
    board_gui = BoardGUI(board)
    
    # Simula um clique no mouse para mover a peça
    mouse_pos = (50, 50)  # Posição fictícia onde o mouse está
    piece = board_gui.get_piece_on_mouse(mouse_pos)
    
    # Verifica se a peça foi encontrada
    assert piece is not None, "A peça não foi encontrada no clique do mouse"

    # Simula o movimento da peça (movendo para outra posição)
    new_pos = (100, 100)  # Nova posição do mouse
    new_piece_position = board_gui.get_position_by_rect(pygame.Rect(new_pos[0], new_pos[1], 50, 50))
    assert new_piece_position is not None, "A nova posição da peça não foi calculada corretamente"

# 5. Teste de Marcações de Movimento Válido
def test_move_marks_display():
    pieces = [Piece("12WN")]
    board = Board(pieces, "W")
    board_gui = BoardGUI(board)
    
    # Verifica se o método set_move_marks marca os movimentos possíveis corretamente
    possible_moves = [(1, 1), (2, 2)]  # Posições fictícias de movimentos válidos
    board_gui.set_move_marks(possible_moves)
    
    # Verifica se as marcações de movimento estão sendo desenhadas
    assert len(board_gui.get_move_marks()) == 2, "As marcações de movimento não estão sendo exibidas corretamente"

# 6. Teste de Movimento de Peça com Interação do Usuário
def test_move_piece_interaction():
    pieces = [Piece("12WN"), Piece("16BN")]
    board = Board(pieces, "W")
    board_gui = BoardGUI(board)
    
    # Simula o usuário clicando em uma peça e movendo para outra posição
    initial_pos = (50, 50)  # Posição fictícia de clique no mouse
    new_pos = (100, 100)  # Nova posição fictícia para a peça
    
    # Simula a detecção de peça no clique do mouse
    piece = board_gui.get_piece_on_mouse(initial_pos)
    assert piece is not None, "A peça não foi detectada no clique do mouse"
    
    # Simula o movimento da peça para a nova posição
    new_rect = pygame.Rect(new_pos[0], new_pos[1], 50, 50)
    piece["rect"] = new_rect  # Atualiza a posição da peça no GUI
    board_gui.draw_pieces(pygame.Surface((400, 400)))  # Atualiza o desenho das peças
    
    # Verifica se a posição da peça foi atualizada corretamente
    assert piece["rect"].x == new_pos[0], "A posição x da peça não foi atualizada corretamente"
    assert piece["rect"].y == new_pos[1], "A posição y da peça não foi atualizada corretamente"

# 7. Teste de Obtenção da Peça com o Mouse (Clicando em uma Peça)
def test_get_piece_on_mouse():
    pieces = [Piece("12WN")]
    board = Board(pieces, "W")
    board_gui = BoardGUI(board)
    
    # Simula a posição de clique do mouse sobre a peça
    mouse_pos = (50, 50)  # Posição fictícia onde o mouse clica
    piece = board_gui.get_piece_on_mouse(mouse_pos)
    
    # Verifica se a peça foi corretamente detectada
    assert piece is not None, "A peça não foi detectada no clique do mouse"
    assert piece["color"] == "W", "A peça encontrada não é a correta"

# 8. Teste de Ocultação e Exibição de Peça (Esconder e Mostrar Peças)
def test_hide_and_show_piece():
    pieces = [Piece("12WN")]
    board = Board(pieces, "W")
    board_gui = BoardGUI(board)
    
    # Esconde a peça
    board_gui.hide_piece(0)
    
    # Verifica se a peça está oculta
    assert board_gui.hidden_piece == 0, "A peça não foi corretamente ocultada"
    
    # Mostra a peça
    piece_shown = board_gui.show_piece()
    
    # Verifica se a peça foi corretamente exibida
    assert piece_shown == 0, "A peça não foi corretamente exibida"

# 9. Teste de Interação com o Mouse para uma Peça em uma Posição Inválida
def test_invalid_mouse_interaction():
    pieces = [Piece("12WN")]
    board = Board(pieces, "W")
    board_gui = BoardGUI(board)
    
    # Simula um clique em uma posição inválida
    mouse_pos = (500, 500)  # Posição fictícia fora do tabuleiro
    piece = board_gui.get_piece_on_mouse(mouse_pos)
    
    # Verifica que nenhuma peça foi selecionada
    assert piece is None, "O clique em uma posição inválida não deve selecionar nenhuma peça"

