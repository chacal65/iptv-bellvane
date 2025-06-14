import json


def gerar_m3u(arquivo_json, arquivo_m3u):
    with open(arquivo_json, 'r', encoding='utf-8') as f:
        canais = json.load(f)

    with open(arquivo_m3u, 'w', encoding='utf-8') as m3u:
        m3u.write('#EXTM3U\n')

        for nome, info in canais.items():
            links = info.get('links', [])
            if links:
                for link in links:
                    m3u.write(f'#EXTINF:-1 group-title="{info.get("grupo", "Sem Grupo")}",{nome}\n')
                    m3u.write(f'{link}\n')


if __name__ == "__main__":
    gerar_m3u('canais.json', 'lista.m3u')
