# Anchor Fan Geometry Note

## Checkpoint

The anchor edge `e00` sits in exactly three supported anchored 4-cycles.

These cycles split into:

### Odd anchored cycle
- q0 -> q1 -> q5 -> q2 -> q0
- packet beyond anchor: {e04,e07,e01}

### Even anchored cycle A
- q0 -> q1 -> q6 -> q3 -> q0
- packet beyond anchor: {e05,e10,e02}

### Even anchored cycle B
- q0 -> q1 -> q7 -> q4 -> q0
- packet beyond anchor: {e06,e13,e03}

## Meaning

The anchor does not support just one square packet and one twist packet.

Instead, it supports a local 3-arm fan:
- one odd arm
- two even arms

So the current square packet {e02,e05,e10} is best read as a chosen representative of an even-arm family, while the twist packet {e01,e04,e07} is the unique odd arm in the anchored fan.

## Strongest current reading

The clustered bridge law is now beginning to admit a geometric derivation:

- e00 is the anchor hinge
- the anchor opens into a fan of continuation packets
- odd/twist is the unique odd arm
- square is a representative of the even-arm family

