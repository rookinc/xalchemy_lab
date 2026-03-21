# Two-Sided Anchor Fan Result

## Checkpoint

The anchor edge `e00` was scanned from both orientations:

- q0 -> q1
- q1 -> q0

In both directions, the anchor supports exactly three 4-cycle arms:

- two even arms
- one odd arm

## q0 -> q1 view

Even arms:
- {e05,e10,e02}
- {e06,e13,e03}

Odd arm:
- {e04,e07,e01}

## q1 -> q0 view

Even arms:
- {e02,e10,e05}
- {e03,e13,e06}

Odd arm:
- {e01,e07,e04}

## Meaning

The anchor fan is two-sided and orientation-stable.

The odd arm remains unique from either orientation.
The even arms remain multiple from either orientation.

## Strongest current reading

The local bridge geometry is now visibly organized as:

- a hinge edge `e00`
- one distinguished odd continuation arm
- a family of even continuation arms

So the twist packet is the unique odd arm of the anchor fan, while the square packet is one chosen representative of the even-arm family.

