# Bridge Language Upgrade Note

## Reason for upgrade

The actual-edge search has now shown that the square sector is not a single privileged loop.

Instead, the local lift-derived geometry contains:

- a family of even 4-cycles
- a smaller family of odd 4-cycles

So the bridge language should be upgraded from single-loop terminology to family terminology.

## Old language

Old wording suggested:

- `global_square` = one specific square loop
- `global_twist` = one specific twist loop

That was acceptable during the symbolic seed stage,
but it is no longer the best geometric description.

## New language

### Square-type class
A square-type representative is any actual 4-cycle in the even local family.

So `global_square` should now be read as:

- a chosen representative of the even 4-cycle class

not:

- the one true square loop

### Twist-type class
A twist-type representative is any loop or comparison class in the odd sector.

So `global_twist` should now be read as:

- a chosen representative of the odd class

not:

- the one true odd loop

## Bridge reading after upgrade

Current best bridge statement:

- return-type is even
- square-type belongs to the even 4-cycle family
- twist-type belongs to the odd class

This is the stronger formulation because it matches the actual-edge search.

