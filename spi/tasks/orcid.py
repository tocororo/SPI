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


def get_orcid_list_by_affiliation_and_domain(orcid: str = '') -> str:
    """
        Return a list of persons according to the  current-institution-affiliation-name and the email domain
        @params:
            `current-institution-affiliation-name`: is a `str` with the current institution of the person
            `email`: is a `str` with the email domain
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    params = {
        'q': '(current-institution-affiliation-name:"Universidad de Pinar del Río") OR (email:*@upr.edu.cu)'
    }
    response = requests.get(f'{ORCID_API}/{orcid}/email/', headers=headers, params=params)
    # return response.text
    if response.text and 'email' in json.loads(response.text).keys():
        print('GET ORCID List BY INSTITUTION AND DOMAIN')
        print("=========================")
        emails = []
        for email in json.loads(response.text)['email']:
            emails.append(email['email'])
        return emails
    return []


def normalize_full_name_orcid(orcid_item) -> str:
    if orcid_item['given-names']:
        given_names = orcid_item['given-names']
    else:
        given_names = ''

    if orcid_item['family-names']:
        family_names = orcid_item['family-names']
    else:
        family_names = ''
    return given_names + ' ' + family_names


# if exist update a person with the orcid_id from orcid api
async def save_orcid_search_by_person(person_id, orcid_list):
    if orcid_list:
        for orcid_item in orcid_list:
            full_name = normalize_full_name_orcid(orcid_item)

            # if orcid_item and 'given-names' in orcid_item.keys() and 'family-names' in orcid_item.keys():
            # given_names = orcid_item['given-names'] if orcid_item['given-names'] else ''
            # family_names = orcid_item['family-names'] if orcid_item['family-names'] else ''

            # orcid_full_name = given_names + ' ' + family_names
            # ldap_displayName = entry['displayName'][0].decode("utf-8")

            # if orcid_item['orcid-id'] not in orcid_list_cleaned and orcid_full_name == ldap_displayName:

            existent_orcid_item = await OrcidController.retrieve_one({'orcid_id': orcid_item['orcid-id']})
            if len(existent_orcid_item) > 0 and existent_orcid_item[0]:
                item = existent_orcid_item[0]
                id = item['_id']
                print('UPDATE ORCID -> PERSON_ID')
                print("=========================")
                item.update({
                    "person_id": person_id
                })
                del item['_id']
                await OrcidController.update(id, item)
            else:
                print('INSERT ORCID PERSON')
                print("=========================")
                orcid_item.update({
                    "full_name": full_name,
                    "person_id": person_id
                })
                await OrcidController.insert(orcid_item)


async def save_orcid_search_by_affiliation_and_domain():
    orcid_list_by_affiliation_and_domain = get_orcid_list_by_affiliation_and_domain()
    for orcid_item in orcid_list_by_affiliation_and_domain:
        full_name = normalize_full_name_orcid(orcid_item)

        print('INSERT ORCID PERSON')
        print("=========================")
        new_orcid_item = {
            "orcid_id": orcid_item['orcid-id'],
            "given_names": orcid_item['given-names'],
            "family_names": orcid_item['family-names'],
            "full_name": full_name,
        }
        await OrcidController.insert(new_orcid_item)


async def get_orcid_list():
    persons = await PersonsController.retrieve()
    # save_orcid_search_by_affiliation_and_domain()

    for person in persons:
        for alias in person['aliases']:
            # wait a time before execute query for get_orcid_list_by_full_name
            sleep_time = randint(3, 5)
            print('sleep {0} seconds'.format(sleep_time))
            time.sleep(sleep_time)

            first_name = person['name']
            split_at = len(first_name) + 1
            left, right = alias[:split_at], alias[split_at:]

            await save_orcid_search_by_person(
                person['_id'],
                get_orcid_list_by_name_and_last_name(left, right),
            )
        orcid_list = await OrcidController.retrieve_one({"person_id": person['_id']})

        for orcid_item in orcid_list:

            # wait a time before execute query for email orcid
            sleep_time = randint(3, 5)
            print('sleep {0} seconds'.format(sleep_time))
            time.sleep(sleep_time)

            if person['email'] in get_email_by_orcid(orcid_item['orcid_id']) or orcid_item['full_name'] in person['aliases']:
                await PersonsController.update_person(person['_id'], dict(orcid=orcid_item['orcid_id']))
                print('UPDATE ORCID_ID BY PERSON EMAIL')
                print("=========================")
                break


if __name__ == '__main__':
    # print(get_orcid_list())
    import asyncio

    asyncio.run(connect())
    # asyncio.run(get_orcid())
    asyncio.run(get_orcid_list())
