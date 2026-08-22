from __future__ import annotations

import unittest

from project_spec.role_target import compile_role_target, next_proof_actions


class RoleTargetTests(unittest.TestCase):
    def test_missing_proof_is_ranked_before_existing_evidence(self) -> None:
        target = compile_role_target(
            company="Example AI",
            role="Deployed Engineer",
            source_url="https://example.com/jobs/1",
            exact_source_excerpt="Build production agents and own customer POCs.",
            required_capabilities=["agent_workflows", "customer_poc", "python"],
            evidence_by_capability={
                "agent_workflows": ["multi-step workflow repo"],
                "python": ["tested Python policy engine"],
            },
            receipt_by_capability={
                "customer_poc": "Run one live technical POC with an external operator.",
            },
        )
        actions = next_proof_actions(target)
        self.assertEqual(actions[0]["requirement"], "customer_poc")
        self.assertEqual(actions[0]["gap"], "missing_proof")

    def test_source_evidence_is_preserved_separately(self) -> None:
        excerpt = "Strong Python and systems fundamentals."
        target = compile_role_target(
            company="Example AI",
            role="Engineer",
            source_url="https://example.com/jobs/2",
            exact_source_excerpt=excerpt,
            required_capabilities=["python"],
            evidence_by_capability={},
            receipt_by_capability={},
        )
        self.assertEqual(target.exact_source_excerpt, excerpt)
        self.assertEqual(target.requirements[0].gap, "missing_proof")


if __name__ == "__main__":
    unittest.main()
