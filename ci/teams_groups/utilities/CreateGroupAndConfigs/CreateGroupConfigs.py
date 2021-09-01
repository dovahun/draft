import argparse
import urllib3
import logging
from python_freeipa import ClientMeta
from python_freeipa import exceptions as FreeipaExceptions
import sys
from ruamel.yaml import YAML
from ruamel.yaml import YAMLError
import yaml
import glob


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, help='input dir')
    parser.add_argument('--domain', type=str, help='FreeIPA host')
    parser.add_argument('-u', type=str, help='FreeIPA login')
    parser.add_argument('-p', type=str, help='FreeIPA password')
    parser.add_argument('-of', type=str, help='output configs files')
    return vars(parser.parse_args())


# Логгирование
def logger():
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    return log


# Подключение к ldap
def client(domain, login, password):
    try:
        Log.info("Подключение к ldap")
        client = ClientMeta(domain, verify_ssl=False)
        client.login(login, password)
        return client
    except FreeipaExceptions.FreeIPAError as e:
        Log.exception(e)
        sys.exit(1)


# Парсинг yaml файла
def readInput(path):
    gitGroup = []
    yml = YAML(typ='safe')
    try:
        Log.info("Парсинг yaml файлов")
        files = glob.glob(path + "*.yaml")
        for file in files:
            content = yml.load(open(file))
            gitGroup.append(content)
        return gitGroup
    except YAMLError as e:
        Log.exception(e)
        sys.exit(1)


# Создание списка групп которые есть в ldap
def getLdapGroup(client):
    ldapGroup = {}
    try:
        for group in client.group_find(o_sizelimit=0)['result']:
            ldapGroup[group['cn'][0]] = group
        return ldapGroup
    except FreeipaExceptions.FreeIPAError as e:
        Log.exception(e)
        sys.exit(1)


# Создание/удаление группы
def createGroup(client, gitGroup, ldapGroup):
    for group in gitGroup:
        try:
            if group['state'] == 'present' and group['name'] not in ldapGroup:
                Log.info("Начался процесс создания группы: {}".format(group['name']))
                client.group_add(group['name'])
                Log.info("Создание группы: {} завершилось успешно.".format(group['name']))
            if group['state'] == 'absent' and group['name'] in ldapGroup:
                Log.info("Начался процесс удаления группы: {}".format(group['name']))
                client.group_del(group['name'])
                Log.info("Группа: {} была удалена.".format(group['name']))
        except FreeipaExceptions.FreeIPAError as e:
            Log.exception(e)
            sys.exit(1)


#Создание конфигурационных файлов для создания team
def createTeam(gitTeam):
    template = {
        "name": [""],
        "state": [""],
        "roles": [
            {
                "local": {
                    "users": [
                        "admin"
                    ]
                },
                "name": "owner",
                "ldap": {
                    "groups": ["concourse-admins", "devops"]
                }
            },
            {
                "local": {
                    "users": [
                        "admin"
                    ]
                },
                "name": "member",
                "ldap": {
                    "groups": ["", "devops"]
                }
            },
            {
                "local": {
                    "users": [
                        "admin"
                    ]
                },
                "name": "viewer",
                "ldap": {
                    "groups": [
                        "concourse-users"
                    ]
                }
            }
        ]
    }
    for team in gitTeam:
        if team['state'] == 'present':
            path_config = args['of'] + team['name'] + '.yaml'
            to_yaml = template
            to_yaml["roles"][1]["ldap"]["groups"][0] = team['name']
            to_yaml["name"] = team['name']
            to_yaml["state"] = team['state']
            with open(path_config, 'w') as f:
                yaml.dump(to_yaml, f)

# Запуск функций
if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    Log = logger()
    args = args()
    client = client(args['domain'], args['u'], args['p'])
    gitGroup = readInput(args['i'])
    ldapGroup = getLdapGroup(client)
    createGroup(client, gitGroup, ldapGroup)
    createTeam(gitGroup)