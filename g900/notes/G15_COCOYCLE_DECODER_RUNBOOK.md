# G15 Cocycle Decoder Runbook

## Purpose
Given a 16-bit tree-gauge syndrome for the signed cocycle on G15, solve the minimum-weight support problem and classify the witness shape.

## Script
`scripts/g15_cocycle_decode.py`

## Inputs
- a 16-bit syndrome string in the chosen fundamental-cycle basis

## Output
- all minimum-weight solutions found up to the chosen weight cutoff
- whether each solution is closed
- whether each solution is connected
- support type:
  - `C6`
  - `C3+C3`
  - `P7`
  - `cycle`
  - `path`
  - `other`

## Example run
```bash
python3 scripts/g15_cocycle_decode.py --syndrome 0000000000000000
