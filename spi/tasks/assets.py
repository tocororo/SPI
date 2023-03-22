import json, csv, os, string, array

from spi.controllers import PersonsController, PidsController
from spi.database import connect
from spi.logger_base import create_log
from spi.routes import make_request
import pandas as pd

ASSETS_JSONLD_PATH = os.getenv("ASSETS_JSONLD_PATH")
ASSETS_CSV_PATH = os.getenv("ASSETS_CSV_PATH")

def get_assets_from_csv():
    data_dict = []
    if os.path.exists(ASSETS_CSV_PATH) and os.path.isfile(ASSETS_CSV_PATH):
        csv_file = pd.DataFrame(pd.read_csv(ASSETS_CSV_PATH, sep = ",|;", header = 0, index_col = False, engine = "python"))
        csv_file.to_json("data/csv_temp.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)
        
        f = open("data/csv_temp.json")
        data_dict = json.load(f)
        f.close()
        os.remove("data/csv_temp.json")
        return data_dict
    else:
        return data_dict
    
def get_from_api_assets(config) -> list:
    """
        Return a list of persons from assets api
        @params:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    
    params = {}
    for param in config[params]:
        params[param["key"]]: param["value"]
    
    response = make_request(f'{config.url}', headers=headers, params=params)
    if response.status_code == 200 and len(response.json().keys()) > 0:
        print('GET ASSETES FROM API')
        print("=========================")
        return {"status": response.status_code, "result": response.json()['expanded-result']}
    return {"status": response.status_code, "result": []}


# get list of persons from assets
def get_assets_list_persons():
    file = open(ASSETS_JSONLD_PATH, "r")
    assets_from_jsonld = json.loads(file.read())    
    assets_from_csv = get_assets_from_csv()
    
    institution_config_file = open('institution_config.json', "r")
    institution_config = json.loads(institution_config_file.read())   
    
    persons_assets = []
    
    if (len(assets_from_csv) > 0):
        persons_assets = assets_from_csv
    elif os.path.exists(ASSETS_JSONLD_PATH) and os.path.isfile(ASSETS_JSONLD_PATH):
        create_log('assets').info('CSV file for assetss was not found, proceeding to use jsonld')
        persons_assets = assets_from_jsonld["hydra:member"]
    else:
        api_res = get_from_api_assets(institution_config)
        if api_res["status"] == 200:
            persons_assets = api_res["result"]
        else:
            create_log('assets').warning('Neither a CSV or JSONLD file for assets was found')
        
    keys = institution_config["keys"]
    persons_assets_fixed = []    

    for data in persons_assets:
        name = string.capwords(data[keys["nombre"]])
        lastName =  data[keys.lastName] if "lastName" in data else string.capwords(data[keys["apellido1"]]) + ' ' + string.capwords(data[keys["apellido2"]])
        _identifiers = []
        for id in keys["identifiers"]:
            _identifiers.append({'idtype': id, 'idvalue': str(data[id]).replace(" ", "")})

        # normalize person from data to persons model
        fixed_person = dict(
            identifiers=_identifiers,
            name=name,
            lastName=lastName,
            gender=data[keys["sexo"]].replace(" ", "") if data[keys["sexo"]] else "",
            country=data[keys["pais"]].replace(" ", "") if data[keys["pais"]] else "",
            institutional_email=data[keys["institutional_email"]] if data[keys["institutional_email"]] else "",
            emails=data[keys["emails"]] if data[keys["emails"]] else "",
            aliases=[name + ' ' + lastName]
            # active = ele.activo,
            # date_start = ele.start,
            # date_end = ele.end,
        )
        print(fixed_person)
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
                await PersonsController.update_person(pids['person_id'], {"$set": person})
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