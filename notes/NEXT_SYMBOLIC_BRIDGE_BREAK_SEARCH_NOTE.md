# Next Symbolic Bridge Break Search Note

## Goal

Keep the current symbolic evaluator fixed and push the bridge table outward until the first mismatch appears.

This is the cleanest next diagnostic step.

We are no longer asking whether the current symbolic bridge works on the original named rows.
It does.

We are now asking:

> how far does it keep working before it breaks?

## Fixed symbolic evaluator

Keep the current provisional symbolic evaluator unchanged:

- out-and-back loop -> 0
- small untwisted cycle -> 0
- two-path comparison -> 1

Do not tune it during this pass.

## Strategy

Add more existing local words as diagnostic rows and assign each one a provisional symbolic global role by mod-2 intent.

Then run the bridge table and inspect:

- the first mismatch,
- the first ambiguous row,
- or the first row whose symbolic role assignment feels forced.

That point will tell us where the current symbolic bridge vocabulary stops being natural.

## Why this matters

A symbolic bridge that only works on the original hand-picked rows is weak.

A symbolic bridge that survives a wider nearby family is stronger.

A symbolic bridge that eventually fails in an informative way is even better, because the failure reveals exactly what extra structure is missing.

## What to record

When the first mismatch appears, record:

- local word
- local lift_bit
- assigned symbolic global role
- symbolic global parity
- why the role assignment was chosen
- whether the mismatch suggests:
  - bad assignment,
  - missing symbolic role,
  - or need for true signed-lift data

