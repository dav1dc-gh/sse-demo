# PRESENTER GUIDE — GitHub Copilot Customer Demo

## Overview

This guide provides a structured order of operations for delivering a compelling
GitHub Copilot demo to a prospective customer. The demo is designed for
**25-30 minutes** of live coding and scenario discussion.

**Golden Rule:** Let Copilot do the talking. The most powerful moments in this
demo are when you stop typing and let the audience watch Copilot generate code
in real time. Resist the urge to explain too much — show, don't tell.

---

## Pre-Demo Checklist

- [ ] VS Code installed with **GitHub Copilot** and **GitHub Copilot Chat** extensions
- [ ] Signed into GitHub with a Copilot-enabled account
- [ ] This repository cloned and open in VS Code
- [ ] Font size increased for readability (Cmd+= a few times)
- [ ] Copilot Chat panel visible (Ctrl+Cmd+I or via sidebar)
- [ ] Terminal panel accessible
- [ ] Python installed (for running demo code)
- [ ] Close all other VS Code tabs — start clean
- [ ] Test-run Demo 1 (code completion) to verify Copilot is responding
- [ ] Review the 3 scenario guides in `docs/` folder
- [ ] Disable "Do Not Disturb" / notifications on your machine

---

## Time Budget at a Glance

| Segment | Duration | Features Shown |
|---------|----------|---------------|
| Opening | 1 min | — |
| Demo 1: Code Completion | 5 min | Ghost text, Tab-accept, context-awareness |
| Demo 2: Chat — Explain, Refactor, Doc | 5 min | Chat, /explain, /doc, /fix, inline chat |
| Demo 3: Agent Mode | 5 min | Autonomous multi-file generation |
| Demo 4: Test Generation | 3 min | /tests, runnable output |
| Demo 5: COBOL → Java | 4 min | Language translation, Scenario 1 segue |
| Scenario Discussion & Q&A | 5-7 min | Scenarios 1, 2, 3 |
| **Total** | **28-30 min** | |

---

## Demo Flow — Order of Operations

### Opening (1 minute) — No Slides, Just Talk

**What to say:**
> "GitHub Copilot is an AI-powered coding assistant that lives inside your editor.
> Rather than slides, I'm going to show you what it does — live. It works in
> VS Code, JetBrains, Visual Studio, and more, across 50+ languages, and is
> available at Individual, Business, and Enterprise tiers. Let's jump in."

---

### Demo 1: Code Completion — "Autocomplete on Steroids" (5 min)

**File:** `demos/01-code-completion/inventory_manager_starter.py`
**Fallback:** `demos/01-code-completion/inventory_manager_reference.py`

**Goal:** Show that Copilot generates entire methods from minimal context.

#### Steps:
1. **Open the starter file** — briefly show the `Product` dataclass and
   empty `InventoryManager` class
2. **Type the method signature**: `def add_product(self, product: Product) -> bool:`
   - Pause. Let Copilot suggest the full method body
   - Accept with Tab. Say: "I typed one line, Copilot wrote eight"
3. **Type a comment**: `# Search products by name or category`
   - Press Enter and pause — Copilot generates the entire search method
   - "It understood our data model and created a filter method"
4. **Type**: `def get_low_stock_products`
   - Point out it uses `reorder_threshold` — it understood the *semantics*
5. **Type**: `if __name__ == "__main__":`
   - Watch Copilot generate realistic sample data and a usage example
6. **Run the code** in terminal — show it works

**Key line to deliver:**
> "This isn't autocomplete — it's generating correct business logic.
> The more context you give (type hints, good names, comments) the better
> the suggestions. That's prompt engineering for code."

---

### Demo 2: Chat — Explain, Refactor & Document (5 min)

This demo showcases **three Chat capabilities in rapid succession** using two files.

#### Part A — Explain Legacy Code (2 min)
**File:** `demos/02-chat-and-explain/legacy_processor.py`

1. **Open the file** — say: "You've just joined a team and you're handed this.
   No docs, cryptic names, dense logic."
2. **Select the `proc_txn_batch` function**
3. **In Chat, ask**: "Explain this code"
   - Copilot breaks it down: parsing, FX conversion, grouping, risk scoring
   - "30 seconds to understand code that would take 30 minutes to read"

#### Part B — Refactor Messy Code (1.5 min)
**File:** `demos/03-refactoring/messy_code.py`

1. **Open the file** — let the audience see the horror
2. **Select the `do_stuff` function**
3. **Ask Chat**: "Refactor this following clean code principles"
   - Watch it transform: proper names, separated functions, type hints
   - "Every codebase has code like this. Copilot makes cleanup effortless"

