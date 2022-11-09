import ldap, os

from spi.controllers import PersonsController, PidsController
from spi.database import connect
from spi.logger_base import create_log

username = os.getenv('LDAP_USERNAME')
password = os.getenv('LDAP_PASSWORD')
ldap_server = os.getenv('LDAP_SERVER')
email_domain = os.getenv('EMAIL_DOMAIN')

base_dn = "OU=_Usuarios,DC=upr,DC=edu,DC=cu"
user_dn = username + email_domain
search_filter = "(&(objectClass=user)(sAMAccountName=" + username + "))"

ld = ldap.initialize(ldap_server);
ld.protocol_version = 3
ld.set_option(ldap.OPT_REFERRALS, 0)


# get list of persons from ldap protocol
def get_ldap_list_persons():
    try:
        # print(ld.simple_bind_s(user_dn, password))
        ld.simple_bind_s(user_dn, password)
        # results = ld.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
        results = ld.search_s(base_dn, ldap.SCOPE_SUBTREE)
        ld.unbind_s()
        return results
    except ldap.INVALID_CREDENTIALS:
        create_log('ad').error(f'INVALID_CREDENTIALS: {ldap.INVALID_CREDENTIALS}')
        # print("Your username or password is invalid.")
    except Exception as e:
        create_log('ad').error(f"Connection unsuccessful: {str(e)}")
        # print("Connection unsuccessful: " + str(e))
        ld.unbind_s()
        return []


# save persons from ldap protocol to DB
async def save_ldap_list_persons(ldap_persons):
    for dn, entry in ldap_persons:
        # check for the employeeID and get the person
        if entry and 'employeeID' in entry.keys():
            employeeID = entry['employeeID'][0].decode("utf-8")
            person = await PersonsController.retrieve_one_by_pid({"idvalue": employeeID})

            # check for the employeeID and update the person's aliases
            if person and entry and 'displayName' in entry.keys():
                aliases = person['aliases']
                displayName = entry['displayName'][0].decode("utf-8")
                if displayName not in aliases:
                    aliases += [entry['displayName'][0].decode("utf-8")]
                    await PersonsController.update_person(
                        person['_id'],
                        {"$set": dict(aliases=aliases)}
                    )
                    print('update aliases')
                    print("=========================")

            # check for the mail and update the person's email
            if entry and 'mail' in entry.keys():
                employeeID = entry['employeeID'][0].decode("utf-8")
                mail = entry['mail'][0].decode("utf-8")
                institutional_email = await PersonsController.retrieve_one({'institutional_email': mail})
                if not institutional_email:
                    pids = await PidsController.retrieve_one({"idvalue": employeeID})
                    if pids:
                        await PersonsController.update_person(
                            pids['person_id'],
                            {"$set": dict(institutional_email=mail)}
                        )
                        print('update email')
                        print("=========================")


if __name__ == '__main__':
    import asyncio

    asyncio.run(connect())

    # results = get_ldap_list_persons()
    list = get_ldap_list_persons()
    asyncio.run(save_ldap_list_persons(list))

    #print(results) 

    # for dn, entry in results:
    # print(entry['displayName'][0].decode("utf-8"))

    # for dn, entry in results:
    # print('Processing', repr(entry))
    # f = open("demofile3.json", "a")
    # f.write(str(entry))
    # f.close()
    # if entry and 'mail' in entry.keys() and 'employeeID' in entry.keys() and entry['employeeID'] === CI:
    #     print(entry['mail'])
    # break
