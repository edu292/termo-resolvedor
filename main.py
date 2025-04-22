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
        self.palavra_deconhecida = False

    def analisar_dicas(self, dicas):
        letras_certas = []
        letras_erradas = []
        for indice, (letra, tipo) in enumerate(dicas):
            if tipo == Dica.LETRA_ERRADA and letra not in letras_erradas:
                self.palavras_possiveis = [palavra for palavra in self.palavras_possiveis if palavra[indice] != letra]
                letras_erradas.append(letra)
            elif tipo == Dica.LETRA_LUGAR_ERRADO:
                self.palavras_possiveis = [palavra for palavra in self.palavras_possiveis
                                           if letra in palavra and palavra[indice] != letra]
                letras_certas.append(letra)
            elif tipo == Dica.LETRA_CERTA:
                self.palavras_possiveis = [palavra for palavra in self.palavras_possiveis if palavra[indice] == letra]
                letras_certas.append(letra)
        letras_erradas = [letra for letra in letras_erradas if letra not in letras_certas]
        for letra_errada in letras_erradas:
            self.palavras_possiveis = [palavra for palavra in self.palavras_possiveis if letra_errada not in palavra]
        print(self.palavras_possiveis)
        if len(self.palavras_possiveis) == 0:
            self.palavra_deconhecida = True


class Partida:
    def __init__(self, tabuleiros, html_body):
        self.linha_atual = 0
        self.tabuleiros = tabuleiros
        self.html_body = html_body
        self.numero_linhas = int(tabuleiros[0].get_attribute('rows'))
        self.dicionario = ler_dicionario()
        self.palavra_desconhecida = False

    def resolver(self):
        for tabuleiro in self.tabuleiros:
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
                if tabuleiro_obj.palavra_deconhecida:
                    self.palavra_desconhecida = True
                    print(f'Palavra desconhecida no tabuleiro {elementos_tabuleiros.index(tabuleiro) + 1}')
                    indice_linha += 1
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
        notificacao = driver.find_element(By.XPATH, '/html/body/wc-notify').text
        palavras_partida = notificacao[notificacao.index(':') + 2:].strip(',').split(' ')
        with open('palavras.txt', 'a') as txt:
            for palavra in palavras_partida:
                palavra = unidecode(palavra)
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
            return 1, 0
        elif classe == 'letter wrong':
            dicas.append((letra, Dica.LETRA_ERRADA))
        elif classe == 'letter place':
            dicas.append((letra, Dica.LETRA_LUGAR_ERRADO))
        elif classe == 'letter right':
            dicas.append((letra, Dica.LETRA_CERTA))

    return 0, dicas


def ler_dicionario():
    with open('palavras.txt', 'r') as txt:
        dicionario = txt.read().splitlines()

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
