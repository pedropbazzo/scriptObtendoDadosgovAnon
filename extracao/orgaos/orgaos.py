# -*- coding: utf-8 -*-

import ckanclient
from exceptions import IOError

try:
    with open("../../../api.key","r") as f:
        api_key=f.readline().strip()
except IOError:
    api_key = ""

ckan = ckanclient.CkanClient(base_location='http://dados.gov.br/api', api_key=api_key)

package_list = ckan.package_register_get()
authors = (ckan.package_entity_get(package)['author'] for package in package_list)
for author in authors:
    print author.encode('utf-8') if author else u""
