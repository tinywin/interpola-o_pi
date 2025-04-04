# -----------------------------------------------------------
# IMPORTAÇÃO DE BIBLIOTECAS
# -----------------------------------------------------------
import numpy as np                    # Usada para criar e manipular matrizes (arrays numéricos)
import matplotlib.pyplot as plt       # Usada para exibir as imagens (gráficos)

# -----------------------------------------------------------
# FUNÇÃO PARA EXIBIR MATRIZ COMO IMAGEM
# -----------------------------------------------------------
def plot_matrix(ax, matrix, title, xlabel):
    """
    Exibe a imagem (matriz) em escala de cinza e escreve o valor de cada pixel.
    """
    ax.imshow(matrix, cmap='gray', interpolation='none')   # Mostra a imagem sem interpolação
    ax.set_title(title)                                    # Define o título da imagem
    ax.set_xlabel(xlabel)                                  # Texto abaixo da imagem
    ax.axis('off')                                         # Remove os eixos (estético)

    # Escreve o valor de cada pixel por cima da imagem
    rows, cols = matrix.shape
    for i in range(rows):
        for j in range(cols):
            ax.text(j, i, f"{int(matrix[i, j])}",
                    ha='center', va='center',
                    color='white' if matrix[i, j] < 128 else 'black',
                    fontsize=8)

# -----------------------------------------------------------
# INTERPOLAÇÃO POR VIZINHO MAIS PRÓXIMO (CORRIGIDA)
# -----------------------------------------------------------
def nearest_neighbor_interpolation(img, new_shape):
    """
    Redimensiona a imagem usando interpolação por vizinho mais próximo.
    Para cada pixel novo, escolhe o valor mais próximo da imagem original.
    """
    old_h, old_w = img.shape           # Altura e largura da imagem original
    new_h, new_w = new_shape           # Nova altura e largura desejadas

    result = np.zeros((new_h, new_w), dtype=np.uint8)   # Nova imagem preenchida com zeros

    for i in range(new_h):
        for j in range(new_w):
            # Mapeia a posição nova (i,j) para a posição correspondente na imagem original
            x = i * (old_h - 1) / (new_h - 1) if new_h > 1 else 0
            y = j * (old_w - 1) / (new_w - 1) if new_w > 1 else 0

            # Arredonda para pegar o índice do pixel mais próximo
            orig_x = int(round(x))
            orig_y = int(round(y))

            # Garante que não ultrapasse os limites da matriz original
            orig_x = max(0, min(orig_x, old_h - 1))
            orig_y = max(0, min(orig_y, old_w - 1))

            # Atribui o valor do pixel original correspondente
            result[i, j] = img[orig_x, orig_y]

    return result

# -----------------------------------------------------------
# INTERPOLAÇÃO BILINEAR (MANUAL)
# -----------------------------------------------------------
def bilinear_interpolation(img, new_shape):
    """
    Redimensiona a imagem usando interpolação bilinear.
    Calcula a média ponderada dos 4 pixels vizinhos mais próximos.
    """
    old_h, old_w = img.shape
    new_h, new_w = new_shape
    result = np.zeros((new_h, new_w), dtype=np.uint8)

    for i in range(new_h):
        for j in range(new_w):
            # Mapeia a posição nova (i,j) para a posição original (x,y)
            x = i * (old_h - 1) / (new_h - 1) if new_h > 1 else 0
            y = j * (old_w - 1) / (new_w - 1) if new_w > 1 else 0

            # Define os vizinhos ao redor (superior/inferior e esquerdo/direito)
            x0 = int(np.floor(x))
            y0 = int(np.floor(y))
            x1 = min(x0 + 1, old_h - 1)
            y1 = min(y0 + 1, old_w - 1)

            # Distância fracionária entre x e x0, e entre y e y0
            dx = x - x0
            dy = y - y0

            # Pega os 4 pixels vizinhos
            Q11 = img[x0, y0]
            Q21 = img[x1, y0]
            Q12 = img[x0, y1]
            Q22 = img[x1, y1]

            # Interpola na horizontal (x) primeiro
            R1 = Q11 * (1 - dx) + Q21 * dx
            R2 = Q12 * (1 - dx) + Q22 * dx

            # Interpola na vertical (y) depois
            P = R1 * (1 - dy) + R2 * dy

            # Atribui o valor final ao pixel novo
            result[i, j] = int(round(P))

    return result

# -----------------------------------------------------------
# IMAGEM BASE: MATRIZ 6x6 COM CONTRASTE
# -----------------------------------------------------------
img = np.array([
    [10, 10, 200, 200, 10, 10],
    [10, 200, 250, 250, 200, 10],
    [200, 250, 100, 100, 250, 200],
    [200, 250, 100, 100, 250, 200],
    [10, 200, 250, 250, 200, 10],
    [10, 10, 200, 200, 10, 10]
], dtype=np.uint8)

# -----------------------------------------------------------
# TAMANHOS DE INTERPOLAÇÃO
# -----------------------------------------------------------
shape_up = (9, 9)    # Aumentar para 9x9 (ampliação)
shape_down = (4, 4)  # Reduzir para 4x4 (redução)

# -----------------------------------------------------------
# APLICA AS INTERPOLAÇÕES
# -----------------------------------------------------------
# Ampliação por vizinho e bilinear
nearest_up = nearest_neighbor_interpolation(img, shape_up)
bilinear_up = bilinear_interpolation(img, shape_up)

# Redução por vizinho e bilinear
nearest_down = nearest_neighbor_interpolation(img, shape_down)
bilinear_down = bilinear_interpolation(img, shape_down)

# -----------------------------------------------------------
# EXIBIÇÃO DAS IMAGENS
# -----------------------------------------------------------
# Cria um grid 2x3 para mostrar todas as imagens
fig, axs = plt.subplots(2, 3, figsize=(15, 9))

# Primeira linha: imagem original e ampliações
plot_matrix(axs[0, 0], img, "Imagem Original (6x6)", "Matriz com contraste central e bordas.")
plot_matrix(axs[0, 1], nearest_up, "Ampliação (9x9) - Vizinho", "Interpolação por vizinho mais próximo.")
plot_matrix(axs[0, 2], bilinear_up, "Ampliação (9x9) - Bilinear", "Interpolação bilinear manual.")

# Segunda linha: reduções
axs[1, 0].axis('off')  # Espaço em branco
plot_matrix(axs[1, 1], nearest_down, "Redução (4x4) - Vizinho", "Redução por vizinho mais próximo.")
plot_matrix(axs[1, 2], bilinear_down, "Redução (4x4) - Bilinear", "Redução por interpolação bilinear.")

# Ajusta o layout dos gráficos
plt.tight_layout()
plt.show()
