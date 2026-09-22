> **Superseded — 22 September 2026.** This prototype was made with Codex on 21 September 2026 and is not the method. It has a six-line prompt, five rules and a script that checks the shape of one data file. The full method — the ten requirements, the design loop, the gate criteria, the verifier and the checking tools — is public at **[tmth-studio/forge-cf](https://github.com/tmth-studio/forge-cf)**. Use that. This repository stays only so old links still land somewhere.

# Problem-first architecture engine — prototype

**Go from social problem to profitable business solution.**

An experimental, portable method. It turns a stated social problem — the cost of housing, say — into an auditable venture architecture. It then checks that architecture against explicit published rules. It is the problem-first version of the [IVE Architecture Engine](https://github.com/tmth-studio/ive-architecture-engine), which starts one step later, from a venture brief.

## What is different

The venture brief is derived, not supplied. Five stages sit in front of it, and each one is checked:

1. **Problem frame** — who bears the problem, what you can measure today (with a baseline figure), and what "fixed" means (a target and a date).
2. **Causal chain** — why the condition persists, link by link, back to the first cause a private venture could change.
3. **Intervention point** — the one link the venture acts on, and why that one.
4. **Prime commercial opportunity** — the customer, what they would pay for, and who pays. It also records whether the payer is the person who bears the problem or someone else.
5. **Outcome link** — how the venture at scale moves the outcome metric, with the arithmetic and a number. A small number is allowed. A missing one is not.

Then the architecture continues as in the original: requirements, components, evidence, financial model, open items. Every requirement also names the causal link it acts on.

The method behind stages 4 onward is IVE (Simanis et al., 2021, and the co-authored papers 2023–2025). Stages 1 to 3 are the bridge from a social problem to the point where IVE starts. See `docs/problem-to-venture.md`.

## Status

**Prototype — not WS1-qualified.** This repository does not claim that an LLM can reliably create a venture that fixes a social problem, or a commercially validated architecture. Here, **verified** means: *the supplied artifact passed the versioned, mechanical checks in this repository*. Whether the causal chain is true, the intervention point is right, the customer exists or the outcome arithmetic holds remains separate human work.

## What you can do with this

1. Write your problem as JSON following `schemas/problem-input.schema.json`. `examples/housing-cost/input.json` is a worked example.
2. Give your LLM `prompts/system.md` and your input file.
3. Ask it to return a JSON architecture artifact following `schemas/architecture.schema.json`.
4. Save that output as `architecture.json`.
5. Run `python3 verifier/verify.py architecture.json`.

The verifier writes a report and exits non-zero when a hard rule fails. An LLM must not change `rules/` or `verifier/` for its own output to be called verified.

```bash
python3 verifier/verify.py examples/housing-cost/architecture.json
python3 verifier/verify.py architecture.json --report verification-report.json
python3 engine/scaffold.py examples/housing-cost/input.json architecture.json
python3 -m unittest discover -s tests
```

## The worked example

`examples/housing-cost/` starts from "the cost of housing in London is too high for people on ordinary incomes". It goes through all five stages to a synthetic venture, InfillWorks. InfillWorks sells small builders a standard, borough-accepted route to consent on small sites. The outcome link shows its arithmetic: at 3,000 extra homes a year for ten years it closes about a tenth of the gap to target. That is recorded as an open item, not hidden. Every figure in the example is a placeholder marked as an assumption with the test that would replace it.

## Repository map

- `schemas/` — problem input and architecture artifact contracts.
- `prompts/` — portable instructions to give a generator LLM.
- `rules/` — the versioned verification policy.
- `engine/` — a small local scaffold that turns a problem input into an empty architecture package.
- `verifier/` — independent deterministic checks.
- `examples/` — a synthetic, non-confidential worked example and a passing artifact.
- `docs/` — how the problem-first stages work, and what the verifier does not check.

## Non-negotiable boundaries

- A generator and verifier are separate roles.
- Every material claim carries evidence or is flagged as an assumption with a test.
- Every requirement traces to a causal link, a bottleneck, an intervention, components and evidence.
- The outcome link states a number and shows its arithmetic, however small the number.
- A passing mechanical report is not a claim that the problem will be fixed.
- Do not upload personal data, client data, credentials, paid-source text, or private Forge records.

## License

MIT. See `LICENSE`.
