#!/usr/bin/env python3
"""Dependency-free Tier-1 verifier for IVE problem-first architecture artifacts."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "rules" / "policy.json").read_text())

REQUIRED_TOP = {
    "schema_version", "problem", "causal_chain", "intervention_point", "prime_commercial_opportunity",
    "outcome_link", "venture", "requirements", "components", "evidence", "financial_model", "open_items",
}


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _missing_evidence(ids, evidence):
    return not ids or any(ref not in evidence for ref in ids)


def check(artifact):
    findings = []
    fail = lambda rule, detail: findings.append({"rule": rule, "status": "FAIL", "detail": detail})

    missing = sorted(REQUIRED_TOP - set(artifact))
    if missing:
        return [{"rule": "artifact-shape", "status": "FAIL", "detail": f"Missing fields: {', '.join(missing)}"}]
    if artifact["schema_version"] != POLICY["version"]:
        fail("schema-version", "Unsupported schema version.")

    evidence = {item.get("id"): item for item in artifact["evidence"]}
    component_ids = {item.get("id") for item in artifact["components"]}

    # Problem frame
    problem = artifact["problem"]
    if not _text(problem.get("statement")) or not _text(problem.get("who_bears_it")):
        fail("problem-frame", "Problem needs a statement and who bears it.")
    condition = problem.get("observable_condition") or {}
    if not _text(condition.get("statement")) or not _text(condition.get("metric")) or not _number(condition.get("baseline")):
        fail("problem-condition", "Observable condition needs a statement, a metric and a numeric baseline.")
    if condition.get("evidence_id") not in evidence:
        fail("problem-condition-evidence", "Observable condition baseline needs an existing evidence record.")
    outcome = problem.get("outcome_sought") or {}
    if not _text(outcome.get("statement")) or not _text(outcome.get("metric")) or not _number(outcome.get("target")) or not _text(outcome.get("by_date")):
        fail("outcome-sought", "Outcome sought needs a statement, a metric, a numeric target and a date.")

    # Causal chain and intervention point
    chain = artifact["causal_chain"]
    link_ids = set()
    if not chain:
        fail("causal-chain", "At least one causal link is required.")
    for link in chain:
        lid = link.get("id", "unidentified")
        link_ids.add(lid)
        if not _text(link.get("cause")) or not _text(link.get("effect")):
            fail("causal-link-completeness", f"{lid} needs a cause and an effect.")
        if _missing_evidence(link.get("evidence_ids", []), evidence):
            fail("causal-link-evidence", f"{lid} has missing evidence trace.")
    point = artifact["intervention_point"]
    if point.get("causal_link_id") not in link_ids:
        fail("intervention-point", "Intervention point must name an existing causal link.")
    if not _text(point.get("statement")) or not _text(point.get("why_here")):
        fail("intervention-point", "Intervention point needs a statement and a reason for choosing this link.")

    # Prime commercial opportunity
    pco = artifact["prime_commercial_opportunity"]
    for field in ("customer", "customer_observable_condition", "core_functionality", "payer"):
        if not _text(pco.get(field)):
            fail("pco-completeness", f"Prime commercial opportunity lacks {field}.")
    if pco.get("payer_relationship") not in {"same_as_bearer", "different_from_bearer", "mixed"}:
        fail("pco-payer-relationship", "payer_relationship must be same_as_bearer, different_from_bearer or mixed.")
    if pco.get("willingness_to_pay_evidence_id") not in evidence:
        fail("pco-willingness-to-pay", "Willingness to pay needs an existing evidence record.")

    # Outcome link
    outcome_link = artifact["outcome_link"]
    for field in ("mechanism", "scale_assumption", "arithmetic", "contribution_unit"):
        if not _text(outcome_link.get(field)):
            fail("outcome-link-completeness", f"Outcome link lacks {field}.")
    if not _number(outcome_link.get("contribution_to_target")):
        fail("outcome-link-contribution", "Outcome link needs a numeric contribution to the target.")
    if _missing_evidence(outcome_link.get("evidence_ids", []), evidence):
        fail("outcome-link-evidence", "Outcome link has missing evidence trace.")

    # Requirements
    if not artifact["requirements"]:
        fail("requirements", "At least one requirement is required.")
    for requirement in artifact["requirements"]:
        rid = requirement.get("id", "unidentified")
        for field in ("statement", "bottleneck", "intervention", "verification"):
            if not _text(requirement.get(field)):
                fail("requirement-completeness", f"{rid} lacks {field}.")
        if requirement.get("causal_link_id") not in link_ids:
            fail("requirement-causal-trace", f"{rid} does not name an existing causal link.")
        refs = requirement.get("component_ids", [])
        if not refs or any(ref not in component_ids for ref in refs):
            fail("component-trace", f"{rid} has missing component trace.")
        if _missing_evidence(requirement.get("evidence_ids", []), evidence):
            fail("evidence-trace", f"{rid} has missing evidence trace.")

    # Evidence
    for eid, record in evidence.items():
        if not record.get("source_or_test"):
            fail("evidence-provenance", f"{eid} lacks source or test.")
        if record.get("status") not in {"evidenced", "assumption"}:
            fail("evidence-status", f"{eid} has invalid status.")
        if record.get("status") == "assumption" and not record.get("falsification_test"):
            fail("assumption-test", f"{eid} needs a falsification test.")

    # Financial model
    model = artifact["financial_model"]
    try:
        price, cost, supplied = float(model["price_ceiling"]), float(model["cost_floor"]), float(model["fmos"])
        calculated = (price - cost) / cost
        if cost <= 0 or abs(calculated - supplied) > 0.001:
            fail("fmos-arithmetic", "FMOS calculation is invalid.")
        elif supplied < POLICY["minimum_fmos"]:
            fail("fmos-gate", f"FMOS {supplied:.1%} is below {POLICY['minimum_fmos']:.0%}.")
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        fail("fmos-arithmetic", "Financial model must contain valid numeric values.")

    for item in artifact["open_items"]:
        if item.get("status") == "resolved":
            fail("open-item-integrity", f"{item.get('id', 'open item')} is listed as resolved; remove it or use open/blocked.")

    if not findings:
        findings.append({"rule": "all-tier-1-checks", "status": "PASS", "detail": "All published mechanical checks passed."})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact")
    parser.add_argument("--report", default=None)
    args = parser.parse_args()
    findings = check(json.loads(Path(args.artifact).read_text()))
    verdict = "PASS" if all(row["status"] == "PASS" for row in findings) else "FAIL"
    report = {"policy_version": POLICY["version"], "verdict": verdict, "findings": findings,
              "scope": "Mechanical verification only; not proof that the problem will be fixed, not market validation, not expert sign-off."}
    rendered = json.dumps(report, indent=2) + "\n"
    if args.report:
        Path(args.report).write_text(rendered)
    print(rendered, end="")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
