import requests
import json
from Controllers.personController import PersonsController

ORCID_API = 'https://pub.orcid.org/v3.0/expanded-search/'

class CollectPersonsController():

    @staticmethod
    def get_orcid_list_by_org(org: str = '') -> str:
        """
            Return a list of persons according to the organization
            @params:
                `org`: is a `str` with the alias of the organization with the format: `alias+operator(AND,OR)+alias`
                       example:  "Universidad de Pinar del Rio"+OR+UPR
        """
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'Accept': 'application/json'
        }
        params = {
            'q': 'affiliation-org-name:("Universidad de Pinar del Rio" OR "Universidad de Pinar del Río" OR "Hermanos Saiz Montes de Oca") OR email:*@upr.edu.cu'
        }
        response = requests.get(ORCID_API, headers=headers, params=params)
        return response.text

    @staticmethod
    async def get_assets_list_persons():
        file = open("/home/alejandro/PersonalData/CRAI/sp-Institution/apiassets.jsonld", "r")
        persons_assets = json.loads(file.read())
        persons_assets = [persons_assets["hydra:member"][0]]
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
            return await PersonsController.insert(fixed_person)


if __name__ == '__main__':
    # print(get_orcid_list_by_org())
    f = open("/home/alejandro/PersonalData/CRAI/sp-Institution/apiassets.jsonld", "r")
    data = f.read()
    persons = json.loads(data)
    print(persons["hydra:member"])
