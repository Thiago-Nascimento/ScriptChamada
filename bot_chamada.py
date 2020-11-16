from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

import getpass
import time
from datetime import datetime

import json

class BotChamada:
    def __init__(self, navegador):
        self.navegador = navegador
        self.lista_de_participantes = []
        self.url = ""
        
        if navegador == "firefox":
            options = FirefoxOptions()
            
            options.set_preference("permissions.default.microphone", 1)
            options.set_preference("permissions.default.camera", 1)
            options.set_preference("media.volume_scale", "0.0")

            self.driver = webdriver.Firefox(options=options, executable_path=r".\geckodriver-v0.28.0-win64\geckodriver.exe")
        elif navegador == "chrome":
            self.driver = webdriver.Chrome(executable_path=r".\chromedriver_win32\chromedriver.exe")

    def login(self, email, senha):
        driver = self.driver
        
        driver.get("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow")
        
        driver.find_element_by_xpath("//input[@id='identifierId']").send_keys(email)
        
        # Next Button:
        driver.find_element_by_xpath("//div[@id='identifierNext']").click()
        time.sleep(5)
        
        #Password:
        driver.find_element_by_xpath("//input[@name='password']").send_keys(senha)
            #next button:
        driver.find_element_by_xpath("//*[@id='passwordNext']/div/button").click()
        time.sleep(1)
            
    def fazer_chamada(self, url):
        self.url = url
        driver = self.driver
        lista_de_participantes = self.lista_de_participantes
        
        driver.get(url)
        time.sleep(5)

        # Mutar mic e desativar camera
        driver.find_element_by_xpath("//div[@data-tooltip='Desativar microfone (ctrl + d)']").click()
        driver.find_element_by_xpath("//div[@data-tooltip='Desativar câmera (ctrl + e)']").click()
        time.sleep(5)

        # Clicar em participar
        driver.find_element_by_xpath("/html/body/div[1]/c-wiz/div/div/div[7]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div/div[1]/span/span").click()
        time.sleep(5)

        # Mostrar participantes
        driver.find_element_by_xpath("//div[@data-tooltip='Mostrar todos']").click()

        # Pegar elementos de class=ZjFb7c, que são <span>, onde o inner text é o nome de um participante
        participantes = driver.find_elements_by_class_name("ZjFb7c")

        for participante in participantes:
            nome = participante.get_attribute('innerText')
            lista_de_participantes.append(nome)

        # Mostrar o numero de participantes e os nomes deles na tela
        num_de_participantes = len(lista_de_participantes)
        
        print("Número de participantes:", num_de_participantes)
        print("\nLista de Participantes:")
        
        for nome in lista_de_participantes:
            print(nome)

    def exportar_lista(self):
        # Exportar para um arquivo .txt
        driver = self.driver
        reuniao = self.url
        lista = self.lista_de_participantes

        timestamp = "{:%d_%m_%Y_%H%M%S}".format(datetime.now())

        arquivo = open(r".\listas\meet_"+timestamp, "x")

        arquivo.write("Reuniao: " + reuniao + "\n")
        arquivo.write("Data e Hora: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n\n")
        arquivo.write("Lista de Participantes:\n\n")

        for nome in lista:
            arquivo.write(nome + "\n")

        arquivo.close()
        driver.close()
        
print("\nBot para gerar lista de presença de uma Reunião no Google Meet.")
print("Repositório do projeto: https://github.com/Thiago-Nascimento/ScriptChamada\n")

f = open("config.json")
config = json.load(f)
f.close()

# reuniao = str(input("\nInsira a url da reunião: "))
reuniao = "https://meet.google.com/rah-viep-vuo"


email = config["email"]
senha = config["senha"]
navegador = config["navegador"]

dia_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

print("\nEmail de entrada:", email)
print("Reunião:", reuniao)
print("Data e hora: " + dia_hora + "\n")

bot = BotChamada(navegador)
bot.login(email, senha)
bot.fazer_chamada(reuniao)
bot.exportar_lista()
