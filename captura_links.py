from playwright.sync_api import sync_playwright
import json
import time


def capturar_links(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        links_encontrados = []

        def handle_request(request):
            if ".m3u8" in request.url or "/live/" in request.url or "hls" in request.url:
                links_encontrados.append(request.url)

        page.on("request", handle_request)

        try:
            page.goto(url, timeout=60000)

            # Fechar pop-up se existir
            try:
                page.locator('xpath=//button[contains(text(), "X")]').click(timeout=5000)
            except:
                pass  # Ignorar se não tiver popup

            # Espera o player carregar
            time.sleep(15)

        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")

        browser.close()
        return links_encontrados


def processar_fontes(arquivo_fontes):
    with open(arquivo_fontes, 'r') as f:
        urls = f.read().splitlines()

    resultado = {}

    for url in urls:
        nome = url.strip().split('/')[-1].split('.')[0].upper()
        print(f"Capturando links de: {nome}")

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
