import os
import requests
import json
import time
from random import randint

from spi.controllers import PersonsController, OrcidController
from spi.database import connect
from spi.controllers import OrcidController

ORCID_API = str(os.getenv("ORCID_API"))
ASSETS_JSON_TMP = str(os.getenv("ASSETS_JSON_TMP"))


def get_orcid_list_by_name_and_last_name(given_names: str = '', family_name: str = '') -> str:
    """
        Return a list of persons according to the organization
        @params:
            `given-names`: is a `str` with the first name of the person
            `family-names`: is a `str` with the lastt name of the person
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
    response = requests.get(f'{ORCID_API}/expanded-search/', headers=headers, params=params)
    # return response.text
    if response.text and 'expanded-result' in json.loads(response.text).keys():
        print('GET ORCID LIST BY NAME AND LAST NAME')
        print("=========================")
        return json.loads(response.text)['expanded-result']
    return None

def get_orcid_list_by_full_name(full_name: str = '') -> str:
    """
        Return a list of persons according to the organization
        @params:
            `given-and-family-names`: is a `str` with the first name of the person
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    params = {
        'q': f'(given-and-family-names:{full_name.lower()})'
    }
    response = requests.get(f'{ORCID_API}/expanded-search/', headers=headers, params=params)
    # return response.text
    if response.text and 'expanded-result' in json.loads(response.text).keys():
        print('GET ORCID LIST BY FULL NAME')
        print("=========================")
        return json.loads(response.text)['expanded-result']
    return None

def get_email_by_orcid(orcid: str = '') -> str:
    """
        Return info of email according to an orcid
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    response = requests.get(f'{ORCID_API}/{orcid}/email/', headers=headers)
    # return response.text
    if response.text and 'email' in json.loads(response.text).keys():
        print('GET ORCID PERSON BY EMAIL')
        print("=========================")
        emails = []
        for email in json.loads(response.text)['email']:
            emails.append(email['email'])
        return emails
    return []


# if exist update a person with the orcid_id from orcid api
async def update_orcid_by_person(person_id, orcid_list):
    if orcid_list:
        for orcid_item in orcid_list:
            if orcid_item['given-names']:
                given_names = orcid_item['given-names']
            else:
                given_names = ''

            if orcid_item['family-names']:
                family_names = orcid_item['family-names']
            else:
                family_names = ''

            full_name = given_names + ' ' + family_names

            # if orcid_item and 'given-names' in orcid_item.keys() and 'family-names' in orcid_item.keys():
            # given_names = orcid_item['given-names'] if orcid_item['given-names'] else ''
            # family_names = orcid_item['family-names'] if orcid_item['family-names'] else ''

            # orcid_full_name = given_names + ' ' + family_names
            # ldap_displayName = entry['displayName'][0].decode("utf-8")

            # if orcid_item['orcid-id'] not in orcid_list_cleaned and orcid_full_name == ldap_displayName:

            existent_orcid_item = await OrcidController.retrieve_one({'orcid_id': orcid_item['orcid-id']})
            if not existent_orcid_item:
                print('INSERT ORCID PERSON')
                print("=========================")
                orcid_item.update({
                    "full_name": full_name,
                    "person_id": person_id
                })
                await OrcidController.insert(orcid_item)


async def get_orcid_list():
    persons = await PersonsController.retrieve()
    for person in persons:

        # wait a time before execute query for assets orcid
        sleep_time = randint(3, 9)
        print('sleep {0} seconds'.format(sleep_time))
        time.sleep(sleep_time)

        ldap_name = person['ldap_name']
        ldap_lastName = person['ldap_lastName']

        await update_orcid_by_person(
            person['_id'],
            get_orcid_list_by_name_and_last_name(ldap_name, ldap_lastName)
        )

        for alias in person['aliases']:
            orcid_list = get_orcid_list_by_full_name(alias)
            await update_orcid_by_person(person['_id'], orcid_list)

        orcid_list = await OrcidController.retrieve({"person_id": person['_id']})

        for orcid_item in orcid_list:
            if person['email'] in get_email_by_orcid(orcid_item['orcid_id']):
                print('UPDATE ORCID_ID BY PERSON EMAIL')
                print("=========================")
                await PersonsController.update_person(person['_id'], dict(orcid=orcid_item['orcid_id']))
            # elif orcid_item['full_name'] in persons['aliases']:



    # f_ad = open("demofile4.json", "a")
    # f_ad.write(str(orcid_list_cleaned))
    # f_ad.close()


async def get_orcid():
    # persons = await PersonsController.retrieve()
    persons = await PersonsController.retrieve_person({"idvalue": "10642"})
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
