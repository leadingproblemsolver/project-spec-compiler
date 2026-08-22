# Live role → proof target

The compiler can now accept a **live externally sourced role** as an evidence artifact and turn it into a bounded proof agenda.

The point is not resume keyword matching. It is to answer:

> What does this company actually require, what do we already have hard evidence for, and what is the smallest externally reviewed receipt that closes the highest-value gap?

## Contract

Input:

- company
- role
- source URL
- exact source excerpt
- normalized required capabilities chosen from the source
- existing evidence per capability
- desired next receipt per capability

Output:

- preserved source evidence
- each requirement marked `evidenced` or `missing_proof`
- missing proof ranked ahead of already-covered requirements
- next externally judged receipt

## Example use

For a deployed/applied-AI role, a source may demand:

- Python / JavaScript
- systems fundamentals
- multi-step agent workflows
- orchestration and failure handling
- customer POCs / technical evaluations
- evals / observability / guardrails
- cloud and container operation

Existing SignalOps receipts can cover some policy/state/provenance/testing requirements. Missing production operation, real customer POC, observability, or externally reviewed open-source work should become **build targets**, not claims.

## Boundary

The role description is evidence from an external market actor. The normalized capability labels are interpretation. They remain separate.

This module does not determine candidate eligibility, invent experience, generate a resume, or claim that a project satisfies a requirement without an explicit receipt.
