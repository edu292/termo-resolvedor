from unidecode import unidecode
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from enum import Enum, auto


class Dica(Enum):
    LETRA_ERRADA = auto()
    LETRA_LUGAR_ERRADO = auto()
    LETRA_CERTA = auto()


class Tabuleiro:
    def __init__(self, tabuleiro, dicionario, numero_linhas):
        self.tabuleiro = tabuleiro
        self.palavras_possiveis = dicionario
        self.numero_linhas = numero_linhas
        self.palavra_desconhecida = False

    def analisar_dicas(self, dicas):
        letras_certas = []
        letras_erradas = set()
        letras_lugar_errado = []
        for indice, (letra, tipo) in enumerate(dicas):
            if tipo == Dica.LETRA_ERRADA and letra not in letras_erradas:
                letras_erradas.add(letra)
            elif tipo == Dica.LETRA_LUGAR_ERRADO:
                letras_lugar_errado.append((letra, indice))
            elif tipo == Dica.LETRA_CERTA:
                letras_certas.append((letra, indice))
        letras_erradas -= {lc for lc, _ in letras_certas}
        letras_erradas -= {lle for lle, _ in letras_lugar_errado}
        novas_palavras_possiveis = []
        for palavra in self.palavras_possiveis:
            if any(palavra[i] != l for l, i in letras_certas):
                continue
            if any(l not in palavra or palavra[i] == l for l, i in letras_lugar_errado):
                continue
            if letras_erradas.intersection(palavra):
                continue
            novas_palavras_possiveis.append(palavra)
        self.palavras_possiveis = novas_palavras_possiveis
        print(self.palavras_possiveis)
        if len(self.palavras_possiveis) == 0:
            self.palavra_desconhecida = True


class Partida:
    def __init__(self, tabuleiros, html_body):
        self.linha_atual = 0
        self.tabuleiros = tabuleiros
        self.html_body = html_body
        self.numero_linhas = int(tabuleiros[0].get_attribute('rows'))
        self.dicionario = ler_dicionario()
        self.palavra_desconhecida = False

    def resolver(self):
        for indice_tabuleiro, tabuleiro in enumerate(self.tabuleiros, 1):
            tabuleiro_obj = Tabuleiro(tabuleiro, self.dicionario, self.numero_linhas)
            for indice_linha in range(0, self.numero_linhas):
                if indice_linha == self.linha_atual:
                    self.linha_atual += 1
                    self.html_body.send_keys(tabuleiro_obj.palavras_possiveis[0])
                    self.html_body.send_keys(Keys.ENTER)
                    sleep(2)
                tabuleiro_concluido, dicas = verificar_tabuleiro(tabuleiro, indice_linha)
                if tabuleiro_concluido:
                    break
                tabuleiro_obj.analisar_dicas(dicas)
                if tabuleiro_obj.palavra_desconhecida:
                    self.palavra_desconhecida = True
                    print(f'Palavra desconhecida no tabuleiro {indice_tabuleiro}')
                    break
        if self.palavra_desconhecida:
            self.aprender_palavra()

    def aprender_palavra(self):
        print('Completando linhas')
        numero_linhas_faltando = self.numero_linhas - self.linha_atual
        for a in range(0, numero_linhas_faltando):
            self.html_body.send_keys('teste')
            self.html_body.send_keys(Keys.ENTER)
            sleep(2)
        notificacao = body.find_element(By.XPATH, '/html/body/wc-notify').text
        palavras_partida = notificacao[notificacao.index(':') + 2:].split(' ')
        with open('palavras.txt', 'a') as txt:
            for palavra in palavras_partida:
                palavra = unidecode(palavra.strip(','))
                if palavra not in self.dicionario:
                    print(f'Palavra adicionada: {palavra}')
                    txt.write(palavra + '\n')


def verificar_tabuleiro(tabuleiro, indice_linha):
    dicas = []
    linha = tabuleiro.shadow_root.find_element(By.CSS_SELECTOR, f'wc-row[termo-row="{indice_linha}"]').shadow_root
    for indice_coluna in range(0, 5):
        celula = linha.find_element(By.CSS_SELECTOR, f'div[lid="{indice_coluna}"]')
        classe = celula.get_attribute('class')
        letra = celula.text.lower()
        letra = unidecode(letra)
        if classe == 'letter right done':
            return 1, []
        elif classe == 'letter wrong':
            dicas.append((letra, Dica.LETRA_ERRADA))
        elif classe == 'letter place':
            dicas.append((letra, Dica.LETRA_LUGAR_ERRADO))
        elif classe == 'letter right':
            dicas.append((letra, Dica.LETRA_CERTA))

    return 0, dicas


def ler_dicionario():
    with open('palavras.txt', 'a+') as txt:
        txt.seek(0)
        dicionario =  txt.read().splitlines()

    return dicionario


modo = input()
url = 'https://term.ooo/'
if modo == '2' or modo == '4':
    url += modo

options = Options()
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options)
driver.get(url)
body = driver.find_element(By.XPATH, '/html/body')
body.click()

elementos_tabuleiros = body.find_elements(By.CSS_SELECTOR, 'wc-board')
partida = Partida(elementos_tabuleiros, body)
partida.resolver()
