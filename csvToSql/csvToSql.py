import csv

filename = 'data/example.csv'
output_file = 'data/Delete-149vs150.sql'

with open(filename, 'r') as file, open(output_file, 'w') as output:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        db_id, author, file_name = row
        output.write(f"delete from jsrot.DATABASECHANGELOG where ID = '{db_id}' and AUTHOR = '{author}' and FILENAME = '{file_name}';\n")