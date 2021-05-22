Script para gerar a planilha solicitada pelo TCU na auditoria de 2016.

# Instalação

1. Clonar o repositório

`git clone https://github.com/dadosgovbr/scripts-dadosgovbr.git`

2. Para usar os scripts em Python, criar e ativar um [ambiente virtual](https://virtualenv.readthedocs.org/en/latest/)

```
cd scripts-dadosgovbr
virtualenv --no-site-packages pyenv
source pyenv/bin/activate
```

3. Coloque sua chave da API no arquivo api.key (opcional).

4. Instalar as dependências do script que deseja usar. Entre no diretório `scripts/extracao/planilha-auditoria-tcu-2016` e use o comando

`pip install -r requirements.txt`

5. Para executar o script, use

`python gera-planilha-tcu.py`

Será gerado um arquivo na forma `dados/planilha-dadosgovbr-AAAA-MM-DD.csv`.

