import csv
import json


# function for making the json file for the given csv file

def csv_to_json(csvFilePath, jsonFilePath):
    json_list = []

    with open(csvFilePath) as csvf:
        csvReader = csv.DictReader(csvf)

        for row in csvReader:
            if row['conv_id'] == str(i):
                diction = {'nlg': row.get('utterance'), 'false nlg': " "}
                nested_row = {'speaker': row.get('speaker'), 'utterance': diction}
                json_list.append(nested_row)

    with open(jsonFilePath, 'w') as jsonf:
        json_String = json.dumps(json_list, indent=4)
        jsonf.write(json_String)


csvFilePath = r'dialogue_docpat.csv'
for i in range(1, 604):
    jsonFilePath = r'id'+str(i)+'.json'
    csv_to_json(csvFilePath, jsonFilePath)

'''jsonFilePath = r'id1.json'
csv_to_json(csvFilePath, jsonFilePath)'''