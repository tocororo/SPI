import json
import os

from spi.controllers import PersonsController
from spi.database import connect

ASSETS_JSON_TMP = str(os.getenv("ASSETS_JSON_TMP"))


# get list of persons from assets
def get_assets_list_persons():
    file = open(ASSETS_JSON_TMP, "r")
    persons_assets = json.loads(file.read())
    persons_assets = persons_assets["hydra:member"]
    persons_assets_fixed = []

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
        persons_assets_fixed.append(fixed_person)
    return persons_assets_fixed


# insert normalized person to DB
async def save_assets_list_persons():
    assets_list_persons = get_assets_list_persons()
    for person in assets_list_persons:
        await PersonsController.insert(person)

if __name__ == '__main__':
    import asyncio

    asyncio.run(connect())
    asyncio.run(save_assets_list_persons())
