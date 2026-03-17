# SCENARIO GUIDE — Deep-Dive Preparation Notes

This document provides in-depth guidance for handling the three customer scenarios
during and after the demo. Read this before the presentation to internalize the
key arguments, reframes, and objection responses. The per-scenario files in
`scenarios/` contain additional reference material (objection tables, pilot
templates, etc.) that you can consult during Q&A.

---

## Scenario 1: COBOL-to-Java Migration

### What the customer is really asking
On the surface they're asking "can Copilot convert our COBOL?" But the deeper
question is: **"Can we get off the mainframe without a 5-year, $50M project?"**
The talent angle ("find developers") tells you they're already feeling the pain
of a shrinking COBOL workforce.

### Your strategic position
**Be honest — don't oversell, but don't undersell either.** Copilot is genuinely
one of the best tools available for COBOL-to-Java conversion because it produces
*idiomatic* Java (proper classes, enums, BigDecimal for currency) rather than the
unreadable transliterated output that older automated converters produce. The live
demo proves this instantly. But you must set realistic expectations about the
**90% of the work that isn't code conversion**:

- **Data layer**: COBOL programs talk to VSAM files, IMS, DB2. The Java
  equivalents need a database strategy (PostgreSQL? Oracle? Keep DB2?). Copilot
  doesn't migrate your data.
- **Integration**: JCL batch scheduling, CICS online transactions, MQ message
  flows — these are operational infrastructure, not just code.
- **Testing**: The COBOL programs that have been running for 30 years have been
  "tested by production." The new Java code has zero test history. You need
  comprehensive validation.
- **Performance**: COBOL on z/OS is *extremely* fast for batch processing. Java
  equivalents may need optimization.

### How to frame it
Use this mental model: **Copilot handles the 30% of the effort that used to take
70% of the time.** The code conversion itself — understanding the COBOL,
translating it, generating tests — is where Copilot shines. What used to take a
developer a week per program can happen in hours. But the overall migration still
needs:

1. **Phased approach** (Strangler Fig pattern) — convert one program at a time
2. **Parallel running** — old and new run side-by-side until validated
3. **Prioritization** — not all COBOL needs converting; focus on
   high-change-frequency programs

### The key insight to deliver
> "Copilot doesn't eliminate the need for a migration strategy — it makes the
> strategy *economically viable*. Without Copilot, converting 10,000 COBOL
> programs is prohibitively expensive. With Copilot, the per-program cost drops
> dramatically, making a phased migration realistic."

Also mention: even if they **never migrate**, Copilot still helps their COBOL
developers understand and document legacy code, and generate new COBOL faster.
It's a win either way.

### Watch out for
The customer may push back with "we tried automated converters before and they
produced garbage." This is your moment — the live demo shows Copilot generating
*clean, readable* Java, not a 1:1 transliteration. That's the differentiator.

### Common objections

| Objection | Response |
|-----------|----------|
| "Can't we just batch-convert everything?" | Conversion is the easy part. Validation, testing, and operational readiness are 70% of the effort. Copilot accelerates the conversion piece enormously. |
| "How accurate is the conversion?" | Very good for business logic translation, but every conversion needs human review and testing — just like code from any developer. |
| "We tried automated converters before" | Copilot generates *idiomatic* Java, not a 1:1 transliteration. It understands both languages natively. The live demo proves this clearly. |
| "How long will the full migration take?" | Depends on complexity, but Copilot can reduce the per-program conversion effort by 50-70%. The rest is testing and integration work. |

---

## Scenario 2: Proving ROI to Management

### What the customer is really asking
They're already bought in personally — they want Copilot. What they need is
**ammunition for an internal business case.** They're essentially asking you:
"Help me sell this to my CFO/CTO."

### Your strategic position
This is the most straightforward scenario because the math genuinely works in
Copilot's favor. The ROI is almost absurdly good when you do the numbers.

### The simple math you should be able to recite

- Copilot Business costs **$19/user/month** ($228/year)
- A developer's loaded cost is typically **$150K-$250K/year** (~$75-$125/hr)
- If Copilot saves just **30 minutes per day** per developer:
  - 250 working days × 0.5 hours = 125 hours saved/year
  - At $75/hr = **$9,375 in productivity per developer**
  - vs. $228 cost = **~41x ROI**
- Even at 15 minutes/day the ROI is ~20x
- At 1 hour/day with 100 devs: 25,000 hours saved, $1.875M value, ~82x ROI

The challenge isn't the math — it's that **executives don't trust vendor-provided
numbers**. So the real answer is: **run your own pilot and generate your own data.**

### The three-pillar measurement framework

Explain that they should measure impact across three dimensions, because different
stakeholders in their org care about different things:

