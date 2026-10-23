# Governance and documentation

When to read this: writing a model card or data notes, a risk record, or answering questions about regulation, compliance, hiring, credit or other decisions about people. Everything regulatory here is orientation only, not legal advice; a lawyer decides.

## 1. Risk framework in one paragraph
NIST's AI Risk Management Framework organises the work as govern, map, measure, manage [S-GOV-1]; its generative-AI profile lists risks such as confabulation, data privacy, information security and harmful bias [S-GOV-2]. Use it as a checklist for the design file's risk section, not as a certificate. Company principle sets (fairness, reliability, privacy, inclusiveness, transparency, accountability) are a similar lens [S-GOV-9].

## 2. Model card template (`docs/ai/<model>-model-card.md`)
Based on model cards [S-GOV-3] and the Hugging Face template [S-GOV-10]:
1. Model: what it is, version, date, owner.
2. Intended use and users; out-of-scope uses.
3. Data: source, size, labels and who made them, known problems (duplicates, overlap, imbalance, label conflicts), personal data handling.
4. Evaluation: test set, baseline, per-class metrics with `k of n` and intervals, slices that matter (language, length), what was not measured.
5. Limits and risks; known failure examples.
6. Recommendation (go, no-go, conditions) as a decision for the owner, and what would change it.
7. What was not run, and how each number was obtained (`verified` computed here, `inferred`, `unknown`).

For a dataset, add data-sheet notes: why it was made, how collected, what it contains, consent, how it may be used [S-GOV-4].

## 3. EU AI Act and decisions about people (orientation only)
- The Act sorts AI uses by risk; uses such as recruitment and decisions about workers are in the high-risk group, which carries obligations for providers and deployers (risk management, data governance, documentation, human oversight, accuracy) [S-GOV-5], [S-GOV-6]. Whether a given tool falls inside, and which duties apply, is a legal question.
- Never write a compliance certificate or a statement that a tool "is compliant". Offer instead: a risk and documentation pack (intended use, data, evaluation, human oversight design, logs) that a lawyer or the formal conformity process can use.
- Hiring and similar decisions: the AI must not rank or reject real people on its own; a named human decides. Protected or sensitive details (age or date of birth, marital status, children, health, religion, ethnicity) must not drive the decision; remove them before any model sees the text. Test for bias with synthetic CVs that differ only in one such detail.
- Running real candidates' CVs through a model is a use of personal data that needs the owner's approval and a lawful basis; as a specialist, return it as `needs_approval` and do not process them.

## 4. Records to keep in `docs/ai/`
Design file, eval set and results, model card, risk notes (top risks, mitigations, owner), approvals received (who, when, what), and the change log of prompts and model versions. Keep them short and dated.
