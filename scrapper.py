from playwright.async_api import async_playwright
from rapidfuzz import fuzz
import re
import asyncio
from collections import defaultdict


# evitamos cosas como productos para repuestos
PALABRAS_PROHIBIDAS = [
    "repuestos", "roto", "defectuoso", "para", "no funciona",
    "reparar", "arreglar", "refaccionar", "refacciones"
]

# palabras irrelevantes que no definen el producto
STOPWORDS = [
    "nuevo", "usado", "excelente", "libre", "desbloqueado",
    "reacondicionado", "garantia", "cargador", "bateria",
    "original", "caja", "sellado"
]


def normalizar_titulo(titulo):
    titulo = titulo.lower()
    titulo = re.sub(r'[^a-z0-9 ]', '', titulo)
    titulo = " ".join(titulo.split())

    palabras = titulo.split()

    if any(p in PALABRAS_PROHIBIDAS for p in palabras):
        return None

    palabras = [p for p in palabras if p not in STOPWORDS]

    return " ".join(palabras)


def extraer_features(titulo):
    modelo = None
    capacidad = None

    match_modelo = re.search(r'iphone\s*14\s*(pro\s*max|pro|max|plus)?', titulo)
    if match_modelo:
        modelo = match_modelo.group().replace(" ", "")

    match_cap = re.search(r'\b(64|128|256|512|1024)\b', titulo)
    if match_cap:
        capacidad = match_cap.group()

    return modelo, capacidad


def clave_producto(titulo):
    modelo, capacidad = extraer_features(titulo)

    if not modelo or not capacidad:
        return None

    key = f"{modelo}_{capacidad}"
    print(f"KEY: {key} for {titulo}")  # DEBUG
    return key



def es_similar(a, b):
    return fuzz.ratio(a["titulo"], b["titulo"]) > 90


def deduplicar(lista):
    unicos = []

    for item in lista:
        if not any(es_similar(item, x) for x in unicos):
            unicos.append(item)

    return unicos



def agrupar(productos):
    grupos = defaultdict(list)

    for item in productos:
        key = clave_producto(item["titulo"])
        if key:
            grupos[key].append(item)

    return grupos


async def run_scrapper():
    print("Starting scraper")
    resultados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        for i in range(4):
            try:
                offset = 48 * i
                url = f"https://listado.mercadolibre.com.ar/celulares-telefonos/celulares-smartphones/apple/iphone-14_Desde_{offset + 1}_NoIndex_True"

                await page.goto(url)
                await page.wait_for_load_state("networkidle")

                items = await page.query_selector_all("li.ui-search-layout__item")
                print("ITEMS:", len(items))
                for item in items:
                    title_el = await item.query_selector("h3")
                    price_el =  await item.query_selector(".andes-money-amount__fraction")
                    link_el = await item.query_selector("a")
                    link = None
                    if link_el:
                        link = await link_el.get_attribute("href")

                    if not title_el or not price_el:
                        continue

                    titulo_raw = await title_el.inner_text()
                    titulo = normalizar_titulo(titulo_raw)
                    

                    if not titulo:
                        continue

                    precio_texto = await price_el.inner_text()
                    precio = int(precio_texto.replace(".", ""))

                    resultados.append({
                        "titulo": titulo,
                        "price": precio,
                        "enlace":link
                    })
            except Exception as e:
                print(f"Error on page {i}: {e}")
                continue

        await browser.close()

    print(f"🔎 TOTAL SCRAPEADOS: {len(resultados)}")

    # 🧠 AGRUPAR
    grupos = agrupar(resultados)

    print("\n📊 RESULTADOS AGRUPADOS:\n")
    response = []
    for key, items in grupos.items():
        items = deduplicar(items)

        precios = [x["price"] for x in items]
        promedio = sum(precios) / len(precios)
        minimo = min(precios)

        productos = []
     
  

        for i in items:
            es_oportunidad = i["price"] < promedio
            productos.append({
                "titulo": i["titulo"],
                "precio": i["price"],
                "enlace": i["enlace"],
                "oportunidad": es_oportunidad
            })

        response.append({
            "producto": key,
            "promedio": int(promedio),
            "minimo": minimo,
            "cantidad": len(items),
            "items": productos
        })
    return response
if __name__ == "__main__":
    asyncio.run(run_scrapper())
