# ADR 0001: Segments are authoritative; bundles are compiled

## Decision
The eight section files are the authoring surface. `project.bundle.yaml` is deterministic compiled output.

## Why
Allowing both to be edited creates two sources of truth and permits silent divergence.

## Alternative
Treat the bundle as canonical and split it for readability. Rejected because section-level ownership and review are clearer in the supplied structure.
