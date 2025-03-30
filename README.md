## Interpolação de Imagens (Vizinho Mais Próximo e Bilinear)

Projeto desenvolvido como parte da disciplina **Processamento de Imagens**, na **Universidade Federal do Tocantins (UFT)**.

### Descrição
Este projeto implementa dois métodos de interpolação de imagens em tons de cinza:

- **Vizinho mais próximo** (com mapeamento corrigido)
- **Interpolação bilinear** (implementação manual)

A imagem usada é uma matriz 6x6 com contraste central, sendo ampliada para 9x9 e reduzida para 4x4. O objetivo é visualizar o efeito de cada técnica em diferentes escalas.

### Tecnologias
- Python 3
- NumPy
- Matplotlib

### Como executar
```bash
pip install numpy matplotlib
python interpolacao.py
```

### Imagens geradas
O script exibe visualmente:
- A imagem original
- A ampliação por cada método
- A redução por cada método
- Os valores dos pixels são mostrados sobre cada célula da matriz, facilitando a análise.

### Sobre
Este projeto foi desenvolvido como exercício acadêmico.

- **Aluno(a):** Laura Barbosa Henrique  
- **Email acadêmico:** laura.henrique@mail.uft.edu.br  
- **Professora:** Glenda Botelho
