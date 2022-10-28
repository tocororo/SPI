import json
import os
from pathlib import Path
import string
import pandas as pd

from spi.controllers import PersonsController, PidsController
from spi.database import connect

ASSETS_JSONLD_TMP = str(os.getenv("ASSETS_JSONLD_TMP"))
ASSETS_CSV_TMP = str(os.getenv("ASSETS_CSV_TMP"))
ASSETS_JSON_TMP = str(os.getenv("ASSETS_JSON_TMP"))

def csv_to_json(csv_file_path, json_file_path):
    #create a dictionary
    data_dict = {}
 
    #Step 2
    #open a csv file handler
    with open(csv_file_path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
 
        #convert each row into a dictionary
        #and add the converted data to the data_variable
 
        for rows in csv_reader:
 
            #assuming a column named 'No'
            #to be the primary key
            key = rows['Serial Number']
            data_dict[key] = rows
 
    #open a json file handler and use json.dumps
    #method to dump the data
    #Step 3
    with open(json_file_path, 'w', encoding = 'utf-8') as json_file_handler:
        #Step 4
        json_file_handler.write(json.dumps(data_dict, indent = 4))


# get list of persons from assets
def get_assets_list_persons():
    file = open(ASSETS_JSONLD_TMP, "r")
    persons_assets = json.loads(file.read())
    persons_assets = persons_assets["hydra:member"]
    persons_assets_fixed = []

    for assets in persons_assets:
        _identifiers = [
            # {'idtype': 'userName', 'idvalue': assets['idUser']},
            {'idtype': 'idExpediente', 'idvalue': assets['idExpediente'].replace(" ", "")},
            {'idtype': 'noCi', 'idvalue': assets['noCi'].replace(" ", "")}
        ]
        name = string.capwords(assets['nombre'])
        lastName = string.capwords(assets['apellido1']) + ' ' + string.capwords(assets['apellido2'])

        # normalize person from assets to persons model
        fixed_person = dict(
            identifiers=_identifiers,
            name=name,
            lastName=lastName,
            gender=assets['sexo'].replace(" ", ""),
            country=assets['pais'].replace(" ", ""),
            email='',
            aliases=[name + ' ' + lastName]
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
        can_insert = True
        identifiers = person['identifiers']

        for identifier in identifiers:
            pids = await PidsController.retrieve_one({"idvalue": identifier['idvalue']})
            if pids:
                print("UPDATE ONE")
                print("=========================")
                await PersonsController.update_person(pids['person_id'], person)
                can_insert = False
                break
        if can_insert:
            print("INSERT ONE")
            print("=========================")
            await PersonsController.insert(person)


if __name__ == '__main__':
    import asyncio

    asyncio.run(connect())
    # asyncio.run(save_assets_list_persons())
    
    csv_to_json(ASSETS_CSV_TMP, ASSETS_JSON_TMP)
