import json

with open('canais.json', 'r', encoding='utf-8') as f:
    canais = json.load(f)

with open('lista.m3u', 'w', encoding='utf-8') as m3u:
    m3u.write('#EXTM3U\n')

    for nome, dados in canais.items():
        if dados.get('links'):
            link = dados['links'][0]
            grupo = dados.get('grupo', 'Sem Grupo')
            logo = dados.get('logo', '')

            m3u.write(f'#EXTINF:-1 tvg-id="{nome}" tvg-name="{nome}" tvg-logo="{logo}" group-title="{grupo}",{nome}\n')
            m3u.write(f'{link}\n')
