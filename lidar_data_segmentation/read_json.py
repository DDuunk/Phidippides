import json


def read_json():
    with open('../json-parser/output/output.json') as f:
        data = json.load(f)
    return data
