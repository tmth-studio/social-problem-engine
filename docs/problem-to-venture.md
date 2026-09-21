# From a social problem to a venture

The original architecture engine starts from a venture brief: a named venture, its core functionality, its customer and that customer's observable condition. This version starts one step earlier, from a social problem that someone wants to see fixed, and derives the venture brief from it.

## Why the extra step

A social problem is not a commercial opportunity. "The cost of housing is too high" names a harm and the people who carry it. It does not name a customer, what that customer would pay for, or why paying would change the harm. The method in IVE (Simanis et al., 2021 and later papers) begins at the prime commercial opportunity: a customer with an observable condition. This engine adds the stages that get from the problem to that opportunity, and it makes each stage checkable.

## The five stages before the venture brief

| Stage | What it produces | What the verifier checks |
|---|---|---|
| Problem frame | The problem, who bears it, an observable condition with a baseline figure, and an outcome sought with a target and a date | Baseline is a number with an evidence record; target is a number with a date |
| Causal chain | Ordered links from the condition back to its causes, each with evidence | At least one link; every link has cause, effect and existing evidence |
| Intervention point | The one link the venture acts on, and why that one | Names an existing link; gives a reason |
| Prime commercial opportunity | Customer, the customer's observable condition, core functionality, payer, payer's relationship to the people who bear the problem, willingness-to-pay evidence | All fields present; payer relationship is one of three values; evidence exists |
| Outcome link | The mechanism by which the venture at scale moves the outcome metric, the scale assumption, the arithmetic and the numeric contribution | All present; contribution is a number; evidence exists |

After these stages the artifact continues as before: requirements, components, evidence, financial model and open items. One addition: every requirement names the causal link it acts on.

## The payer question

The people who bear a social problem are often not the people who can pay to fix it. Renters bear high housing costs; a developer pays for a cheaper route to consent. The artifact must say which case applies (`same_as_bearer`, `different_from_bearer` or `mixed`). When the payer differs from the bearer, the outcome link is the only place that states the venture's effect on the bearer. The verifier therefore does not let it be left out.

## The size question

Most single ventures move a large social metric by a small amount. The outcome link forces that amount into the open with its arithmetic. The housing example closes about a tenth of its own gap to target and says so in an open item. A small contribution is not a failure of the method. An unstated one is.

## What the verifier does not do

It does not check that a causal link is true, or that the intervention point is the best one. It does not check that the customer exists or that the arithmetic uses the right rent response. Those are human work and expert review. See `verification-boundary.md`.
