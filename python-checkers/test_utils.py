#test_utils.py
import pytest
from utils import get_position_with_row_col, get_piece_position, get_piece_gui_coords, get_surface_mouse_offset

# 1. Teste da função get_position_with_row_col
@pytest.mark.parametrize("row, col, expected_position", [
    (0, 0, 0),  # Primeira linha, primeira coluna
    (1, 1, 3),  # Segunda linha, segunda coluna
    (7, 7, 31), # Última linha, última coluna
    (3, 2, 9),  # Linha 3, coluna 2
])
def test_get_position_with_row_col(row, col, expected_position):
    result = get_position_with_row_col(row, col)
    assert result == expected_position, f"Esperado {expected_position}, mas obteve {result}"

# Teste de valores fora do limite do tabuleiro
@pytest.mark.parametrize("row, col", [
    (-1, 0),  # Linha negativa
    (0, -1),  # Coluna negativa
    (8, 0),   # Linha fora dos limites (tabuleiro vai de 0 a 7)
    (0, 8),   # Coluna fora dos limites (tabuleiro vai de 0 a 7)
])
def test_get_position_with_row_col_out_of_bounds(row, col):
    with pytest.raises(ValueError):
        get_position_with_row_col(row, col)

# 2. Teste da função get_piece_position
def test_get_piece_position():
    # Teste de conversão de posição de peça para coordenada do tabuleiro
    coords = (56, 56)  # Posição fictícia do mouse na interface gráfica
    square_dist = 56  # Distância entre os quadrados no tabuleiro
    top_left_coords = (34, 34)  # Posição inicial do tabuleiro
    result = get_piece_position(coords, square_dist, top_left_coords)
    
    # Esperado: posição 12 (considerando que a peça está na posição 12 do tabuleiro)
    assert result == 12, f"Esperado 12, mas obteve {result}"

# 3. Teste da função get_piece_gui_coords
@pytest.mark.parametrize("row, col, square_dist, top_left_coords, expected_coords", [
    (0, 0, 56, (34, 34), (34, 34)),  # Primeira linha, primeira coluna
    (1, 1, 56, (34, 34), (90, 90)),  # Segunda linha, segunda coluna
    (7, 7, 56, (34, 34), (318, 318)), # Última linha, última coluna
    (3, 2, 56, (34, 34), (178, 178)),  # Linha 3, coluna 2
])
def test_get_piece_gui_coords(row, col, square_dist, top_left_coords, expected_coords):
    result = get_piece_gui_coords((row, col), square_dist, top_left_coords)
    assert result == expected_coords, f"Esperado {expected_coords}, mas obteve {result}"

# Teste de valores fora do limite do tabuleiro para coordenadas gráficas
@pytest.mark.parametrize("row, col, square_dist, top_left_coords", [
    (-1, 0, 56, (34, 34)),  # Linha negativa
    (0, -1, 56, (34, 34)),  # Coluna negativa
    (8, 0, 56, (34, 34)),   # Linha fora dos limites
    (0, 8, 56, (34, 34)),   # Coluna fora dos limites
])
def test_get_piece_gui_coords_out_of_bounds(row, col, square_dist, top_left_coords):
    with pytest.raises(ValueError):
        get_piece_gui_coords((row, col), square_dist, top_left_coords)

# 4. Teste da função get_surface_mouse_offset
@pytest.mark.parametrize("surface_pos, mouse_pos, expected_offset", [
    ((34, 34), (50, 50), (16, 16)),  # O mouse está a 16 pixels de distância da superfície
    ((100, 100), (150, 150), (50, 50)),  # Distância de 50 pixels
    ((0, 0), (0, 0), (0, 0)),  # Posições iguais, sem deslocamento
])
def test_get_surface_mouse_offset(surface_pos, mouse_pos, expected_offset):
    result = get_surface_mouse_offset(surface_pos, mouse_pos)
    assert result == expected_offset, f"Esperado {expected_offset}, mas obteve {result}"

