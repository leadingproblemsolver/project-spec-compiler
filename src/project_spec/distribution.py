"""Role-proof target -> Clay/SignalOps distribution packet.

This module does not find contacts or tailor a resume. It converts an already compiled
role proof target into an explicit hiring-market routing packet once the operator supplies
(1) the company identifier Clay should search, (2) the observer titles to look for, and
(3) the exact proof artifacts to expose.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Mapping, Sequence

from .role_target import RoleProofTarget


def _tuple(values: Sequence[str]) -> tuple[str, ...]:
    return tuple(str(value).strip() for value in values if str(value).strip())


@dataclass(frozen=True, slots=True)
class RoleDistributionPacket:
    company: str
    role: str
    role_source_url: str
    company_identifier: str
    observer_titles: tuple[str, ...]
    proof_artifacts: tuple[tuple[str, str], ...]
    evidenced_capabilities: tuple[str, ...]
    missing_proof: tuple[str, ...]

    @property
    def packet_key(self) -> str:
        canonical = json.dumps(asdict(self), separators=(",", ":"), sort_keys=True)
        return sha256(canonical.encode("utf-8")).hexdigest()[:24]

    def clay_contact_search(self) -> dict[str, object]:
        return {
            "companyIdentifiers": [self.company_identifier],
            "contactFilters": {"job_title_keywords": list(self.observer_titles)},
        }


def compile_role_distribution_packet(
    target: RoleProofTarget,
    *,
    company_identifier: str,
    observer_titles: Sequence[str],
    proof_artifacts: Mapping[str, str],
) -> RoleDistributionPacket:
    """Create a deterministic contact-search packet without inventing proof or observers."""

    identifier = company_identifier.strip()
    observers = _tuple(observer_titles)
    artifacts = tuple(
        sorted(
            (str(label).strip(), str(url).strip())
            for label, url in proof_artifacts.items()
            if str(label).strip() and str(url).strip()
        )
    )
    if not identifier:
        raise ValueError("company_identifier is required")
    if not observers:
        raise ValueError("at least one observer title is required")
    if not artifacts:
        raise ValueError("at least one externally inspectable proof artifact is required")

    evidenced = tuple(
        item.requirement for item in target.requirements if item.gap == "evidenced"
    )
    missing = tuple(
        item.requirement for item in target.requirements if item.gap == "missing_proof"
    )
    return RoleDistributionPacket(
        company=target.company,
        role=target.role,
        role_source_url=target.source_url,
        company_identifier=identifier,
        observer_titles=observers,
        proof_artifacts=artifacts,
        evidenced_capabilities=evidenced,
        missing_proof=missing,
    )
