import json, csv, os, string, array

from spi.controllers import PersonsController, PidsController
from spi.database import connect

ASSETS_JSONLD_PATH = str(os.getenv("ASSETS_JSONLD_PATH"))
ASSETS_CSV_PATH = str(os.getenv("ASSETS_CSV_PATH"))

def get_assets_from_csv():
    data_dict = {}
    dict_array_formated = []
    if os.path.exists(ASSETS_CSV_PATH) and os.path.isfile(ASSETS_CSV_PATH) :
        with open(ASSETS_CSV_PATH, encoding = 'utf-8') as csv_file_handler:
            csv_reader = csv.DictReader(csv_file_handler)
            #convert each row into a dictionary and add the converted data to the data_variable
    
            for rows in csv_reader:
                #assuming a column named 'No' to be the primary key
                key = rows["No"]
                data_dict[int(key) - 1] = rows
    
        dict_array = array.array('L', data_dict.keys())
        for i, key in enumerate(dict_array):
            dict_array_formated.append(data_dict[key])
        return dict_array_formated
    else:
        return dict_array_formated


# get list of persons from assets
def get_assets_list_persons():
    file = open(ASSETS_JSONLD_PATH, "r")
    persons_assets = json.loads(file.read())
    
    if (len(get_assets_from_csv) > 0):
        persons_assets = get_assets_from_csv()
    else:
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
    asyncio.run(save_assets_list_persons())
    # print(get_assets_from_csv())