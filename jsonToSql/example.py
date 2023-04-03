import json

f = open('../data/example.json', "r")
data: dict = json.loads(f.read())

i = 0
for key in data:
    amount = float(key['amount'])
    stockId = key['stockId']
    if stockId == '8e77ae93-a777-485e-b5a3-5327d6ba889d' and amount > 0:
        i += 1

print(str(i))