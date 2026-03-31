📦 PROYECTO: Price Checker - iPhone 14 Scraper

🧠 Descripción
Este proyecto es un scraper automatizado que obtiene publicaciones de MercadoLibre
para productos iPhone 14, analiza los títulos y precios, y permite detectar oportunidades
comparando productos similares.

El sistema:
- Scrapea múltiples páginas de resultados
- Normaliza títulos para poder compararlos correctamente
- Filtra publicaciones no válidas (ej: "roto", "para repuestos", etc.)
- Elimina ruido en los títulos (palabras irrelevantes)
- Agrupa productos similares
- Calcula precios promedio
- Detecta publicaciones por debajo del promedio (posibles oportunidades)

---

⚙️ Requisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

---

📥 Instalación

1. Clonar el repositorio:

   git clone https://github.com/Epileptic-Experience/scrapperPy.git
   cd scrapperPy

2. Crear entorno virtual (opcional pero recomendado):

   python -m venv venv
   source venv/bin/activate   (Linux/Mac)
   venv\Scripts\activate      (Windows)

3. Instalar dependencias:

   pip install -r requirements.txt

4. Instalar navegadores de Playwright:

   playwright install

---

🚀 Uso

Ejecutar el script principal:

   python main.py

Esto va a:
- Abrir el navegador
- Scrapear publicaciones de MercadoLibre
- Procesar los datos
- Mostrar resultados en consola

---


📊 Output esperado

El programa imprime:

- Lista de productos agrupados
- Precio mínimo por grupo
- Cantidad de publicaciones
- Oportunidades detectadas

---

⚠️ Notas importantes

- MercadoLibre puede cambiar su estructura HTML en cualquier momento
- El scraper depende de selectores CSS específicos
- Ejecutar con headless=False permite ver el navegador (debug)
- Para producción se recomienda usar headless=True

---

🛠️ Tecnologías utilizadas

- Playwright (scraping)
- RapidFuzz (comparación de strings)
- Python (lógica general)

---

📌 Mejoras futuras

- Exportar resultados a CSV / JSON
- Interfaz web
- Alertas automáticas (ej: Telegram / email)
- Soporte para múltiples productos
- Deploy en servidor o Docker

---

👨‍💻 Autor

Proyecto desarrollado para análisis de precios y detección de oportunidades.
