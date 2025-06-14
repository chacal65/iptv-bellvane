from playwright.sync_api import sync_playwright
import json
import time

with open('fontes.txt', 'r') as file:
    urls = [line.strip() for line in file.readlines()]

resultado = {}

def capturar_link(url):
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page()

        try:
            pagina.goto(url, timeout=60000)

            try:
                pagina.locator("button:has-text('X'), .close, .btn-close").first.click(timeout=5000)
            except:
                pass

            time.sleep(5)

            links = []
            for req in pagina.context.request.finished():
                link = req.url
                if '.m3u8' in link:
                    links.append(link)

            return list(set(links))

        except:
            return []
        finally:
            navegador.close()


for url in urls:
    nome_canal = url.strip().split("/")[-1].upper() or "DESCONHECIDO"

    links = capturar_link(url)
    resultado[nome_canal] = {
        "site_fonte": url,
        "grupo": "Sem Grupo",
        "logo": "",
        "links": links
    }

with open('canais_temp.json', 'w', encoding='utf-8') as f:
    json.dump(resultado, f, ensure_ascii=False, indent=4)
