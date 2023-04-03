import csv
import json

filename = "data/NewValues.csv"
filenameJson = "data/AuditLogConfiguration.json"
notedRows: dict = {}
implementedRows: list = []
newRows: list = []


with open(filename, "r") as csv_file:
    csv_reader = csv.reader(open(filename, 'r', encoding='utf_8'), delimiter=';')
    for row in csv_reader:
        if "Áno" in row[1] or "na android" in row[1]:
            notedRows[row[0]] = row[2]


with open(filenameJson, "r", encoding='utf-8') as json_file:
    data = json.load(json_file)
    implementedRows = data["methods"]

    print('implementedRows', len(implementedRows))

    for key, value in notedRows.items():
        is_there = False
        for ir in implementedRows:
            if key == ir['key']:
                is_there = True
                break
        if not is_there:
            newRows.append({'key': key, 'code': key, 'subsystem': 'KMZ-A', 'msg': value})

    data['methods'].append(newRows)
    with open('data/new_filename.json', "w", encoding="utf-8") as json_file:
        json.dump(newRows, json_file, ensure_ascii=False)

    with open('data/new_filenameSql.txt', "w", encoding="utf-8") as sql_file:
        for nr in newRows:
            sql_file.write('(\'AUDIT_CONFIG\', \''+ nr['key'] +'\', null, N\'[{"attribute": "description", "value": "' + nr['msg'] + '"}, {"attribute": "active", "value": true}, {"attribute": "servio", "value": false}]\', 1),\n')
