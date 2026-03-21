# Systematic Symbolic Break Search Note

## Checkpoint

The provisional symbolic bridge evaluator has passed the first manual stress-test rows.

So the next step is no longer to add a few more hand-chosen examples.
It is to search systematically over short local words.

## Goal

Enumerate short route words and compare:

- local `lift_bit`
- provisional symbolic parity assignment

Then record the first mismatch, if one appears.

## Why this is the right next move

A bridge rule that survives only curated rows is weak.
A bridge rule that survives a systematic short-word sweep is much stronger.

If it fails, the failure will tell us exactly where the current symbolic vocabulary stops being natural.

If it does not fail on short words, then the symbolic bridge model has earned a higher level of trust.

