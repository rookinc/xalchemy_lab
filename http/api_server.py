from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from server.dictionary.routes import router as dictionary_router
from server.graph.routes import router as graph_router
from server.extruder.routes import router as extruder_router


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

# API routers
app.include_router(dictionary_router)
app.include_router(graph_router)
app.include_router(extruder_router)

# Static mounts
app.mount("/shared", StaticFiles(directory=BASE_DIR / "shared"), name="shared")
app.mount("/graph_viewer_assets", StaticFiles(directory=BASE_DIR / "graph_viewer"), name="graph_viewer_assets")
app.mount("/extruder_poc", StaticFiles(directory=BASE_DIR / "extruder_poc"), name="extruder_poc")


@app.get("/")
def root_index():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/lab")
def lab_index():
    return FileResponse(BASE_DIR / "lab" / "index.html")


@app.get("/notes")
def notes_index():
    return FileResponse(BASE_DIR / "notes" / "index.html")


@app.get("/concepts")
def concepts_index():
    return FileResponse(BASE_DIR / "concepts" / "index.html")


@app.get("/structures")
def structures_index():
    return FileResponse(BASE_DIR / "structures" / "index.html")


@app.get("/graph_viewer")
def graph_viewer_index():
    return FileResponse(BASE_DIR / "graph_viewer" / "lab.html")


@app.get("/graph_viewer/")
def graph_viewer_index_slash():
    return RedirectResponse(url="/graph_viewer", status_code=307)


@app.get("/graph_viewer/index.html")
def graph_viewer_index_html():
    return RedirectResponse(url="/graph_viewer", status_code=307)


@app.get("/graph_viewer_legacy")
def graph_viewer_legacy_index():
    return FileResponse(BASE_DIR / "graph_viewer" / "index.html")


@app.get("/extruder")
def extruder_index():
    return FileResponse(BASE_DIR / "extruder_poc" / "index.html")
