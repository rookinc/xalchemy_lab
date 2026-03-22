# Sprint Canonical Model

## Canonical floor

This sprint reduces to the following formal stack:

- spark
- kernel
- grammar

## Definitions

### Spark
A spark is the minimal perturbation primitive of the model.

It is the smallest event sufficient to:

- localize an initial active site
- orient the centroid
- seed the first propagation grammar state

### Kernel
The kernel is the transition:

- `r0 -> r1`

It is the unique nontrivial step in which a raw perturbation becomes a reconciled centroid-oriented initial state.

### Trurtle
The trurtle is the ordered triadic frame:

- `xyz`

Order matters before reconciliation.

### Lift+twist
Lift+twist is the half-step reconciliation operator.

It acts on the ordered trurtle frame `xyz` and produces the identification state `I`.

### Identification state
- `I`

is the first identified intermediate state produced by reconciliation.

### r1
The resolved state is:

- `r1 = (localized_site, centroid_orientation, reconciliation_state, initial_grammar_state)`

This is the reconciled centroid-oriented initial state.

### Grammar
After `r1`, propagation is mostly grammar.

## Strongest sentences

A spark is the minimal perturbation primitive.

The kernel is the map from raw perturbation to reconciled centroid-oriented initial state.

After `r1`, propagation is mostly grammar.

