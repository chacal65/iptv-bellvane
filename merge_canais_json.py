import json
import os

if not os.path.exists('canais_temp.json'):
    exit()

with open('canais_temp.json', 'r', encoding='utf-8') as temp_file:
    canais_temp = json.load(temp_file)

if os.path.exists('canais.json'):
    with open('canais.json', 'r', encoding='utf-8') as canais_file:
        canais = json.load(canais_file)
else:
    canais = {}

for nome, dados in canais_temp.items():
    canais[nome] = dados

with open('canais.json', 'w', encoding='utf-8') as output_file:
    json.dump(canais, output_file, indent=2, ensure_ascii=False)
