from unidecode import unidecode
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver


def ler_dicionario():
    with open('palavras.txt', 'r') as txt:
        palavras = txt.read().splitlines()

    return palavras


def aprender_palavra():
    print('Completando linhas')
    numeroLinhasFaltando = numero_linhas - linha_atual
    for a in range(0, numeroLinhasFaltando):
        body.send_keys('teste')
        body.send_keys(Keys.ENTER)
        sleep(2)
    notificacao = driver.find_element(By.XPATH, '/html/body/wc-notify').text
    palavrasPartida = notificacao[notificacao.index(':') + 2:].split(' ')
    with open('palavras.txt', 'a') as txt:
        for palavra in palavrasPartida:
            palavra = unidecode(palavra).strip(',')
            if palavra not in dicionario:
                print(f'Palavra adicionada: {palavra}')
                txt.write(palavra + '\n')


def analisar_dicas(indice_linha, palavras_possiveis):
    linha = tabuleiro.shadow_root.find_element(By.CSS_SELECTOR, f'wc-row[termo-row="{indice_linha}"]').shadow_root
    letras_certas = []
    letras_erradas = []
    for indice_coluna in range(0, 5):
        celula = linha.find_element(By.CSS_SELECTOR, f'div[lid="{indice_coluna}"]')
        classe = celula.get_attribute('class')
        letra = celula.text.lower()
        letra = unidecode(letra)
        if classe == 'letter right done':
            return 1, palavras_possiveis
        elif classe == 'letter wrong' and letra not in letras_erradas:
            palavras_possiveis = [palavra for palavra in palavras_possiveis if palavra[indice_coluna] != letra]
            letras_erradas.append(letra)
        elif classe == 'letter place':
            palavras_possiveis = [palavra for palavra in palavras_possiveis if letra in palavra and palavra[indice_coluna] != letra]
            letras_certas.append(letra)
        elif classe == 'letter right':
            palavras_possiveis = [palavra for palavra in palavras_possiveis if palavra[indice_coluna] == letra]
            letras_certas.append(letra)
    letras_erradas = [letra for letra in letras_erradas if letra not in letras_certas]
    for letra_errada in letras_erradas:
        palavras_possiveis = [palavra for palavra in palavras_possiveis if letra_errada not in palavra]

    return 0, palavras_possiveis


dicionario = ler_dicionario()
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
linha_atual = 0
tabuleiros = body.find_elements(By.CSS_SELECTOR, 'wc-board')
palavra_desconhecida = False
for tabuleiro in tabuleiros:
    palavras_possiveis = dicionario
    numero_linhas = int(tabuleiro.get_attribute('rows'))
    for indice_linha in range(0, numero_linhas):
        if indice_linha == linha_atual:
            linha_atual += 1
            body.send_keys(palavras_possiveis[0])
            body.send_keys(Keys.ENTER)
            sleep(2)
        finalizado, palavras_possiveis = analisar_dicas(indice_linha, palavras_possiveis)
        if finalizado:
            break
        if len(palavras_possiveis) == 0:
            palavra_desconhecida = True
            print(f'Palavra desconhecida no tabuleiro {tabuleiros.index(tabuleiro) + 1}')
            indice_linha += 1
            break
        print(palavras_possiveis)

if palavra_desconhecida:
    aprender_palavra()
