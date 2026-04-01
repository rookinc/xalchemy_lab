# Computational Results for the Bounded Frame-2 Obstruction Regime

## Status
Working draft

## Established results
- Baseline two-step policy is monotone in normalized action distance on the sampled run.
- Baseline produces no nontrivial exact closure.
- Exact-preference repair recovers the dominant reachable frame-0 chamber.
- Residual basin funnels into the frame-2 near-action seam.
- Distinguished locked witnesses are Hamming-1 from exact frame 2 with mismatch at slot 4.
- Exact frame-2 closure requires slot 4 = t2.
- Each locked witness has no exact one-edit child.
- Each locked witness has exactly 7 frame-2 d_A=1 one-edit children.
- Bounded escape-return regime generated from locked witnesses with one-edit moves and cutoff d_A <= 3 saturates by depth 6.
- No new states appear at depths 7 and 8.
- Total visited states: 58,624.
- No exact frame-2 closure appears anywhere in the saturated bounded regime.
- No state in the saturated bounded regime has slot 4 = t2.

## Slot-4 alphabets
### Global bounded regime
{o0, o1, o2, o3, o4, s0, s2, s3, s4, t0, t3, t4}

### Frame-2 seam inside bounded regime
{o4, s0, s2, s3, s4, t0, t3, t4}

## Working interpretation
The repaired machine can find the frame-2 seam but does not install the exact slot-4 value required to seal it.
