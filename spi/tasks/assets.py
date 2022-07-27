import json

from spi.controllers import PersonsController
from spi.database import connect

ASSETS_JSON_TMP = "data/apiassets.jsonld"


async def get_assets_list_persons():
    file = open(ASSETS_JSON_TMP, "r")
    persons_assets = json.loads(file.read())
    persons_assets = persons_assets["hydra:member"]
    for ele in persons_assets:
        _identifiers = [
            {'idtype': 'userName', 'idvalue': ele['idUser']},
            {'idtype': 'idExpediente', 'idvalue': ele['idExpediente']},
            {'idtype': 'noCi', 'idvalue': ele['noCi']}
        ]
        fixed_person = dict(
            identifiers=_identifiers,
            name=ele['nombre'],
            lastName=ele['apellido1'] + ' ' + ele['apellido2'],
            gender=ele['sexo'],
            country=ele['pais'],
            # email = ele.email,
            # active = ele.activo,
            # date_start = ele.start,
            # date_end = ele.end,
        )

        await PersonsController.insert(fixed_person)


if __name__ == '__main__':
    import asyncio

    asyncio.run(connect())
    asyncio.run(get_assets_list_persons())
