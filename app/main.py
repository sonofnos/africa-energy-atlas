from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import countries, data, indicators, narrative

app = FastAPI(title="Africa Energy Atlas API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(countries.router)
app.include_router(indicators.router)
app.include_router(data.router)
app.include_router(narrative.router)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
