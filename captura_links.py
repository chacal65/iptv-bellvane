import asyncio
from playwright.async_api import async_playwright
import json
import os

# Carregar fontes
with open('fontes.txt', 'r') as f:
    fontes = [linha.strip() for linha in f if linha.strip()]

# Carregar canais existentes ou criar vazio
if os.path.exists('canais_temp.json'):
    with open('canais_temp.json', 'r') as f:
        canais = json.load(f)
else:
    canais = {}

async def captura():
    async with async_playwright() as p:
        navegador = await p.chromium.launch(headless=True)
        contexto = await navegador.new_context()
        pagina = await contexto.new_page()

        for url in fontes:
            print(f"Capturando {url}")

            try:
                await pagina.goto(url, timeout=60000)

                # Fechar pop-ups se tiver botão X
                try:
                    await pagina.click('button:has-text("×")', timeout=5000)
                except:
                    pass

                # Espera pelo player carregar
                await pagina.wait_for_timeout(10000)

                # Captura qualquer solicitação para arquivos .m3u8
                link_m3u8 = None

                def capturar_resposta(resposta):
                    nonlocal link_m3u8
                    if resposta.url.endswith('.m3u8'):
                        link_m3u8 = resposta.url

                pagina.on('response', capturar_resposta)

                # Interage um pouco para garantir carregamento
                await pagina.wait_for_timeout(5000)

                nome_canal = url.strip('/').split('/')[-1].upper()
                if nome_canal == "":
                    nome_canal = "CANAL"

                if nome_canal not in canais:
                    canais[nome_canal] = {
                        'site_fonte': url,
                        'grupo': 'Sem Grupo',
                        'logo': '',
                        'links': []
                    }

                if link_m3u8 and link_m3u8 not in canais[nome_canal]['links']:
                    canais[nome_canal]['links'].append(link_m3u8)
                    print(f"Capturado: {link_m3u8}")
                else:
                    print(f"Nenhum link .m3u8 encontrado para {nome_canal}")

            except Exception as e:
                print(f"Erro ao capturar {url}: {e}")

        await navegador.close()

    # Salvar canais_temp.json
    with open('canais_temp.json', 'w') as f:
        json.dump(canais, f, indent=4, ensure_ascii=False)
    print('Arquivo canais_temp.json atualizado.')

asyncio.run(captura())
