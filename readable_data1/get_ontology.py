# 根据readable_data整理出ontology文件
import json
from collections import defaultdict
def read_json(fp):
    with open(fp, 'r', encoding='utf8') as json_file:
        data = json.load(json_file)
    return data

def save_json(data, fp):
    with open(fp, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file)

type = ['test', 'train', 'val']
filename = [f'readabe_{t}_data.json' for t in type]
slots = set()
values = defaultdict(set)

for file in filename:
    datas = read_json(file)
    for ob in datas:
        for t in ob['turns']:
            for dialog_act in t["dialog_act"]:
                 if dialog_act[-2] not in ['', ' ', 'none', None]:
                    slots.add(dialog_act[-2])
                    if dialog_act[-1] not in ['', ' ', 'none', None]:
                        values[dialog_act[-2]].add(dialog_act[-1].rstrip('元'))

slots = list(slots)
for key in values.keys():
    values[key] = list(values[key])

ontology = {
    'slots': slots,
    'values': values
}
save_json(ontology, 'ontology.json')