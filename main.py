
from fastapi import FastAPI
from scrapper import run_scrapper
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return{"status:": "Api funcionando"}

from fastapi.responses import JSONResponse
from fastapi import FastAPI
import traceback

app = FastAPI()

@app.get("/scrape")
async def scrape():
    try:
        data = await run_scrapper()

        # 🔒 SIEMPRE devolver estructura consistente
        if not data:
            return JSONResponse(content={"results": []})

        return JSONResponse(content={"results": data})

    except Exception as e:
        print(traceback.format_exc())

        return JSONResponse(content={
            "error": str(e),
            "results": []
        })