# Resolvedor Automático do Termo

Um projeto que **resolve automaticamente o jogo Termo** usando técnicas de web scraping, filtragem inteligente de palavras e lógica de tentativa. Cada letra e dica são analisadas e levadas em consideração para realizar a filtragem a partir do banco de palavras do script. Sempre que o bot se depara com uma palavra ele a aprende e em jogos futuros pode utiliza-la

---

## 🧩 Como funciona?

- O bot começa com uma palavra inicial
- Recebe as dicas (letras corretas, letras fora de posição, letras erradas).
- Filtra as palavras internas com base nas pistas recebidas.
- Faz uma nova tentativa, repetindo o processo até encontrar a palavra certa.
- Caso não encontre a palavra do tabuleiro, pula para o próximo.
- Chega até o final do jogo e registra a palavra no dicionário com base na mensagem de derrota.

---

## 🕹️ Como usar
| Modo de Jogo | Entrada |
|--------------|---------|
| Termo        | ``ENTER``     |
| Dueto        | 2 + ``ENTER`` |
| Quarteto     | 4 + ``ENTER`` |

---

## ⚙️ Como Rodar

Baixe as dependências:
```
pip install requirements.txt
```

Execute o script
```
python main.py
```

---

---

## 🔍 Preview
![pycharm64_3fX0FXg5FK](https://github.com/user-attachments/assets/c10e3caa-b35e-4ecd-bff3-4a80bf788703)


---
