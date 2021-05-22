# -*- coding: utf-8 -*-

import csv
import datetime
import dateutil.parser
import ckanapi
from exceptions import IOError

try:
    with open("../../../api.key","r") as f:
        api_key=f.readline().strip()
except IOError:
    api_key = ""

ckan = ckanapi.RemoteCKAN('http://dados.gov.br', user_agent='planilha-auditoria-tcu-2016/1.0 (+http://github.com/dadosgovbr/scripts-dadosgovbr)', apikey=api_key)

dataset_ids = ckan.action.package_list()

# funcao envolucra para pular datasets sem leitura autorizada
# (ex.: privados, excluidos)
def le_dataset(dataset_id):
    try:
        return ckan.action.package_show(id=dataset_id)
    except ckanapi.errors.NotAuthorized:
        return {}

datasets = (dataset for dataset in
    (le_dataset(dataset_id) for dataset_id in dataset_ids)
        if dataset and dataset['state']==u'active' and not dataset['private'])

# csvwriter nao trata unicode, entao envolvemos em uma funcao lambda para encoding
def utf_8_encoder(unicode_csv_data):
    return [item.encode('utf-8') if item else '' for item in unicode_csv_data]

# converte timestamp em data
def converte_em_data(timestamp):
    if timestamp:
        return dateutil.parser.parse(timestamp).date().isoformat()
    else:
        return u''

nome_planilha = "dados/planilha-dadosgovbr-%s.csv" % (datetime.date.today().isoformat())
with open(nome_planilha, "w") as f:
    planilha = csv.writer(f)
    planilha.writerow(utf_8_encoder([
        u"nome do conjunto",
        u"data de catalogação",
        u"autor",
        u"fonte",
        u"mantenedor",
        u"tema",
    ]))
    for dataset in datasets:
        vcge = [kv[u'value'] for kv in dataset[u'extras'] if kv[u'key']==u"VCGE"]
        # se nao estiver vazio, use o primeiro elemento da tupla
        vcge = vcge[0] if vcge else ''
        planilha.writerow(utf_8_encoder([
            dataset.get(u'title', u''),
            converte_em_data(dataset.get(u'metadata_created', u'')),
            dataset.get(u'author', u''),
            dataset.get(u'url', u''),
            dataset.get(u'maintainer', u''),
            vcge,
        ]))

