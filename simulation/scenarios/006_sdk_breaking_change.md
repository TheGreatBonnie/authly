# Scenario 006 — SDK breaking change

## Change

Rename a public SDK method.

Example:

Old:

`authly.permissions.check()`

New:

`authly.permissions.evaluate()`

## Intentional drift

Leave old examples in the docs.

## Expected behavior

Draftly should locate references across:

- docs/
- examples/
- README.md
- tests/
