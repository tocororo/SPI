import json

from spi.controllers import PersonsController
from spi.database import connect
from spi.tasks import ad

ASSETS_JSON_TMP = "../../data/apiassets.jsonld"


async def get_assets_list_persons():
    email = ''
    ldap_persons = ad.get_ldap_list_persons()
    file = open(ASSETS_JSON_TMP, "r")
    persons_assets = json.loads(file.read())
    persons_assets = persons_assets["hydra:member"]
    for assets in persons_assets:
        _identifiers = [
            # {'idtype': 'userName', 'idvalue': assets['idUser']},
            {'idtype': 'idExpediente', 'idvalue': assets['idExpediente']},
            {'idtype': 'noCi', 'idvalue': assets['noCi']}
        ]

        for dn, entry in ldap_persons:
            # print('Processing', repr(entry))
            # f = open("demofile3.json", "a")
            # f.write(str(entry))
            # f.close()
            if entry and 'mail' in entry.keys() and 'employeeID' in entry.keys():
                employeeID = str(entry['employeeID']).replace("[b'", '').replace("']", '')
                mail = str(entry['mail']).replace("[b'", '').replace("']", '')
                if employeeID == assets['noCi'].replace(" ", ""):
                    email=mail

        fixed_person = dict(
            identifiers=_identifiers,
            name=assets['nombre'],
            lastName=assets['apellido1'] + ' ' + assets['apellido2'],
            gender=assets['sexo'],
            country=assets['pais'],
            email=email
            # active = ele.activo,
            # date_start = ele.start,
            # date_end = ele.end,
        )


        new_results = []

        print(new_results)

        await PersonsController.insert(fixed_person)


if __name__ == '__main__':
    import asyncio

    asyncio.run(connect())
    asyncio.run(get_assets_list_persons())
