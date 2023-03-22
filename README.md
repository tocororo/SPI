# System of Persons Identification (SPI)

[![MongoDB](https://img.shields.io/badge/MongoDB-%2014-gren.svg?style=flat)](https://www.mongodb.com/)
[![Python](https://img.shields.io/badge/Python-%20>=%203.8-blue.svg?style=flat)](https://www.python.org/downloads/)
[![FasApi](https://img.shields.io/badge/FasApi-%20>=%200.79.1-teal.svg?style=flat)](https://fastapi.tiangolo.com/)

>**This project it's part of a process, to create a database that contains the information of every person afiliated to some cuban universities and then to be used or to be consulted by the app [personas](https://personas.sceiba.cu/)**.

## Steps to create a collection of persons

1. First, you need to have a MongoDB server running.
2. Create a file ***.env***  with the content of ***template.env***.
3. Modify the ***database configs*** in ***.env*** file if needed.
4. Take the content of ***institution_config_template.json*** file and create an ***institution_config.json*** file with that content and edit it with the info of youUsingr institution (assets).
5. Open you terminal ``pip install -e .``
6. The script ***assets*** needs to have a directory data with a ***file_name.json*** or ***file_name.csv***. This paths needs to be modified in ***.env*** file (if names or directories don't match).
7. In order to obtain a list of persons from your assets directory ***file_name.json or file_name.csv***, excecute from the spi root folder ``python spi/tasks/assets.py``.
   * If you need to update the ***email*** for every person in that list whith the ldap protocol of your institution, first update the ***ldap configs*** in your ***.env*** file and then excecute from the spi root folder ``python spi/tasks/ad.py``.
   * If you need to update the ***orcid*** for every person in the assets list drectly from ***ORCID API***, excecute from the spi root folder ``python spi/tasks/orcid.py``.
8. In order to export the persons collection in a JSON format write in a terminal 

   * For local: ``mongoexport --db="database_name" --collection=persons --out=data/persons.json``, this command will export the collection to the mongodb ***data*** folder.
   * For remote: ``mongoexport uri="database_uri" --db="database_name" --collection=persons --out=data/persons.json``, this command will export the collection to the mongodb ***data*** folder.

### Want to use the API ? (This feature use the database generated by the above steps)

1. In order to run the server open your terminal and excecute from the spi root folder ``python main.py``. The server will run in the ***IP and PORT*** provided in the .env file ***(API_HOST and API_PORT)***.
2. Routes available:
   * ``/persons`` will provide a list of all the persons
   * ``/person?idExpediente="..."`` will provide a person that match with that ***idExpediente***.
   * ``/person_search?id="..."`` will provide a person with a field ***search_results***, this field contains a list of persons that orcid consider can be a scpecific person.
