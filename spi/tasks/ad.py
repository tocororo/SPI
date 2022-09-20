import ldap

username = "alejandro.cabreram"
password = "Acm97.321"

ldap_server = "ldap://ad.upr.edu.cu"
base_dn = "OU=_Usuarios,DC=upr,DC=edu,DC=cu"
user_dn = username + "@upr.edu.cu"
search_filter = "(&(objectClass=user)(sAMAccountName=" + username + "))"

ld = ldap.initialize(ldap_server);
# ld = ldap.open(ldap_server)
ld.protocol_version = 3
ld.set_option(ldap.OPT_REFERRALS, 0)


# bind user information to ldap connection
def get_ldap_list_persons():
    try:
        # print(ld.simple_bind_s(user_dn, password))
        ld.simple_bind_s(user_dn, password)
        results = ld.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
        # results = ld.search_s(base_dn, ldap.SCOPE_SUBTREE)
        print(results)
        ld.unbind_s()
        return results
    except ldap.INVALID_CREDENTIALS:
        print("Your username or password is invalid.")
    except Exception as e:
        print("Connection unsuccessful: " + str(e))
        ld.unbind_s()
        return []


if __name__ == '__main__':
    import asyncio

    results = get_ldap_list_persons()
    # for dn, entry in results:
        # print('Processing', repr(entry))
        # f = open("demofile3.json", "a")
        # f.write(str(entry))
        # f.close()
        # if entry and 'mail' in entry.keys() and 'employeeID' in entry.keys() and entry['employeeID'] === CI:
        #     print(entry['mail'])
        # break
