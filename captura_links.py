from playwright.sync_api import sync_playwright
import json

def capturar_links(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        links = []

        def handle_request(request):
            if ".m3u8" in request.url or "/live/" in request.url or "/hls/" in request.url:
                print("Link encontrado:", request.url)
                links.append(request.url)

        page.on("request", handle_request)

        try:
            page.goto(url, timeout=60000)
            
            # Tentativa de fechar pop-up pelo botão X
            try:
                page.locator("button:has-text('X')").click(timeout=3000)
                print("Pop-up fechado!")
            except:
                print("Nenhum pop-up com botão X encontrado, seguindo...")

            # Espera pra garantir carregamento do player
            page.wait_for_timeout(15000)  # 15 segundos

        except Exception as e:
            print("Erro ao acessar a página:", e)

        browser.close()
        return links


def processar_fontes(arquivo_fontes):
    with open(arquivo_fontes, 'r') as f:
        urls = f.read().splitlines()

    resultado = {}

    for url in urls:
        nome = url.strip().split('/')[-1].split('.')[0].upper()
        links_encontrados = capturar_links(url)

        if links_encontrados:
            resultado[nome] = {
                "site_fonte": url,
                "grupo": "Sem Grupo",
                "logo": "",
                "links": links_encontrados
            }
        else:
            resultado[nome] = {
                "site_fonte": url,
                "grupo": "Sem Grupo",
                "logo": "",
                "links": []
            }

    with open('canais_temp.json', 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    print("Arquivo canais_temp.json gerado com sucesso.")


if __name__ == "__main__":
    processar_fontes('fontes.txt')
