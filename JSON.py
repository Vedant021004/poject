import json

text = '{"name":"Vedant","age":20}'

data = json.loads(text)

print(data)
print(type(data))

# 

import json

person = {
    "name": "Vedant",
    "age": 20
}

json_data = json.dumps(person)

print(json_data)
print(type(json_data))