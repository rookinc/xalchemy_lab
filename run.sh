#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

case "${1:-}" in
  svg)
    PYTHONPATH=src python -m xalchemy_lab.app.export_g60_cube_svg
    ;;
  png)
    PYTHONPATH=src python -m xalchemy_lab.app.export_g60_cube_png
    ;;
  tk)
    PYTHONPATH=src python -m xalchemy_lab.app.run_g60_cube_kernel_tk
    ;;
  gallery)
    PYTHONPATH=src python -m xalchemy_lab.app.export_g60_state_cube_svg
    ;;
  contact)
    PYTHONPATH=src python -m xalchemy_lab.app.export_g60_state_contact_sheet
    ;;
  sheet)
    PYTHONPATH=src python -m xalchemy_lab.app.export_g60_state_sheet_svg
    ;;
  *)
    echo "usage: ./run.sh {svg|png|tk|gallery|contact|sheet}"
    exit 1
    ;;
esac
