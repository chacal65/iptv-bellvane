from playwright.sync_api import sync_playwright
import json
import time

def capturar_links(url):
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page()

        links_encontrados = []

        def interceptar_request(request):
            if ".m3u8" in request.url and request.url.startswith("http"):
                links_encontrados.append(request.url)

        pagina.on("request", interceptar_request)

        pagina.goto(url, timeout=60000)

        try:
            elementos = [
                "button[aria-label='Close']",
                "button[class*='close']",
                "div[class*='close']",
                "text=✕",
                "xpath=//button[contains(text(), 'X')]",
                "xpath=//div[contains(text(), 'X')]"
            ]
            for seletor in elementos:
                popup = pagina.locator(seletor)
                if popup.is_visible():
                    popup.click(timeout=5000)
                    break
        except:
            pass

        tempo_maximo = time.time() + 60
        while time.time() < tempo_maximo:
            if links_encontrados:
                break
            time.sleep(1)

        navegador.close()
        return list(set(links_encontrados))

def processar_fontes(arquivo_fontes):
    with open(arquivo_fontes, 'r') as f:
        urls = f.read().splitlines()

    resultado = {}

    for url in urls:
        nome = url.strip().split('/')[-1].split('.')[0].upper()
        links = capturar_links(url)

        resultado[nome] = {
            "site_fonte": url,
            "grupo": "Sem Grupo",
            "logo": "",
            "links": links if links else []
        }

    with open('canais_temp.json', 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    processar_fontes('fontes.txt')