**Pillar 1: Quantitative metrics** (for the CFO/finance)
- PR cycle time (before vs. after)
- Deployment frequency
- Copilot acceptance rate (from the built-in Copilot usage dashboard)
- Standardized task completion time (Copilot group vs. control group)
- GitHub's own research showed **55% faster task completion** with Copilot

**Pillar 2: Qualitative metrics** (for the CTO/engineering leadership)
- Developer satisfaction surveys (before vs. after)
- Specific anecdotes: "I was stuck on X for an hour, Copilot solved it in 30 seconds"
- NPS-style question: "Would you recommend Copilot to a colleague?"
- GitHub's research: **75% of developers feel more satisfied** with Copilot

**Pillar 3: Business impact** (for the CEO/board)
- Projected cost savings at full scale
- Quality improvements (bug rates, test coverage)
- Talent retention and recruitment advantage
- Cost of replacing a developer: 50-200% of annual salary

### The pilot structure to recommend

| Phase | Duration | Activities |
|-------|----------|------------|
| **1. Baseline** | 2 weeks | Survey devs, capture current metrics (PR cycle time, deploy frequency, code churn), identify 5 standardized coding tasks |
| **2. Pilot** | 4-6 weeks | Enable Copilot for 2-4 selected teams, 1-hour onboarding session, weekly check-ins with brief survey + dashboard metrics, developers log "Copilot moments" |
| **3. Analysis** | 1-2 weeks | Compare before/after, compile survey results and anecdotes, calculate projected ROI, build executive presentation |

### The template they can take to their boss

Offer them this framing for their internal pitch:

> "During our 6-week pilot with [N] developers, GitHub Copilot delivered:
> - **X% faster** task completion on standardized coding exercises
> - **Y% improvement** in PR cycle time
> - **Z% of code** accepted from Copilot suggestions (reducing manual coding)
> - **Developer satisfaction increased** from [A] to [B] (out of 10)
> - **Projected annual ROI**: [calculated figure] at full-scale rollout
> - **Developer quote**: '[compelling anecdote from pilot participant]'"

### Watch out for
The objection "what if developers become dependent?" is common from skeptical
managers. The answer: Copilot is a tool in the IDE, like syntax highlighting or
IntelliSense. Nobody worries about developers becoming "dependent" on
autocomplete. It augments their capability — they still have to understand the
code, make design decisions, and review the output.

### Common objections

| Objection | Response |
|-----------|----------|
| "How do we know the productivity gain is real?" | We measure outcomes (PRs merged, tasks completed, deploy frequency), not code volume. Copilot also improves quality and test coverage. |
| "Is the 55% figure realistic for us?" | Your pilot will generate your own numbers. Even a 20% improvement delivers massive ROI at $19/user/month. |
| "What if developers become dependent on it?" | It's a tool like any IDE feature. Developers still understand the code. Think of autocomplete on steroids — it augments, not replaces. |
| "How do we measure quality, not just speed?" | Track bug rates, test coverage, code review feedback, and production incidents before and after. |

---

## Scenario 3: Outsourcing & "Automating" Juniors

### What the customer is really asking
They want to **cut costs** from their outsourcing budget. They've heard AI can
"replace developers" and they're hoping Copilot is the tool to do it. This is
the scenario that requires the most **careful handling** because their framing
is wrong, and if you just agree with it, you'll set them up for disappointment
(and a failed deployment).

### Your strategic position
**Acknowledge the goal, redirect the method.** Cost efficiency is a legitimate
and important goal. But the mechanism — "automate juniors to remove headcount" —
fundamentally misunderstands what Copilot does. You need to reframe without
being dismissive.

### The critical reframe

The customer says "replace developers." You say "amplify developers." Here's why
this isn't just semantics:

**What Copilot automates:**
- Boilerplate code and repetitive patterns
- Syntax recall and API usage
- Test scaffolding
- Documentation
- Understanding unfamiliar code

**What Copilot does NOT automate:**
- Understanding business requirements
- Making architectural decisions
- Evaluating trade-offs
- Debugging complex production issues
- Code review judgment
- Communicating with stakeholders

A developer's job is maybe 40% "writing code" and 60% "everything else." Copilot
accelerates the 40% dramatically, but a human is still in the loop for all of it.

### The reframe table

When the customer uses language from the left column, gently redirect to the right:

| Customer Says | Better Framing |
|--------------|----------------|
| "Replace 5 junior developers" | "Make your 5 junior developers perform like 8" |
| "Automate junior work" | "Eliminate repetitive work so juniors can tackle higher-value tasks" |
| "Reduce headcount" | "Increase throughput without increasing headcount" |
| "Cut costs" | "Deliver more features per dollar spent on development" |

