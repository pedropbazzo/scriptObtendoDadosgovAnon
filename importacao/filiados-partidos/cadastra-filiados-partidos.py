# -*- coding: utf-8 -*-

import re
import ckanclient
from exceptions import IOError

try:
    with open("../../../api.key","r") as f:
        api_key=f.readline().strip()
except IOError:
    raise Exception(u"Uma chave de API no arquivo api.key é necessária para a operação.")

option_extract = re.compile(r'value="(\w+)"[^>]*>([\w ]+)<', re.UNICODE)
partidos_html = u'''<option value="dem" selected="selected">DEM</option>
				<option value="novo">NOVO</option>
				<option value="pen">PEN</option>
				<option value="pc_do_b">PC do B</option>
				<option value="pcb">PCB</option>
				<option value="pco">PCO</option>
				<option value="pdt">PDT</option>
				<option value="phs">PHS</option>
				<option value="pmdb">PMDB</option>
				<option value="pmn">PMN</option>
				<option value="pp">PP</option>
				<option value="ppl">PPL</option>
				<option value="pps">PPS</option>
				<option value="pr">PR</option>
				<option value="prb">PRB</option>
				<option value="pros">PROS</option>
				<option value="prp">PRP</option>
				<option value="prtb">PRTB</option>
				<option value="psb">PSB</option>
				<option value="psc">PSC</option>
				<option value="psd">PSD</option>
				<option value="psdb">PSDB</option>
				<option value="psdc">PSDC</option>
				<option value="psl">PSL</option>
				<option value="psol">PSOL</option>
				<option value="pstu">PSTU</option>
				<option value="pt">PT</option>
				<option value="pt_do_b">PT do B</option>
				<option value="ptb">PTB</option>
				<option value="ptc">PTC</option>
				<option value="ptn">PTN</option>
				<option value="pv">PV</option>
				<option value="rede">REDE</option>
				<option value="sd">SD</option>
				'''
partidos = dict(option_extract.findall(partidos_html))

estados_html = u'''<select id="uf"><option value="ac" selected="selected">do Acre</option><option value="al">de Alagoas</option><option value="am">do Amazonas</option><option value="ap">do Amapá</option><option value="ba">da Bahia</option><option value="ce">do Ceará</option><option value="df">do Distrito Federal</option><option value="es">do Espírito Santo</option><option value="go">de Goiás</option><option value="ma">do Maranhão</option><option value="mg">de Minas Gerais</option><option value="ms">do Mato Grosso do Sul</option><option value="mt">do Mato Grosso</option><option value="pa">do Pará</option><option value="pb">da Paraíba</option><option value="pe">de Pernambuco</option><option value="pi">do Piauí</option><option value="pr">do Paraná</option><option value="rj">do Rio de Janeiro</option><option value="rn">do Rio Grande do Norte</option><option value="ro">de Rondônia</option><option value="rr">de Roraima</option><option value="rs">do Rio Grande do Sul</option><option value="sc">de Santa Catarina</option><option value="se">de Sergipe</option><option value="sp">de São Paulo</option><option value="to">do Tocantins</option></select>'''
estados = dict(option_extract.findall(estados_html))

ckan = ckanclient.CkanClient(base_location='http://dados.gov.br/api', api_key=api_key)

dataset = ckan.package_entity_get('filiados-partidos-politicos')

# mapeia os recursos pela url
resources = {}
for resource in dataset['resources']:
    resources[resource[u'url']] = resource

# troca 'de' por 'em'
subst = {u'de': u'em', u'do': u'no', u'da': u'na'}
de_por_em = lambda frase: u" ".join((subst.get(part, part) for part in frase.split(u" ",1)))
position = 0
for estado in sorted(estados.keys()):
    print u"Verificando recursos referentes ao estado: %s" % estado.upper()
    for partido in sorted(partidos.keys()):
        metadados = {
            u'mimetype': u'application/zip+text/csv', 
            u'description': u'''Arquivo ZIP, contendo a relação dos eleitores filiados ao %s no estado %s, em formato csv, com campos separados por ponto-e-vírgula.

Colunas:

* Data da extração das informações do banco de dados;
* Hora da extração das informações do banco de dados;
* Número da inscrição eleitoral;
* Nome do filiado;
* Sigla do partido político;
* Nome do partido político;
* Unidade da federação;
* Código do município;
* Nome do município;
* Zona eleitoral;
* Seção eleitoral;
* Data da filiação;
* Situação do registro de filiação;
* Tipo do registro de filiação;
* Data do processamento do registro de filiação;
* Data da desfiliação;
* Data do cancelamento do registro de filiação;
* Data da regularização do registro de filiação;
* Motivo do cancelamento do registro de filiação.
''' % (partidos[partido], estados[estado]),
            u'url': u'http://agencia.tse.jus.br/estatistica/sead/eleitorado/filiados/uf/filiados_%s_%s.zip' % (partido, estado),
            u'format': u'zip+csv',
            u'name': u'Filiados ao %s %s' % (partidos[partido], de_por_em(estados[estado])),
            u'position': position,
            u'resource_type': u'file',
        }
        url = metadados[u'url']
        # se o recurso existe, atualiza
        if url in resources.keys():
            resources[url].update(metadados)
        else: # senao, acrescenta
            print u"Adicionando recurso '%s'..." % url
            ckan.add_package_resource(dataset['name'], url, **metadados)
        position = position + 1

# traz o dataset atualizado com os recursos acrescentados
#dataset_novo = ckan.package_entity_get('filiados-partidos-politicos')
# aplica as modificacoes realizadas em recursos
#for i, resource in enumerate(dataset_novo['resources']):
#    url = resource[u'url']
#    if url in resources.keys():
#        dataset_novo['resources'][i].update(resources[url])
# grava as alteracoes
#print u"Consolidando as alterações..."
#ckan.package_entity_put(dataset)


