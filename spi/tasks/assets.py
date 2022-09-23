import json

from spi.controllers import PersonsController
from spi.database import connect

ASSETS_JSON_TMP = "../../data/apiassets.jsonld"


# get list of persons from assets
async def get_assets_list_persons():
    file = open(ASSETS_JSON_TMP, "r")
    persons_assets = json.loads(file.read())
    persons_assets = persons_assets["hydra:member"]

    for assets in persons_assets:
        _identifiers = [
            # {'idtype': 'userName', 'idvalue': assets['idUser']},
            {'idtype': 'idExpediente', 'idvalue': assets['idExpediente'].replace(" ", "")},
            {'idtype': 'noCi', 'idvalue': assets['noCi'].replace(" ", "")}
        ]
        lastName = assets['apellido1'] + ' ' + assets['apellido2']

        # normalize person from assets to persons model
        fixed_person = dict(
            identifiers=_identifiers,
            name=assets['nombre'],
            lastName=lastName,
            gender=assets['sexo'].replace(" ", ""),
            country=assets['pais'].replace(" ", ""),
            email='',
            aliases=[assets['nombre'] + ' ' + lastName]
            # active = ele.activo,
            # date_start = ele.start,
            # date_end = ele.end,
        )

        # insert normalized person to DB
        await PersonsController.insert(fixed_person)


if __name__ == '__main__':
    import asyncio

    asyncio.run(connect())
    asyncio.run(get_assets_list_persons())
