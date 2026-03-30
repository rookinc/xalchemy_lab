# G15 Weight-6 M3 Runbook

## Purpose
Run the weight-6 support scan on the MacBook Pro M3 Pro.

This does **not** brute-force all syndromes directly.
Instead, it enumerates all 6-edge supports on G15, computes the induced 16-bit syndrome for each one, and classifies the support type.

That directly answers:

- which syndromes are realized by weight-6 supports,
- whether those supports are open, closed, connected, or disconnected,
- and whether `C6`, `C3+C3`, or path-like witnesses dominate at weight 6.

## Script
`scripts/g15_syndrome_bruteforce_weight6.py`

## Run
```bash
mkdir -p artifacts
python3 scripts/g15_syndrome_bruteforce_weight6.py \
  --json-out artifacts/g15_weight6_syndrome_scan.jsonMD
