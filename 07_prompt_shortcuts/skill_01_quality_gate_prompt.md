# Skill 01 Quality Gate Prompt

Use this prompt to run a quality gate review with AI.

---

Please act as the QE Director Agent and use **Skill 01: Quality Gate Review**.

Your job:
Evaluate whether this release is ready to proceed from a quality engineering perspective.

You must follow this output structure:
1. Conclusion
2. Key risks
3. Analysis
4. Recommended actions
5. Priority
6. Director reminder

Decision options:
- Go
- Conditional Go
- No Go

Evaluation criteria:
- Are there any unresolved blocker issues?
- Is regression coverage sufficient?
- Is rollback feasible?
- Is monitoring ready?
- Are key risks explicitly acknowledged?

Now review this case:

Project name:
[fill here]

Release name:
[fill here]

Change scope:
[fill here]

Open high-risk issues:
[fill here]

Regression result:
[fill here]

Monitoring and rollback readiness:
[fill here]
