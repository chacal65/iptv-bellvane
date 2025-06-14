from playwright.sync_api import sync_playwright
import json
import time

with open('fontes.txt', 'r') as f:
    urls = [linha.strip() for linha in f if linha.strip()]

resultado = {}

def capturar_m3u8(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        links_encontrados = []

        def intercepta_response(response):
            if ".m3u8" in response.url:
                links_encontrados.append(response.url)

        page.on("response", intercepta_response)

        try:
            page.goto(url, timeout=60000)
            time.sleep(10)

            try:
                page.locator("button:has-text('×')").click(timeout=3000)
            except:
                pass

        except:
            pass

        browser.close()
        return list(set(links_encontrados))

for url in urls:
    links = capturar_m3u8(url)

    nome_canal = url.strip('/').split('/')[-1].upper()
    if nome_canal == "":
        nome_canal = "SEM_NOME"

    resultado[nome_canal] = {
        "site_fonte": url,
        "grupo": "Sem Grupo",
        "logo": "",
        "links": links
    }

with open('canais_temp.json', 'w', encoding='utf-8') as f:
    json.dump(resultado, f, ensure_ascii=False, indent=4)
