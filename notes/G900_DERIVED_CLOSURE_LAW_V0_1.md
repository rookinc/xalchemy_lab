# G900 Derived Closure Law v0.1

## Status
Derivation note.

## Starting data
Use the centered preimage family

- (I - d, I, I + d)

with the current exported instance

- I = 145
- d = 5
- L = 10

so that the extracted band is

- (140, 145, 150).

## Step 1: midpoint law
From the centered form,

- (I - d) + (I + d) = 2I

so the middle value is the midpoint:

- I = ((I - d) + (I + d)) / 2.

In the current instance:

- 145 = (140 + 150) / 2.

## Step 2: quotient image
Under the current quotient reading, the paired face values recombine to the quotient image:

- Q(I) candidate = (I - d) + (I + d) = 2I.

So the core quotient law is:

- Q(I) = 2I.

In the current instance:

- 140 + 150 = 290 = 2 * 145.

## Step 3: extension parameter disappears from the image
The quantity d cancels in

- (I - d) + (I + d) = 2I.

So the quotient image is insensitive to the offset magnitude.
This separates the package into:

- core data: I and Q(I) = 2I
- extension data: d

## Step 4: exported band law
The current export records the normalized offsets

- (-5, 0, +5)

so that

- d = 5.

The same export gives

- L = 10.

Hence, in the present export,

- d = L / 2.

So the centered family can be rewritten as

- (I - L/2, I, I + L/2).

For the current instance:

- (145 - 10/2, 145, 145 + 10/2)
- (140, 145, 150).

## Step 5: derived closure law
Combining the quotient reading with the exported band law gives:

- (I - L/2, I, I + L/2) -> Q(I) = 2I.

This is the strongest compact closure statement currently supported by the checked package.

## Current instantiated case
With

- I = 145
- L = 10

the band is

- (140, 145, 150)

and the quotient image is

- Q(145) = 290.

## What is actually derived
The current package supports:

- midpoint law
- doubled-center law
- quotient image Q(I) = 2I
- insensitivity of the quotient image to d
- export-level band law d = L / 2

## What is not yet derived structurally
Still open:

- why the carrier produces L = 10
- why the export normalization must choose d = L / 2
- whether side-contribution semantics are zero, bookkeeping-only, or normalized away

## Honest conclusion
The current G900 package supports the derived closure law

- (I - L/2, I, I + L/2) -> Q(I) = 2I

at the export-and-checker level.

For the present instance:

- (140, 145, 150) -> 290.

