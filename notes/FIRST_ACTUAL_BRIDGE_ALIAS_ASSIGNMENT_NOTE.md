# First Actual Bridge Alias Assignment Note

## Checkpoint

The bridge symbols are now assigned to actual edge labels in the full 30-edge G15 template.

## Assigned aliases

- x  = e00

Twist paths:
- a  = e00
- b  = e04
- c  = e01
- d  = e07

Square cycle:
- s1 = e00
- s2 = e04
- s3 = e07^-1
- s4 = e01^-1

## Geometric reading

### global_return
Uses e00, so:
- q0 -> q1 -> q0

### global_twist
Compares two actual paths from q0 to q5:
- path 1 = e00, e04 = q0 -> q1 -> q5
- path 2 = e01, e07 = q0 -> q2 -> q5

### global_square
Uses the actual 4-cycle:
- q0 -> q1 -> q5 -> q2 -> q0

So the bridge specimens are no longer floating symbolic paths.
They are now tied to actual edges of the full G15 template.

