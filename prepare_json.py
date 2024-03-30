from json import dump
projects = {'test_project': ['HP OfficeJet Pro', 'Artica Proxy']}
with open('C:/Users/о/PycharmProjects/UFA_HACK_2024/proj_components.json', 'w') as json_file:
    dump(projects, json_file)
