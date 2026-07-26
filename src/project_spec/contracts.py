from __future__ import annotations

MANDATORY_SECTIONS = (
    "project_identity",
    "problem_and_value",
    "system_architecture",
    "state_contracts_and_invariants",
    "workflows_interfaces_and_repository",
    "roadmap_evaluation_and_metrics",
    "reliability_security_and_operations",
    "portfolio_and_employer_signal",
)

SEGMENT_FILES = {
    "project_identity": "00_project_identity.yaml",
    "problem_and_value": "01_problem_and_value.yaml",
    "system_architecture": "02_system_architecture.yaml",
    "state_contracts_and_invariants": "03_state_contracts_and_invariants.yaml",
    "workflows_interfaces_and_repository": "04_workflows_interfaces_and_repository.yaml",
    "roadmap_evaluation_and_metrics": "05_roadmap_evaluation_and_metrics.yaml",
    "reliability_security_and_operations": "06_reliability_security_and_operations.yaml",
    "portfolio_and_employer_signal": "07_portfolio_and_employer_signal.yaml",
}

ALLOWED_STATUSES = {
    "implemented", "partially_implemented", "documented", "planned", "deferred"
}