#### Part C — Generate Documentation (1.5 min)
**File:** `demos/04-documentation/api_service.py`

1. **Open the file** — "Zero documentation."
2. **Select the `WeatherApiClient` class**, use Chat: `/doc`
   - Copilot generates docstrings for every method
   - "Documentation goes from a 30-minute chore to a 30-second task"

**Key line to deliver:**
> "Chat isn't just Q&A — it explains, refactors, documents, and finds bugs.
> It's a senior pair programmer that's always available."

---

### Demo 3: Agent Mode — "Build From Requirements" (5 min)

**File:** `demos/05-agent-mode/requirements.md`

**Goal:** Show Copilot Agent Mode autonomously building a complete application.

#### Steps:
1. **Open the requirements file** — briefly show the data model and endpoints
2. **Switch Chat to Agent Mode** then prompt: "Using the requirements in
   demos/05-agent-mode/requirements.md, build a complete FastAPI application
   with all the necessary files"
3. **Narrate while Agent works** (it takes 2-3 min):
   - "It's creating models, routes, a database layer, and the main app"
   - "Notice it ran a command and got an error — now it's fixing it automatically"
4. **Quick scan** the generated files when it finishes

**Key lines to deliver:**
> "I gave it a natural language spec, and it built a working API — multiple files,
> proper structure, validation, error handling. Agent Mode creates files, runs
> commands, and iterates on errors autonomously."

**If Agent is slow:** Start it, narrate for 30 seconds, then say: "This will
continue working — let me show you the next demo and we'll come back to the results."

---

### Demo 4: Test Generation (3 min)

**File:** `demos/06-test-generation/shopping_cart.py`

**Goal:** Show Copilot generating comprehensive, runnable unit tests.

#### Steps:
1. **Open the file** — "Here's a shopping cart with pricing, discounts, and tax"
2. **Select the entire `ShoppingCart` class**
3. **Chat**: `/tests`
4. **Highlight the output** — descriptive test names, edge cases (empty cart,
   expired discounts, invalid quantities), proper fixtures
5. **Save and run**:
   ```bash
   cd demos/06-test-generation && python -m pytest test_shopping_cart.py -v
   ```
6. **Tests pass** — mic-drop moment

**Key line to deliver:**
> "Testing is the task developers skip the most. Copilot removes that friction —
> and it found edge cases I might have missed."

---

### Demo 5: COBOL → Java (4 min) — Scenario 1 Segue

**File:** `demos/07-cobol-to-java/customer-report.cbl`

**Goal:** Show live COBOL translation and tee up the scenario discussion.

#### Steps:
1. **Open the COBOL file** — let the audience absorb the syntax for 10 seconds
2. **Ask Chat**: "Explain what this COBOL program does"
   - Copilot summarizes: reads customer/transaction records, calculates balances,
     applies interest/fees, generates a statement report
3. **Ask**: "Convert this COBOL program to Java"
   - Point out: `PIC S9(9)V99` → `BigDecimal`, `EVALUATE` → `switch`,
     88-level conditions → enums, paragraphs → methods
4. **Say**: "This is one program. For millions of lines, you need a migration
   strategy — but Copilot is the engine that makes each conversion fast and
   high-quality. Let's talk about that."

**Transition to scenarios.**

---

## Scenario Discussion & Q&A (5-7 min)

Move to a conversational format. Briefly address each scenario — point the
customer to the detailed guides for deeper follow-up.

### Scenario 1: COBOL Migration (2 min)
**Guide for your prep:** `docs/scenario1-cobol-migration.md`

**Key messages to deliver:**
- Copilot is the **best accelerator** for program-by-program conversion —
  what takes a developer a week can be done in hours
- But it's not a push-button migration: data migration, integration testing,
  and operational parity still require a strategy
- **Recommended approach**: Strangler Fig pattern — convert one program at a time,
  validate, cut over, repeat
- Copilot also helps developers *understand* COBOL before converting it (Demo 2)

### Scenario 2: Measuring Impact (2 min)
**Guide for your prep:** `docs/scenario2-measuring-impact.md`

**Key messages to deliver:**
- Run a **4-6 week pilot** with 2-4 teams; measure before and after
- Three pillars: **Quantitative** (PR cycle time, Copilot acceptance rate,
  DORA metrics), **Qualitative** (developer satisfaction surveys),
  **Business ROI** (time saved × loaded cost vs. $19/user/month)
