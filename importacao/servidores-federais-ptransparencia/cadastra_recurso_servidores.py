# -*- coding: utf-8 -*-

import requests

class LinkCSV(object):
    resource_url_template = u"http://"
    ckan_url = u"http://demo.ckan.org"
    package_id = u""
    apikey = u""
    
    @property
    def url(self):
        return self.resource_url_template % \
            (self.ano, self.mes, self.tipo)

    name = u""
    description = u""
    format = u""
    mimetype = u""
    mimetype_inner = u""
    size = None

    def register(self):
        u"Register resource into CKAN"
        import ckanapi
        ckansite = ckanapi.RemoteCKAN(self.ckan_url, apikey=self.apikey)
        
        # resource url responds?
        resource = requests.head(self.url)
        self.size = int(resource.headers["content-length"])
        
        # resource exists?
        resources = ckansite.action.resource_search(query=u"url:%s" % self.url)
        if resources[u"count"] == 0:
            ckansite.action.resource_create(
                package_id = self.package_id,
                url = self.url,
                name = self.name,
                description = self.description,
                format = self.format,
                mimetype = self.mimetype,
                size = self.size,
            )

class LinkServidores(LinkCSV):
    resource_url_template = u"http://arquivos.portaldatransparencia.gov.br/downloads.asp?a=%04d&m=%02d&d=%s&consulta=Servidores"
    ckan_url = u"http://dados.gov.br"
    package_id = u"servidores-do-executivo-federal"
    apikey = u""
    mes_extenso = {1: u"janeiro", 2: u"fevereiro", 3: u"março", 4: u"abril", 5: u"maio", 6: u"junho",
        7: u"julho", 8: u"agosto", 9: u"setembro", 10: u"outubro", 11: u"novembro", 12: u"dezembro"}
    
    def __init__(self, ano, mes, tipo=u"C", api_key=u""):
        self.mes = mes
        self.ano = ano
        self.tipo = tipo
        self.apikey = api_key
    
    @property    
    def name(self):
        palavra = u"civis"
        if self.tipo == u"M":
            palavra = u"militares"
        return u"Servidores %s do executivo federal em %d/%d" % (palavra, self.mes, self.ano)
    
    @property
    def description(self):
        palavra = u"civis"
        if self.tipo == u"M":
            palavra = u"militares"
        return u"Informações sobre os servidores %s do executivo federal, no mês de %s de %d" % (palavra, self.mes_extenso[self.mes], self.ano)

    format = u"zip+csv"
    mimetype = u"application/zip"
    mimetype_inner = u"text/csv"


if __name__ == "__main__":
    from sys import argv
    from exceptions import IOError
    try:
        with open("../../../api.key","r") as f:
            api_key=f.readline().strip()
    except IOError:
        raise Exception(u"Uma chave de API no arquivo api.key é necessária para a operação.")
    link = LinkServidores(int(argv[1]), int(argv[2]), argv[3], api_key)
    link.register()

