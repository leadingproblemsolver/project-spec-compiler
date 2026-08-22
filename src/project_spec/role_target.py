"""Compile employer/role evidence into a bounded proof-target artifact.

This module does not tailor prose for a resume. It turns a live role description into a
machine-readable engineering agenda: requirement -> current receipt -> proof gap -> smallest
externally judged next receipt.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True, slots=True)
class RoleRequirement:
    requirement: str
    evidence: tuple[str, ...]
    gap: str
    next_receipt: str
    priority: int


@dataclass(frozen=True, slots=True)
class RoleProofTarget:
    company: str
    role: str
    source_url: str
    exact_source_excerpt: str
    requirements: tuple[RoleRequirement, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def compile_role_target(
    *,
    company: str,
    role: str,
    source_url: str,
    exact_source_excerpt: str,
    required_capabilities: Sequence[str],
    evidence_by_capability: Mapping[str, Sequence[str]],
    receipt_by_capability: Mapping[str, str],
) -> RoleProofTarget:
    """Compile explicit capability labels supplied from a live role description.

    Inputs remain operator-controlled so the compiler never pretends a fuzzy parser has proven
    what a company requires. The source excerpt is preserved separately from the normalized
    capability labels.
    """
    if not company.strip() or not role.strip() or not source_url.strip() or not exact_source_excerpt.strip():
        raise ValueError("company, role, source_url and exact_source_excerpt are required")

    requirements: list[RoleRequirement] = []
    for index, raw in enumerate(required_capabilities):
        capability = str(raw).strip()
        if not capability:
            continue
        evidence = tuple(
            str(item).strip()
            for item in evidence_by_capability.get(capability, ())
            if str(item).strip()
        )
        if evidence:
            gap = "evidenced"
            next_receipt = receipt_by_capability.get(
                capability,
                "Only strengthen if a higher proof rung is cheap and externally useful.",
            )
            priority = 2
        else:
            gap = "missing_proof"
            next_receipt = receipt_by_capability.get(
                capability,
                "Create the smallest externally reviewed artifact that proves this capability.",
            )
            priority = 10 - min(index, 8)
        requirements.append(RoleRequirement(capability, evidence, gap, next_receipt, priority))

    requirements.sort(key=lambda item: (item.gap != "missing_proof", -item.priority, item.requirement))
    return RoleProofTarget(
        company=company.strip(),
        role=role.strip(),
        source_url=source_url.strip(),
        exact_source_excerpt=exact_source_excerpt.strip(),
        requirements=tuple(requirements),
    )


def next_proof_actions(target: RoleProofTarget, limit: int = 3) -> list[dict[str, object]]:
    missing = [item for item in target.requirements if item.gap == "missing_proof"]
    return [asdict(item) for item in missing[: max(0, limit)]]
