import urllib.parse
from typing import List

from spi.controllers import PersonsController
from spi.database import connect
from spi.models import PersonSchema

from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, Namespace

from spi.pids import get_pid_value
from spi.tasks.assets import get_assets_list_persons


def fix(s):
    i = s.rindex('/')
    return s[:i]+urllib.parse.quote(s[i:])


async def export_graph(persons: List[PersonSchema]):
    g = Graph()
    vcard = Namespace("http://www.w3.org/2006/vcard/ns#")
    vivo = Namespace("http://vivoweb.org/ontology/core#")
    g.bind("foaf", FOAF)
    g.bind("vcard", vcard)
    g.bind("vivo", vivo)
    for person in persons:

        p = URIRef(get_pid_value(person, 'idExpediente'))
        g.add((p, RDF.type, FOAF.Person))
        g.add((p, RDF.type, vivo.term('FacultyMember')))
        g.add((p, vivo.term('uid'), Literal(person['_id'])))
        g.add((p, vivo.term('uri'), URIRef(get_pid_value(person, 'idExpediente'))))
        g.add((p, vcard.term('familyName'), Literal("{0}".format(person['name']))))
        g.add((p, vcard.term('middleName'), Literal("{0}".format(person['lastName']))))
        g.add((p, vcard.term('nickName'), Literal("{0}".format(person['name']))))
        g.add((p, vcard.term('title'), Literal("profesor")))

        # TODO: use PersonSchema not dict to access attributes
        g.add((p, FOAF.name, Literal("{0} {1}".format(person['name'], person['lastName']))))
    g.bind("foaf", FOAF)
    print(g.serialize(format='xml'))


async def export_all():
    persons = await PersonsController.retrieve()
    await export_graph(persons)


if __name__ == '__main__':
    import asyncio

    asyncio.run(connect())

    asyncio.run(export_all())
