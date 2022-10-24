import opencv
import pickle
import json
import pandas

df = open("concept_dic_1.pkl","rb")
data = pickle.load(df)

dict_temp = {}

for key, value in data.items():
    dict_temp[key] = []
    for item in value:
        dict_temp[key].append(key + ", " + item[0] + ", " + item[1])

with open('concept_dic_mini.json', 'w') as outfile:
    json.dump(dict_temp, outfile)
