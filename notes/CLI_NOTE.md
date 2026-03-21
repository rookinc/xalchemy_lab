# CLI note

The app now has a Python CLI entrypoint:

- PYTHONPATH=src python -m xalchemy_lab.app.cli ...

or via the shell wrapper:

- ./summon ...

## Commands

- ./summon cube
- ./summon png
- ./summon gallery
- ./summon contact
- ./summon sheet
- ./summon dxf
- ./summon all

## Config

Default config path:
- config/app.toml

Current first version:
- loads TOML config
- dispatches subcommands
- keeps exporter modules as the real workhorses

Future version:
- pass config values directly into renderers
- allow CLI overrides such as --kernel, --outdir, --state

