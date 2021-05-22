## Objetivo

Cadastrar, no conjunto de dados [filiados-partidos-politicos](http://dados.gov.br/dataset/filiados-partidos-politicos)
os recursos que apontam para as URLs dos arquivos fornecidos pelo TSE.
Os arquivos são separados por partido e por estado.

## Utilização

1. Colocar no diretorio a três níveis acima o arquivo
   `../../../api.key` contendo a sua chave da api do CKAN.
2. Executar o script

  python cadastra-filiados-partidos.py

## Dependências

  ckanclient
