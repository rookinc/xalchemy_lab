from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from server.graph.graph_routes import router as graph_router
from server.dictionary.routes import router as dictionary_router

app = FastAPI()

app.include_router(graph_router, prefix="/api")
app.include_router(dictionary_router, prefix="/api")

app.mount("/", StaticFiles(directory=".", html=True), name="static")