- GitHub's research: 55% faster task completion, 75% higher satisfaction
- Even at a conservative 30 min saved/dev/day, ROI is ~40x

### Scenario 3: Outsourcing & Junior Automation (2 min)
**Guide for your prep:** `docs/scenario3-outsourcing-automation.md`

**Key messages to deliver:**
- **Reframe**: "amplify everyone" not "replace juniors." Juniors benefit the
  *most* — Copilot elevates them toward mid-level performance
- The right model: **more throughput from the same team**, not fewer people
- Copilot still requires human judgment — code review, architecture, requirements.
  Even Coding Agent (which can implement issues autonomously) creates PRs that
  need human review
- Better first-draft quality from outsourced teams = less rework in reviews

**Q&A bridge:**
> "Those are the three scenarios — happy to go deeper on any of them.
> What questions do you have?"

---

## Prompt Engineering Tips to Weave In Naturally

Don't present these as a list — drop them during demos where they fit:

- **Demo 1**: "Good names and type hints ARE the prompt — that's prompt engineering for code"
- **Demo 2**: "Slash commands like `/explain`, `/doc`, `/fix` are built-in shortcuts"
- **Demo 3**: "The more specific the requirements, the better Agent Mode's output"
- **Demo 4**: "You can ask for a specific style: 'pytest with fixtures' or 'unittest.TestCase'"
- **Anytime**: "If the first suggestion isn't right, iterate: 'Make it async' or 'Use a list comprehension'"
- **Anytime**: "Use `#file:name.py` in Chat to reference specific files, or `@workspace` for full project context"

---

## Handling Common Questions

| Question | Answer |
|----------|--------|
| "Does Copilot store/learn from our code?" | No. Copilot Business and Enterprise do not retain prompts or suggestions, and your code is never used to train the model. |
| "What about licensing/IP concerns?" | Copilot Enterprise includes a code referencing filter that detects when a suggestion matches public code and shows the license. You can enable/disable this. |
| "Which languages does it support?" | All major languages. It's strongest in Python, JavaScript/TypeScript, Java, C#, Go, Ruby, and Rust. It also knows COBOL, SQL, Terraform, YAML, and more. |
| "How does it handle private/internal APIs?" | Copilot uses your open files and workspace as context. With `@workspace`, it searches your entire project. It learns your project's patterns during the session. |
| "What's the difference between Business and Enterprise?" | Enterprise adds: organization-wide policy management, audit logs, IP indemnity, knowledge bases (index your internal repos for better context), and fine-tuned models. |
| "Can we self-host it?" | Copilot runs as a cloud service. Your code is sent to the model for processing but NOT stored. Enterprise customers get data residency options. |
| "What about security — can it generate vulnerable code?" | Copilot includes an AI-based vulnerability filter that blocks common insecure patterns (SQL injection, hardcoded credentials, etc.). But like any code, Copilot output should go through your standard review process. |
| "What is Coding Agent?" | You can assign a GitHub Issue to `@copilot` and it autonomously creates a branch, implements the feature, writes tests, and opens a PR for human review. See `demos/08-coding-agent/feature_request.md` for an example. |

---

## Closing (1 minute)

**What to say:**
> "Copilot meets developers where they already work — inside their editor.
> It doesn't change the workflow; it supercharges it. Whether you're modernizing
> legacy code, measuring productivity, or getting more from your teams, it
> delivers measurable, immediate value. The best next step is a focused pilot.
> We can help structure that — let the data speak for itself."

---

## Emergency Fallbacks

1. **Network issues**: Tether to your phone. Copilot requires internet access.
2. **Poor suggestions**: Say "Let me show you prompt engineering in action" —
   refine the prompt and iterate. This is actually a *good* demo moment.
3. **Totally stuck**: Use the `_reference.py` files to show completed code and say
   "Here's what Copilot generated during my prep" — but always try live first.
4. **Agent Mode is slow**: Start it, narrate what's happening, and move to the
   next demo. Come back to show results.

---

## Bonus Material (if you have extra time or a follow-up session)

The following files are included in the repo and can extend the demo if needed:

- **`demos/03-refactoring/messy_code.py`** — Full refactoring deep-dive (ask Chat
   to enumerate code smells, apply Strategy pattern, etc.)
- **`demos/04-documentation/api_service.py`** — Extended documentation demo
  (generate a full README, an OpenAPI spec, usage examples)
- **`demos/08-coding-agent/feature_request.md`** — Live Coding Agent demo
  (create a GitHub Issue, assign to `@copilot`, show the resulting PR)
