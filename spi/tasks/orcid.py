import requests
import json

from spi.controllers import PersonsController
from spi.database import connect
from spi.tasks.ad import get_ldap_list_persons

ORCID_API = 'https://pub.orcid.org/v3.0/expanded-search/'


def get_orcid_list_by_assets_name(org: str = '') -> str:
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
        'q': '(given-names:Rafael) AND (family-name:Martinez Estevez)'
    }
    response = requests.get(ORCID_API, headers=headers, params=params)
    # return response.text
    return json.loads(response.text)['expanded-result']


def get_orcid_list_by_ad_name(given_names: str = '', family_name: str = '') -> str:
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    params = {
        'q': '(given-names:Rafael) AND (family-name:Martinez Estevez)'
    }
    response = requests.get(ORCID_API, headers=headers, params=params)
    return json.loads(response.text)['expanded-result']


def get_orcid_list() -> str:
    orcid_list_by_assets_name = get_orcid_list_by_assets_name()
    orcid_list_by_ad_name = get_orcid_list_by_ad_name()


async def get_orcid():
    # persons = await PersonsController.retrieve()
    persons = await PersonsController.retrieve_person("10642          ")
    for person in [persons]:
        fullNameSPI = person['name'] + ' ' + person['lastName']
        orcid_list = get_orcid_list()
        print(fullNameSPI)
        for item in orcid_list:
            fullNameORCID = item['given-names'] + ' ' + item['family-names']
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
    asyncio.run(get_orcid())
