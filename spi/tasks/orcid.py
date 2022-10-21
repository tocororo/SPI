import os
import requests
import json
import time
from random import randint

from spi.controllers import PersonsController
from spi.database import connect
from spi.tasks.ad import get_ldap_list_persons
from spi.controllers import OrcidController

ORCID_API = str(os.getenv("ORCID_API"))
ASSETS_JSON_TMP = str(os.getenv("ASSETS_JSON_TMP"))


def get_orcid_list_by_name(given_names: str = '', family_name: str = '') -> str:
    """
        Return a list of persons according to the organization
        @params:
            `org`: is a `str` with the alias of the organization with the format:
            `alias+operator(AND,OR)+alias`
                   example:  "Universidad de Pinar del Rio"+OR+UPR
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    # params = {
    #     'q': 'affiliation-org-name:("Universidad de Pinar del Rio" OR "Universidad de Pinar del '
    #          'Río" OR "Hermanos Saiz Montes de Oca") OR email:*@upr.edu.cu'
    #     }
    params = {
        'q': f'(given-names:{given_names.lower()}) AND (family-name:{family_name.lower()})'
    }
    response = requests.get(ORCID_API, headers=headers, params=params)
    # return response.text
    if response.text and 'expanded-result' in json.loads(response.text).keys():
        print('success')
        return json.loads(response.text)['expanded-result']
    return None


async def get_orcid_list():
    orcid_list_cleaned = []

    file = open(ASSETS_JSON_TMP, "r")
    persons_assets = json.loads(file.read())

    # ldap_list = get_ldap_list_persons()[0:5]
    # assets_list = persons_assets["hydra:member"][0:5]

    ldap_list = get_ldap_list_persons()
    assets_list = persons_assets["hydra:member"]

    for item in assets_list:
        name = item['nombre']
        lastName = item['apellido1'] + ' ' + item['apellido2']
        assets_full_name = name + ' ' + lastName

        # wait a time before execute query for assets orcid
        sleep_time = randint(3, 9)
        print('sleep {0} seconds'.format(sleep_time))
        time.sleep(sleep_time)
        orcid_assests_list = get_orcid_list_by_name(name, lastName)

        if orcid_assests_list:
            for orcid_item in orcid_assests_list:
                # if orcid_item and 'given-names' in orcid_item.keys() and 'family-names' in orcid_item.keys():
                #     given_names = orcid_item['given-names'] if orcid_item['given-names'] else ''
                #     family_names = orcid_item['family-names'] if orcid_item['family-names'] else ''
                #     orcid_full_name = given_names + ' ' + family_names

                    # if orcid_item['orcid-id'] not in orcid_list_cleaned and orcid_full_name.lower() == assets_full_name.lower():
                    if orcid_item['orcid-id'] not in orcid_list_cleaned:
                        orcid_list_cleaned.append(orcid_item['orcid-id'])
                        await OrcidController.insert(orcid_item)

    for dn, entry in ldap_list:
        if entry and 'sn' in entry.keys() and 'givenName' in entry.keys() and 'displayName' in entry.keys():
            given_names = entry['givenName'][0].decode("utf-8")
            family_name = entry['sn'][0].decode("utf-8")

            # wait a time before execute query for ldap orcid
            sleep_time = randint(3, 9)
            print('sleep {0} seconds'.format(sleep_time))
            time.sleep(sleep_time)
            orcid_ldap_list = get_orcid_list_by_name(given_names, family_name)

            if orcid_ldap_list:
                for orcid_item in orcid_ldap_list:
                    # if orcid_item and 'given-names' in orcid_item.keys() and 'family-names' in orcid_item.keys():
                        # given_names = orcid_item['given-names'] if orcid_item['given-names'] else ''
                        # family_names = orcid_item['family-names'] if orcid_item['family-names'] else ''

                        # orcid_full_name = given_names + ' ' + family_names
                        # ldap_displayName = entry['displayName'][0].decode("utf-8")

                        # if orcid_item['orcid-id'] not in orcid_list_cleaned and orcid_full_name == ldap_displayName:
                        if orcid_item['orcid-id'] not in orcid_list_cleaned:
                            orcid_list_cleaned.append(orcid_item['orcid-id'])
                            await OrcidController.insert(orcid_item)

    f_ad = open("demofile4.json", "a")
    f_ad.write(str(orcid_list_cleaned))
    f_ad.close()


async def get_orcid():
    # persons = await PersonsController.retrieve()
    persons = await PersonsController.retrieve_person("10642          ")
    for person in [persons]:
        fullNameSPI = person['name'] + ' ' + person['lastName']
        orcid_list = get_orcid_list()
        print(fullNameSPI)
        for item in orcid_list:
            fullNameORCID = item['given-names'] + ' ' + item['family-name']
            print(fullNameORCID)
            if fullNameSPI.lower() == fullNameORCID.lower():
                print(item)
            else:
                print("not equal")
        # print(orcid_list)


if __name__ == '__main__':
    # print(get_orcid_list())
    import asyncio

    asyncio.run(connect())
    # asyncio.run(get_orcid())
    asyncio.run(get_orcid_list())
