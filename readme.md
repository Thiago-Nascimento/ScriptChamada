# Bot para Listar participantes de uma chamada no Google Meet
Esse script abre o navegador utlizando as credenciais fornecidas no arquivo config.json.

**No arquivo config.json, insira seu email e senha para logar em uma conta Google, e redirecionar para a chamada no Meet.**

Com esses dados o bot entra na reunião com o email inserido, e armazana o nome de todos os integrantes da reunião, exportando para um arquivo .txt (localizado em uma pasta chamada listas).

## Necessário ter o Python 3 instalado
Windows:
[Python 3.9](https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe).

Com o Python instalado, execute o comando:
```
pip install selenium
```

Após o selenium instalado, o script já pode ser executado:
```
python .\bot_chamada.py
```

**Limitado ao Firefox à principio**
