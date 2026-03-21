# Candidate G60 Packet Schema v1

## Goal

Propose the smallest upstairs transport structure on `G60` that could descend to the current local normal form.

This is not yet asserted to be true.
It is the first minimal candidate schema that could pass the local `G60` interface test.

---

## Candidate schema

A minimal local `G60` packet should contain four components:

1. **one anchor chamber packet**
2. **one odd exchange branch**
3. **two sibling continuation sheets**
4. **one rigid distal skeleton**

Symbolically:

\[
\mathcal P_{60}
=
\mathcal H
\;\cup\;
\mathcal O
\;\cup\;
\mathcal E_1
\;\cup\;
\mathcal E_2
\;\cup\;
\mathcal K_{\mathrm{distal}}.
\]

where:

- \(\mathcal H\) = anchor chamber packet
- \(\mathcal O\) = odd exchange branch
- \(\mathcal E_1\) = continuation sheet 1
- \(\mathcal E_2\) = continuation sheet 2
- \(\mathcal K_{\mathrm{distal}}\) = rigid distal skeleton

---

## 1. Anchor chamber packet

The anchor packet \(\mathcal H\) is the upstairs object whose local receipt supports the anchored control surface.

It must permit three local control actions:

- odd exchange activation,
- \(E1\)-sheet activation,
- anchored sheet-polarity swapping.

So \(\mathcal H\) must carry at least one chamber-level control slot that can couple differently to:

- the odd exchange branch,
- continuation sheet \(E1\),
- continuation sheet \(E2\).

This is the upstairs source of the local controls:
- \(\tau\)
- \(\sigma\)
- \(A\)

---

## 2. Odd exchange branch

The odd branch \(\mathcal O\) is the upstairs source of the local odd exchange mode.

Its local receipt must account for:

- the anchored odd generator
  \[
  (A,O,O,O),
  \]
- the persistence of odd-side branch structure away from the anchor,
- the existence of mixed branch/sheet traces.

So \(\mathcal O\) must be a genuine branch, not merely a bit-label.

---

## 3. Two sibling continuation sheets

The continuation sheets \(\mathcal E_1,\mathcal E_2\) are the upstairs source of the local even propagation structure.

They must descend to:

- the two anchored even arms,
- the \(E1\)-activation behavior,
- the \(E2\)-sheet polarity behavior,
- the mixed even-sheet continuation traces.

So the upstairs model must distinguish these two sheets, even if later quotients collapse them partially.

---

## 4. Rigid distal skeleton

The rigid distal skeleton \(\mathcal K_{\mathrm{distal}}\) is the upstairs source of the parity-stable distal trace classes.

It must descend to the current rigid odd/even backbone:

### Rigid odd backbone
- \((D,E1,E1,E2)\)
- \((D,E1,E1,M+)\)
- \((D,E1,E2,E2)\)
- \((E2,E2,E2,E2)\)

### Rigid even backbone
- \((D,E1,O,M+)\)
- \((E1,E1,M+,M+)\)
- \((E1,E2,E2,E2)\)
- \((E1,E2,M+,M+)\)
- \((E1,M+,M+,O)\)
- \((E2,E2,E2,O)\)

This component should remain stable under the nearby local controls descending to \((A,\sigma,\tau)\).

---

## Local descent dictionary

The current local receipt dictionary is:

- \(\mathcal H \rightsquigarrow\) anchor traces involving `A`
- \(\mathcal O \rightsquigarrow\) odd-branch traces involving `O`
- \(\mathcal E_1 \rightsquigarrow\) sheet-1 traces involving `E1`
- \(\mathcal E_2 \rightsquigarrow\) sheet-2 traces involving `E2`
- \(\mathcal K_{\mathrm{distal}} \rightsquigarrow\) distal `D/M+` backbone structure

This is only a receipt dictionary, not yet a proof of correspondence.

---

## Minimal pass conditions

A candidate upstairs `G60` packet schema passes the current local interface only if:

### Control packet descent
It reproduces:
- \(\tau\): anchor odd exchange activation
- \(\sigma\): \(E1\)-sheet activation
- \(A\): anchored polarity swap + odd rearm

### Skeleton descent
It preserves:
- the rigid odd backbone
- the rigid even backbone

under those nearby local controls.

---

## Strongest current reading

The smallest plausible upstairs object is not just a graph.
It is a packet-and-skeleton transport structure:

- one anchor packet,
- one odd exchange branch,
- two sibling continuation sheets,
- one rigid distal skeleton.

Any viable `G60` model must contain at least this much structure in order to descend to the local law already established.

