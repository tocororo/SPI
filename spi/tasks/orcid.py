import requests

ORCID_API = 'https://pub.orcid.org/v3.0/expanded-search/'


def get_orcid_list_by_org(org: str = '') -> str:
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
    params = {
        'q': 'affiliation-org-name:("Universidad de Pinar del Rio" OR "Universidad de Pinar del '
             'Río" OR "Hermanos Saiz Montes de Oca") OR email:*@upr.edu.cu'
        }
    response = requests.get(ORCID_API, headers=headers, params=params)
    return response.text
