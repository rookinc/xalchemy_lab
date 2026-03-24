PIRALIZER_PAPER_BOOT_NOTE.md

## Working title
A combinatorial descent framework for predicting graph ladders from local transition structure

## Purpose
This is a new standalone paper.
It is not a revision of the dodecahedral transport / L(Petersen) paper.
That older paper is now a bridge and precedent, not the main object here.

The goal of this paper is to define the general descent framework that may predict which graphs appear in a coherent ladder such as

G900 -> ... -> G60 -> G30 -> G15 -> G0

without assuming in advance that the ladder is merely a list of unrelated graph constructions.

## Core intuition
The working idea is that the graphs in the ladder are realizations of a common combinatorial regime.

Local transition structure generates candidate organization.
Admissibility determines which transitions endure.
Descent through quotient/coherence maps reveals the coarse laws induced by the finer carrier.

Internal north-pole language:

- informative action explores
- admissible action endures
- coherence reveals
- the truth sticks

Journal-facing translations:

- informative action = local transition rule or local update rule
- admissible action = admissible transition or lawful transition
- coherence = controlled identification / persistent structure / descent coherence
- carrier = transition graph / state graph / supporting graph

Avoid using "spiralizer" in the abstract or formal theorem statements.
It can survive as private scaffolding or notebook language.

## Current central hypothesis
The ladder is governed by a shared regime rather than by isolated graph objects.

The present model suggests a centered two-sheet three-channel carrier with:
- top branch weight = 140
- center / rung weight = 145
- bottom branch weight = 150

with centered offsets:
- 140 -> -5
- 145 -> 0
- 150 -> +5

The coarse triangular law is obtained by coherent identification of the two off-center branch classes:

140 + 150 = 290

so the first coarse triangle has uniform edge law:
- AB = 290
- BC = 290
- CA = 290

The vertical/rung edges are structurally essential upstairs but do not survive as extra edge terms downstairs; under the coarse triangle quotient they collapse into vertex identification.

## Parity refinement
Later notes indicate that the same coarse law admits a parity refinement.

Coarse:
- 290

Parity-refined decomposition:
- 160 + 130 = 290

So the coarse contact law is stable under parity splitting.

Important distinction:
- the coarse side-contribution question is resolved
- the fully refined edge-by-edge parity bookkeeping may remain partially open

## Main mathematical question
How can one define a general descent framework that predicts which graphs may appear in a coherent ladder?

Equivalent formulation:
Which carriers remain compatible with the same admissible descent pattern, and therefore qualify as members of the same structural family?

## Proposed framing
The key object is not a single graph, but a refinement-quotient family equipped with persistent local transition structure.

The program should distinguish:

1. local transition grammar
2. admissibility rule
3. supporting carrier
4. quotient / coherence maps
5. coarse induced laws
6. prediction criteria for allowable ladder members

## Discrete-math-facing abstract seed
We introduce a combinatorial descent framework for finite graph families related by refinement and quotient operations. The main idea is that a graph ladder may be governed by a common local transition law whose induced structures persist across scales. Starting from a local transition grammar, one forms admissible carriers by retaining only lawful transitions, and then studies the quotient graphs obtained by controlled identification of these carriers. The resulting quotients encode coarse laws that are induced by the finer combinatorial organization.

Our motivating case is a family with centered two-sheet, three-channel support and an associated triangular quotient law. The fine-level branch and parity distinctions are not discarded arbitrarily under descent, but combine in a structured way to produce stable coarse behavior. This suggests that the relevant object is not an individual graph in isolation, but an entire refinement-quotient family equipped with a persistent descent pattern.

From this perspective, the problem is predictive as well as descriptive: determine which graphs can occur in a common ladder by testing compatibility with the same admissible descent law. The framework is proposed as a method for identifying structural invariants of such families and for forecasting further members of a finite graph sequence.

## Immediate paper tasks
1. define the primitive objects
   - graph ladder
      - local transition grammar
         - admissible carrier
            - descent/coherence map
               - coarse law

               2. decide the formal status of the regime
                  - example
                     - conjectural template
                        - theorem schema
                           - algorithmic criterion

                           3. define the centered prism regime precisely
                              - two-sheet three-channel support
                                 - top/center/bottom weights
                                    - triangle coherence law
                                       - parity refinement

                                       4. state the prediction problem clearly
                                          - not classification after the fact
                                             - prediction of allowable ladder members

                                             5. separate bridge material from standalone material
                                                - old dodecahedral transport paper = motivating precedent only
                                                   - new paper = general framework

                                                   ## Good candidate section outline
                                                   1. Introduction
                                                   2. Graph ladders and local transition structure
                                                   3. Admissible carriers and controlled identifications
                                                   4. Centered two-sheet three-channel regime
                                                   5. Coarse triangular law and parity refinement
                                                   6. Predictive formulation of the ladder problem
                                                   7. Examples, conjectures, and open directions

                                                   ## Tone guidance
                                                   Keep the paper rigorous, sparse, and combinatorial.
                                                   Do not lean on project-native mythology in the main prose.
                                                   Use words like:
                                                   - refinement
                                                   - quotient
                                                   - admissibility
                                                   - support
                                                   - induced law
                                                   - persistent structure
                                                   - compatibility
                                                   - prediction
                                                   - family
                                                   - ladder

                                                   Minimize words like:
                                                   - spiralizer
                                                   - reveal
                                                   - truth sticks
                                                   - informative action
                                                   - admissible action

                                                   Those can remain in private notes only.

                                                   ## One-sentence paper thesis
                                                   A graph ladder should be studied as a refinement-quotient family governed by a persistent local transition law, and the main prediction problem is to determine which graphs remain compatible with that law under admissible descent.
