from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
import time
from main import main
from whales_v_retail import get_whales

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    FastAPICache.init(InMemoryBackend(), prefix="mispriced")
    yield

app = FastAPI(lifespan=lifespan, title="Prediction Market Edge Finder")


@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/mispriced")
@cache(expire=7200)
async def get_mispriced():
    try:
        result = await main()
        return result
    except Exception as e:
        return {"error": str(e), "status": "failed"}

@app.get("/whale_signal/{link:path}")
async def whale_signal(link):
    try:
        result = await get_whales(link)
        return result
    except Exception as e:
        return {"error": str(e), "status": "failed"}