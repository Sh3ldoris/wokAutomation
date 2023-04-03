import json

def main():
    sql_file = open('../data/AuditConfigurationInit.sql', 'x')
    jsrot_data: dict = __open_file_and_get_data('../data/AuditLogConfigurationJsrot.json')
    servio_data: dict = __open_file_and_get_data('../data/AuditLogConfigurationServio.json')

    sql_file.write('MERGE WF_CODEBOOK_VALUE v\nUSING (\n\tselect *\n\tfrom (values\n\t\t')

    methods: list = jsrot_data['methods']
    exceptions: list = jsrot_data['exceptions']
    method_length: int = len(methods)
    exception_length: int = len(exceptions)

    for i in range(method_length):
        method: dict = methods[i]
        sql_file.write('(\'AUDIT_CONFIG\', \'' + method['key'] + '\', \'' + method['msg'] + '\', \'')
        sql_file.write(__create_attribute_json() + '\', 1),\n\t\t')

    for i in range(exception_length):
        method: dict = exceptions[i]
        sql_file.write('(\'AUDIT_CONFIG\', \'' + method['key'] + '\', \'Výjimka\', \'')
        sql_file.write(__create_attribute_json() + '\', 1),\n\t\t')

    methods = servio_data['methods']
    method_length: int = len(methods)

    for i in range(method_length):
        method: dict = methods[i]
        sql_file.write('(\'AUDIT_CONFIG\', \'' + method['key'] + '\', \'' + method['msg'] + '\', \'')
        sql_file.write(__create_attribute_json(servio=True) + '\', 1)')
        sql_file.write(',\n\t\t') if i < method_length - 1 else sql_file.write('\n\t\t\t')

    entities: list = servio_data['entities']
    entities_length: int = len(entities)

    for i in range(entities_length):
        method: dict = entities[i]
        sql_file.write('(\'AUDIT_CONFIG\', \'' + method['key'] + '\', \'\', \'')
        sql_file.write(__create_attribute_json(servio=True) + '\', 1)')
        sql_file.write(',\n\t\t') if i < method_length - 1 else sql_file.write('\n\t\t\t')


    sql_file.write(') newPlo (codebook_id, code, c_value, extra_values, valid)\n) n\n')
    sql_file.write('ON (v.CODEBOOK_ID = n.CODEBOOK_ID and v.CODE = n.CODE)\n')
    sql_file.write('WHEN MATCHED THEN\n\tUPDATE\n\tSET c_value = n.c_value, extra_values = n.extra_values\n')
    sql_file.write('WHEN NOT MATCHED BY TARGET THEN\n\t')
    sql_file.write('INSERT (CODEBOOK_ID, CODE, c_value, extra_values, VALID, LAST_UPDATE)\n\t')
    sql_file.write('VALUES (n.CODEBOOK_ID, n.CODE, n.C_VALUE, extra_values, n.VALID, CURRENT_TIMESTAMP);')
    sql_file.close()


def __open_file_and_get_data(file: str) -> dict:
    # JSON file
    f = open(file, "r")
    # Reading from file
    data: dict = json.loads(f.read())
    f.close()
    return data

def __create_attribute_json(active: bool = True, servio: bool = False) -> str:
    active_value: dict = {
        'attribute': 'active',
        'value': active
    }
    servio_value: dict = {
        'attribute': 'servio',
        'value': servio
    }

    return json.dumps([active_value, servio_value])

if __name__ == '__main__':
    main()
