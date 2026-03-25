# Graph Viewer

Browser-side graph rendering module.

## Role in the pipeline

This folder is the final render stage for graph views.

Pipeline:

MySQL graph tables
-> FastAPI `/api/graphs/{graph_key}/views/{view_key}`
-> browser fetch
-> in-memory graph build
-> spring solver
-> canvas render

## Source of truth

The database is the source of truth for:

- graphs
- graph_nodes
- graph_edges
- graph_views
- graph_view_nodes
- graph_view_edges
- graph_actions
- graph_view_actions

This folder does not define canonical graph content. It consumes API payloads and renders them.

## Current contents

- `petersen.html`
  Standalone debug harness for the Petersen graph view.

- `kernel/spring_solver.js`
  Force-directed layout computation.

- `kernel/canvas_renderer.js`
  2D canvas rendering and pointer interaction.

## Current purpose

Validate the graph pipeline end to end:

- DB-backed graph definition
- API-backed view retrieval
- browser-side computation
- browser-side rendering
