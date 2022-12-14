import os
import urllib

from spi.models import PersonSchema

SPI_DOMAIN = str(os.getenv("SPI_DOMAIN"))


# TODO: add here an enum with known pid types..


def internal_id_to_spi_uri(pid_type, pid_value):

    return "http://{0}/{1}/{2}".format(SPI_DOMAIN, pid_type, pid_value)


# TODO: add this to PersonSchema
def get_pid_value(person: PersonSchema, pid_type):
    for identifier in person['identifiers']:
        if pid_type == identifier['idtype']:
            return str(identifier['idvalue'])
