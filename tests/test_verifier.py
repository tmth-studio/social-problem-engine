import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "verifier"))
from verify import check


def rules(findings):
    return {item["rule"] for item in findings}


class VerifierTests(unittest.TestCase):
    def setUp(self):
        fixture = Path(__file__).resolve().parents[1] / "examples" / "housing-cost" / "architecture.json"
        self.artifact = json.loads(fixture.read_text())

    def test_passing_fixture(self):
        self.assertTrue(all(item["status"] == "PASS" for item in check(self.artifact)))

    def test_rejects_missing_baseline_evidence(self):
        bad = copy.deepcopy(self.artifact)
        bad["problem"]["observable_condition"]["evidence_id"] = "MISSING"
        self.assertIn("problem-condition-evidence", rules(check(bad)))

    def test_rejects_non_numeric_target(self):
        bad = copy.deepcopy(self.artifact)
        bad["problem"]["outcome_sought"]["target"] = "lower"
        self.assertIn("outcome-sought", rules(check(bad)))

    def test_rejects_empty_causal_chain(self):
        bad = copy.deepcopy(self.artifact)
        bad["causal_chain"] = []
        found = rules(check(bad))
        self.assertIn("causal-chain", found)
        self.assertIn("intervention-point", found)

    def test_rejects_intervention_point_off_chain(self):
        bad = copy.deepcopy(self.artifact)
        bad["intervention_point"]["causal_link_id"] = "L9"
        self.assertIn("intervention-point", rules(check(bad)))

    def test_rejects_bad_payer_relationship(self):
        bad = copy.deepcopy(self.artifact)
        bad["prime_commercial_opportunity"]["payer_relationship"] = "unknown"
        self.assertIn("pco-payer-relationship", rules(check(bad)))

    def test_rejects_outcome_link_without_number(self):
        bad = copy.deepcopy(self.artifact)
        bad["outcome_link"]["contribution_to_target"] = "small"
        self.assertIn("outcome-link-contribution", rules(check(bad)))

    def test_rejects_requirement_without_causal_link(self):
        bad = copy.deepcopy(self.artifact)
        bad["requirements"][0]["causal_link_id"] = "L9"
        self.assertIn("requirement-causal-trace", rules(check(bad)))

    def test_rejects_bad_trace(self):
        bad = copy.deepcopy(self.artifact)
        bad["requirements"][0]["component_ids"] = ["MISSING"]
        self.assertIn("component-trace", rules(check(bad)))

    def test_rejects_assumption_without_test(self):
        bad = copy.deepcopy(self.artifact)
        del bad["evidence"][0]["falsification_test"]
        self.assertIn("assumption-test", rules(check(bad)))

    def test_rejects_weak_margin(self):
        bad = copy.deepcopy(self.artifact)
        bad["financial_model"] = {"price_ceiling": 33000, "cost_floor": 30000, "fmos": 0.1}
        self.assertIn("fmos-gate", rules(check(bad)))

    def test_rejects_resolved_open_item(self):
        bad = copy.deepcopy(self.artifact)
        bad["open_items"][0]["status"] = "resolved"
        self.assertIn("open-item-integrity", rules(check(bad)))


if __name__ == "__main__":
    unittest.main()
