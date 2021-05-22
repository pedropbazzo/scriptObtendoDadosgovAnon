from collections import namedtuple
import codecs
import re
import ckanclient
from exceptions import IOError

try:
    with open("../../../api.key","r") as f:
        api_key=f.readline().strip()
except IOError:
    api_key = ""

ckan = ckanclient.CkanClient(base_location='http://dados.gov.br/api', api_key=api_key)

Subject = namedtuple('Subject', ['label', 'url'])
Package = namedtuple('Package', ['title', 'url'])

vcge_re = re.compile(r"([^[]+)\s*\[(http://[^[\]]+)\]\s?[,;]?\s?")
get_subject = lambda subject_str: (Subject(title, url) for title, url in vcge_re.findall(subject_str))

package_list = ckan.package_register_get()
subjects_packages = (
    (
        Package(ckan.package_entity_get(package)['title'], ckan.package_entity_get(package)['ckan_url']),
        get_subject(ckan.package_entity_get(package)['extras'].get('VCGE',''))
    ) for package in package_list)
subject_list = {}

for package, subjects in subjects_packages:
    if subjects:
        for subject in subjects:
            packages = subject_list.setdefault(subject.url, [subject, set()])[1]
            packages.add(package)

with codecs.open("assuntos.html", "w", encoding="utf-8") as f:
    f.write(u"<!DOCTYPE html>\n<html>\n<head><meta http-equiv='Content-Type' content='text/html; charset=utf-8'></head>\n<body>")
    f.write(u"<ul>")
    for subject_url in sorted(subject_list.keys()):
        subject, packages = subject_list[subject_url]
        f.write(u"<li><a href='%s'>%s</a> (%d) <ul>" % (subject.url, subject.label, len(subject_list[subject_url][1])))
        for package in sorted(packages):
            f.write(u"<li><a href='%s'>%s</a></li>" % (package.url, package.title))
        f.write(u"</ul></li>")
    f.write("</ul>\n")
    f.write("</body>\n</html>\n")
    
