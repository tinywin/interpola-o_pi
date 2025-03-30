# Aluna: Laura Barbosa Henrique
# Matrícula: 2022216981
# Código 1 - interpolação
# Data: 28/03/2025
# Universidade Federal do Tocantins
# Disciplina: Processamento de Imagens
# Descrição: Código para interpolação de imagens usando vizinho mais próximo e bilinear
import numpy as np
import matplotlib.pyplot as plt

def plot_matrix(ax, matrix, title, xlabel):
    ax.imshow(matrix, cmap='gray', interpolation='none')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.axis('off')
    rows, cols = matrix.shape
    for i in range(rows):
        for j in range(cols):
            ax.text(j, i, f"{int(matrix[i, j])}", ha='center', va='center',
                    color='white' if matrix[i, j] < 128 else 'black', fontsize=8)

# Vizinho mais próximo - com correção
def nearest_neighbor_interpolation(img, new_shape):
    old_h, old_w = img.shape
    new_h, new_w = new_shape
    result = np.zeros((new_h, new_w), dtype=np.uint8)

    for i in range(new_h):
        for j in range(new_w):
            x = (i + 0.5) * old_h / new_h - 0.5
            y = (j + 0.5) * old_w / new_w - 0.5
            orig_x = min(int(round(x)), old_h - 1)
            orig_y = min(int(round(y)), old_w - 1)
            result[i, j] = img[orig_x, orig_y]
    return result

# Bilinear manual
def bilinear_interpolation(img, new_shape):
    old_h, old_w = img.shape
    new_h, new_w = new_shape
    result = np.zeros((new_h, new_w), dtype=np.uint8)

    for i in range(new_h):
        for j in range(new_w):
            x = i * (old_h - 1) / (new_h - 1)
            y = j * (old_w - 1) / (new_w - 1)

            x0 = int(np.floor(x))
            y0 = int(np.floor(y))
            x1 = min(x0 + 1, old_h - 1)
            y1 = min(y0 + 1, old_w - 1)

            dx = x - x0
            dy = y - y0

            Q11 = img[x0, y0]
            Q21 = img[x1, y0]
            Q12 = img[x0, y1]
            Q22 = img[x1, y1]

            R1 = Q11 * (1 - dx) + Q21 * dx
            R2 = Q12 * (1 - dx) + Q22 * dx
            P = R1 * (1 - dy) + R2 * dy

            result[i, j] = int(round(P))

    return result

# Matriz base 6x6
img = np.array([
    [10, 10, 200, 200, 10, 10],
    [10, 200, 250, 250, 200, 10],
    [200, 250, 100, 100, 250, 200],
    [200, 250, 100, 100, 250, 200],
    [10, 200, 250, 250, 200, 10],
    [10, 10, 200, 200, 10, 10]
], dtype=np.uint8)

# Novos tamanhos
shape_up = (9, 9)
shape_down = (4, 4)

# Interpolações
nearest_up = nearest_neighbor_interpolation(img, shape_up)
bilinear_up = bilinear_interpolation(img, shape_up)
nearest_down = nearest_neighbor_interpolation(img, shape_down)
bilinear_down = bilinear_interpolation(img, shape_down)

# Exibição
fig, axs = plt.subplots(2, 3, figsize=(15, 9))

plot_matrix(axs[0, 0], img, "Imagem Original (6x6)", "Matriz com contraste central e bordas.")
plot_matrix(axs[0, 1], nearest_up, "Ampliação (9x9) - Vizinho", "Interpolação correta por vizinho mais próximo.")
plot_matrix(axs[0, 2], bilinear_up, "Ampliação (9x9) - Bilinear", "Interpolação bilinear manual.")

axs[1, 0].axis('off')
plot_matrix(axs[1, 1], nearest_down, "Redução (4x4) - Vizinho", "Redução correta com vizinho mais próximo.")
plot_matrix(axs[1, 2], bilinear_down, "Redução (4x4) - Bilinear", "Redução com interpolação bilinear.")

plt.tight_layout()
plt.show() 