### The three business models to present

Rather than arguing against their goal, give them **three concrete models** they
can evaluate:

**Model A: "Do More with the Same"** (recommended — lowest risk, fastest results)
- Keep the same outsourced team size
- Deploy Copilot to the entire team
- Measure the increased output (features shipped, bugs fixed, PRs merged)
- Result: **30-50% more throughput at the same cost + Copilot licenses**

**Model B: "Gradual Efficiency"** (moderate risk)
- As natural attrition occurs, don't backfill every role
- Each remaining developer with Copilot absorbs some of the workload
- Over 12-18 months, the team may be 15-20% smaller at the same output level

**Model C: "Insource with Copilot"** (strategic, higher risk)
- Use Copilot to make a smaller internal team viable for work currently outsourced
- 5 internal developers with Copilot might replace 8-10 outsourced developers
- Benefits: better IP protection, faster iteration, reduced communication overhead

Recommend Model A because it's lowest risk, shows results immediately, and
doesn't create morale problems. If the pilot shows 40% more throughput, they
effectively got 40% more capacity without hiring — that IS cost savings, just
expressed differently.

### The junior developer argument

This is the most important point to land: **juniors benefit the most from Copilot
and are therefore the worst candidates to cut.**

- A junior with Copilot works at something close to mid-level pace
- Copilot *teaches* juniors by showing them patterns, idioms, and best practices
- Juniors are how you build your talent pipeline — cut juniors today, and in
  2-3 years you have no mid-level developers
- If you frame the pilot as "we're going to use this to replace you," adoption
  will tank because developers will resist using the tool

### The outsourcing-specific angles

Copilot addresses real outsourcing pain points that have nothing to do with
headcount:

- **Ramp-up time**: New outsourced developers can understand a codebase in hours
  instead of weeks (Chat/Explain — you demoed this)
- **Code review rework cycles**: Better first-draft quality means fewer review
  rounds between your internal team and the outsourced team
- **Consistency**: Copilot follows project patterns, so outsourced code "feels"
  more like internally-written code
- **Knowledge silos**: Copilot generates documentation, reducing the risk when
  an outsourced developer leaves

### Risks to flag

| Risk | Mitigation |
|------|------------|
| **Quality erosion** — cutting headcount + expecting same output = quality drops | Maintain code review standards. Use Copilot for review assistance, but don't skip human review. |
| **Capability loss** — cutting juniors disrupts the talent pipeline | Invest in juniors + Copilot to build a stronger team over time. Juniors become seniors. |
| **Vendor dependency** — per-headcount contracts may trigger unfavorable renegotiation | Focus on throughput/velocity metrics in vendor contracts rather than headcount. |

### Watch out for
The biggest risk is the customer hearing what they want to hear. If they walk
away thinking "Copilot will let us cut 30% of our outsourced team next quarter,"
they will be disappointed and blame the tool. Be clear: **harvest productivity
gains first, make staffing decisions from data second.** Model A first, then
consider Model B based on actual results.

### Common objections

| Objection | Response |
|-----------|----------|
| "But we want to cut costs, not just be more productive" | Productivity IS cost savings. If the same team delivers 40% more, you avoid hiring for the next 2-3 projects. That's a concrete saving. |
| "Can Copilot write entire features without a developer?" | Coding Agent can handle well-defined, scoped tasks, but it creates a PR that needs human review. It's an accelerator, not a replacement. |
| "Our outsourcing vendor says they can cut rates instead" | A rate cut doesn't improve velocity or quality. Copilot improves both. A developer at $50/hr with Copilot delivers more value than one at $40/hr without it. |
| "We just want to try it with juniors first" | Great pilot idea — juniors show the most dramatic improvement. But frame the pilot around productivity gains, not headcount reduction, so developers actually adopt it. |
| "Can we measure how much work Copilot is doing vs. developers?" | Yes — the dashboard shows acceptance rates. But the real metric is team output (features, velocity, quality), not Copilot's individual contribution. |

---

## How the Three Scenarios Connect

There's a thread that ties all three together, and it's worth calling out in
the presentation:

1. **Scenario 1** (COBOL): Copilot is the **engine** for modernization — it does
   the heavy lifting of code conversion, but you still need a strategy around it
2. **Scenario 2** (Measurement): Copilot's value is **provable** — run a
   structured pilot, measure three pillars, and the data will make the business case
3. **Scenario 3** (Outsourcing): Copilot **amplifies people** — it makes every
   developer more capable, which is fundamentally more valuable than trying to
   eliminate developers

**The common theme:**
> Copilot is a productivity multiplier for your developers, not a substitute for
> them. That's both an honest and a compelling message.
