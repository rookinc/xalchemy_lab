# Framed Return Probe Result

## Result

Several loops were tested for framed return behavior.

### A, B, C loops
These loops shared the same physical trace:

- e_right
- e_left
- e_right

But they had different chart traces:

- return_A: chart_right, chart_left, chart_right
- return_B: chart_left, chart_right, chart_left
- return_C: chart_right, chart_right, chart_right

Despite these differences, all three had:

- initial_frame = final_frame
- return_class = same

### D loop
This loop produced a different pattern:

- physical_trace = e_right, e_right, e_left
- chart_trace = chart_right, chart_left, chart_left
- initial_frame = chart_right
- final_frame = chart_left
- return_class = reversed

## Strongest conclusion

Chart trace carries finer framed information than return class.

Different framed traces may belong to the same closure class, while some loops produce a genuinely reversed framed return.

## Strongest sentence

The current runtime exhibits a two-level framed structure: chart traces distinguish local framed histories, while return classes distinguish coarser closure behavior.

## Interpretation

This strengthens the claim that the transport law has a genuine framed return structure and is not exhausted by raw physical exits.

## Next step

Refine the return classifier so it is defined from a more principled framed quantity than only the first and last chart symbol.

