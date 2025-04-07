# 🤖 Resolvedor Automático do Termo

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Em%20desenvolvimento-yellow?style=for-the-badge)
![Web Scraping](https://img.shields.io/badge/WebScraping-BeautifulSoup-red?style=for-the-badge)
![Automação](https://img.shields.io/badge/Automação-Bot-green?style=for-the-badge)

Um projeto que **resolve automaticamente o jogo Termo** usando técnicas de web scraping, filtragem inteligente de palavras e lógica de tentativa. Ideal para estudar **estratégias de automação, algoritmos de eliminação e manipulação de dados com Python**.

---

## 🔍 Preview

<p align="center">
  <img src="https://via.placeholder.com/600x300?text=Simula%C3%A7%C3%A3o+do+Resolvedor+do+Termo" alt="Preview do bot jogando o Termo" />
</p>

---

## 🧩 Como funciona?

1. O bot começa com uma palavra inicial
2. Verifica o retorno (letras corretas, letras fora de posição, letras inválidas).
3. Filtra as palavras do dicionário interno com base nas pistas recebidas.
4. Faz uma nova tentativa, repetindo o processo até encontrar a palavra certa.
5. As palavras possíveis são exibidas no terminal a cada filtragem.
6. Caso se depare com uma palavra que não conheça em um tabuleiro, ele resolve o próximo.
7. Chega até o final do jogo e registra a palavra no dicionário com base na mensagem de derrota.

---
