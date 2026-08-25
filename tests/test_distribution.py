from __future__ import annotations

import pytest

from project_spec.distribution import compile_role_distribution_packet
from project_spec.role_target import compile_role_target


def _target():
    return compile_role_target(
        company="Example AI",
        role="Product & GTM Intern",
        source_url="https://example.com/jobs/gtm",
        exact_source_excerpt="Build workflows, talk to customers, and ship experiments.",
        required_capabilities=["workflow implementation", "customer discovery", "SQL"],
        evidence_by_capability={
            "workflow implementation": ["SignalOps workflow receipt"],
            "customer discovery": ["operator outreach receipt"],
        },
        receipt_by_capability={"SQL": "Complete an externally judged SQL exercise."},
    )


def test_compiles_clay_contact_search_and_preserves_proof_state() -> None:
    packet = compile_role_distribution_packet(
        _target(),
        company_identifier="example.com",
        observer_titles=["Founder", "Head of GTM"],
        proof_artifacts={
            "SignalOps": "https://github.com/leadingproblemsolver/signalops-workbench",
            "Target Spec": "https://github.com/leadingproblemsolver/project-spec-compiler",
        },
    )

    assert packet.clay_contact_search() == {
        "companyIdentifiers": ["example.com"],
        "contactFilters": {"job_title_keywords": ["Founder", "Head of GTM"]},
    }
    assert packet.evidenced_capabilities == ("workflow implementation", "customer discovery")
    assert packet.missing_proof == ("SQL",)


def test_packet_key_is_stable() -> None:
    kwargs = dict(
        company_identifier="example.com",
        observer_titles=["Founder"],
        proof_artifacts={"Proof": "https://example.com/proof"},
    )
    assert compile_role_distribution_packet(_target(), **kwargs).packet_key == compile_role_distribution_packet(_target(), **kwargs).packet_key


def test_requires_real_observer_and_proof_artifact() -> None:
    with pytest.raises(ValueError, match="observer title"):
        compile_role_distribution_packet(
            _target(),
            company_identifier="example.com",
            observer_titles=[],
            proof_artifacts={"Proof": "https://example.com/proof"},
        )
    with pytest.raises(ValueError, match="proof artifact"):
        compile_role_distribution_packet(
            _target(),
            company_identifier="example.com",
            observer_titles=["Founder"],
            proof_artifacts={},
        )
