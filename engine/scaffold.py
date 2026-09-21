#!/usr/bin/env python3
"""Create a deliberately incomplete architecture package from a valid problem brief."""
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: scaffold.py INPUT.json OUTPUT.json", file=sys.stderr)
        return 2
    source = json.loads(Path(sys.argv[1]).read_text())
    condition = dict(source["observable_condition"])
    condition["evidence_id"] = "E-BASELINE"
    artifact = {
        "schema_version": "0.2",
        "problem": {
            "statement": source["problem"],
            "who_bears_it": source["who_bears_it"],
            "observable_condition": condition,
            "outcome_sought": source["outcome_sought"],
        },
        "causal_chain": [],
        "intervention_point": {"causal_link_id": None, "statement": None, "why_here": None},
        "prime_commercial_opportunity": {
            "customer": None, "customer_observable_condition": None, "core_functionality": None,
            "payer": None, "payer_relationship": None, "willingness_to_pay_evidence_id": None,
        },
        "outcome_link": {"mechanism": None, "scale_assumption": None, "contribution_to_target": None,
                         "contribution_unit": None, "arithmetic": None, "evidence_ids": []},
        "venture": None,
        "requirements": [],
        "components": [],
        "evidence": [{
            "id": "E-BASELINE",
            "claim": condition["statement"],
            "status": "evidenced" if condition.get("source") and condition["source"] != "assumption" else "assumption",
            "source_or_test": condition.get("source") or "Name the source or the test that would falsify the baseline.",
        }] + source.get("evidence", []),
        "financial_model": {"price_ceiling": None, "cost_floor": None, "fmos": None},
        "open_items": [
            {"id": "OPEN-1", "statement": "Complete the causal chain, intervention point, prime commercial opportunity, outcome link, requirements, components and financial model.", "status": "open"}
        ],
    }
    Path(sys.argv[2]).write_text(json.dumps(artifact, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
