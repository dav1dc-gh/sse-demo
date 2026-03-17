# PRESENTER GUIDE — GitHub Copilot Customer Demo

## Overview

This guide provides a structured order of operations for delivering a compelling
GitHub Copilot demo to a prospective customer. The demo is designed to take
**45-60 minutes** of live coding, followed by **15-30 minutes** of scenario
discussion and Q&A.

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
- [ ] Review the 3 scenario guides in `scenarios/` folder
- [ ] Disable "Do Not Disturb" / notifications on your machine

---

## Demo Flow — Order of Operations

### Opening (2-3 minutes) — No Slides, Just Talk

**What to say:**
> "GitHub Copilot is an AI-powered coding assistant that integrates directly
> into your editor. Rather than showing you slides, I'm going to show you what
> it can actually do. Everything you're about to see is live — no scripts,
> no pre-recorded output."

Briefly mention:
- Copilot works in VS Code, JetBrains, Visual Studio, Neovim, and on github.com
- It understands 50+ programming languages
- It uses the context of your project to make relevant suggestions
- Available at Individual, Business, and Enterprise tiers

---

### Demo 1: Code Completion — "The Autocomplete on Steroids" (8-10 min)

**File:** `demos/01-code-completion/inventory_manager_starter.py`
**Reference:** `demos/01-code-completion/inventory_manager_reference.py`

**Goal:** Show that Copilot generates entire methods from minimal context.

#### Steps:
1. **Open the starter file** — show the audience the `Product` dataclass and
   empty `InventoryManager` class with just `__init__`
2. **Type the method signature**: `def add_product(self, product: Product) -> bool:`
   - Pause. Let Copilot suggest the full method body
   - Accept with Tab. Point out: "I typed one line, Copilot wrote eight"
3. **Type a comment**: `# Search products by name or category`
   - Press Enter and pause — Copilot generates the entire search method
   - Highlight: "It understood our data model and created a filter method"
4. **Type**: `def get_low_stock_products`
   - Copilot should suggest using `reorder_threshold` — point out it understood
     the semantic meaning of the field, not just the name
5. **Type**: `def generate_inventory_report`
   - Let Copilot generate a multi-line formatted report
   - Show cycling through alternatives with Alt+] if the first suggestion isn't perfect
6. **Type**: `if __name__ == "__main__":`
   - Watch Copilot generate realistic sample data and usage examples
   - Point out: "It created products across different categories with realistic
     names and prices — this isn't random data"
7. **Run the code** in terminal to show it actually works

**Key talking points during this demo:**
- "Copilot understands the *context* of this file — it knows about the Product class,
  the Category enum, and uses them correctly"
- "Ghost text appears as you type — you accept with Tab, reject with Esc"
- "This isn't just autocomplete — it's generating *correct business logic*"

**Prompt Engineering Tip to Mention:**
> "Notice how a descriptive comment or a clear method signature is all Copilot
> needs. The more context you give — good variable names, type hints, docstrings
> — the better the suggestions. This is prompt engineering for code."

---

### Demo 2: Chat & Explain — "Your AI Pair Programmer" (5-7 min)

**File:** `demos/02-chat-and-explain/legacy_processor.py`

**Goal:** Show that Copilot Chat can explain complex, unfamiliar code.

#### Steps:
1. **Open the file** — scroll through and say: "Imagine you've just joined a
   team and you're handed this file. No documentation, cryptic variable names,
   dense logic. This happens every day in every company."
2. **Select the entire `proc_txn_batch` function** (lines 30-100 approximately)
3. **In Copilot Chat, ask**: "Explain this code"
   - Copilot will break down: parsing, FX conversion, grouping, risk scoring
   - Point out: "In 30 seconds, I understand code that would take me 30 minutes to read"
4. **Select the `validate_account_id` function** (the dense regex)
5. **Ask**: "What does this regex validate?"
   - Copilot will explain: IBAN, US routing numbers, and SWIFT codes
6. **Select `find_related_transactions`**
7. **Ask**: "What is the time complexity of this function?"
   - Copilot will identify the BFS pattern and analyze complexity
8. **Ask**: "Is there a bug in this code?" or "What edge cases could break this?"
   - Copilot will identify potential issues

**Key talking points:**
- "This is incredibly powerful for onboarding and knowledge transfer"
- "For your outsourced developers: they can understand any codebase instantly"
- "For your COBOL migration (Scenario 1): developers can understand legacy code
  before converting it"

---

### Demo 3: Agent Mode — "Build From Requirements" (8-10 min)

**File:** `demos/03-agent-mode/requirements.md`

**Goal:** Show Copilot Agent Mode autonomously building a complete application.

#### Steps:
1. **Open the requirements file** — show the audience the specifications
2. **Open Copilot Chat** and switch to **Agent Mode** (look for the @ or Agent toggle)
3. **Paste or reference the requirements**: "Using the requirements in
   demos/03-agent-mode/requirements.md, build a complete FastAPI application
   with all the necessary files"
4. **Watch Agent Mode work**:
   - It will create multiple files (models, routes, database, main app)
   - It may install dependencies
   - It iterates if there are errors — point this out!
5. **Show the generated files** — open each one briefly
6. **Run the application** if time permits (though the wow-factor is the generation)

**Key talking points:**
- "Agent Mode is different from regular Chat — it can create files, run commands,
  and iterate autonomously"
- "I gave it a natural language spec, and it built a complete, working API"
- "This is how Copilot accelerates greenfield development"

**Time management:** This demo can take 3-5 minutes for Agent to complete. If
running short on time, you can show the requirements, start Agent, and switch to
narrating what it's doing rather than waiting for completion.

---

### Demo 4: Test Generation — "/tests" (5-7 min)

**File:** `demos/04-test-generation/shopping_cart.py`

**Goal:** Show Copilot generating comprehensive, runnable unit tests.

#### Steps:
1. **Open the file** — briefly walk through the ShoppingCart class
2. **Select the entire class** (or the whole file)
3. **Use Copilot Chat**: `/tests` or ask "Generate comprehensive unit tests for this class"
4. **Show the generated tests**:
   - Point out test names are descriptive
   - Note edge cases: empty cart, invalid quantities, expired discounts
   - Show it correctly tests the tax calculation logic
   - Show it creates proper test fixtures and setup
5. **Save the generated test file** and **run the tests**:
   ```bash
   cd demos/04-test-generation
   python -m pytest test_shopping_cart.py -v
   ```
6. **Show that tests pass** — this is the mic-drop moment

**Key talking points:**
- "Writing tests is the task developers avoid the most. Copilot removes that friction"
- "It didn't just test the happy path — it found edge cases automatically"
- "This directly addresses code quality metrics for your management (Scenario 2)"

**Prompt Engineering Tip:**
> "You can ask for specific test styles: 'Generate pytest tests with fixtures',
> 'Write tests using unittest.TestCase', 'Include property-based tests'.
> The more specific your prompt, the more tailored the output."

---

### Demo 5: Refactoring — "Clean Up Legacy Code" (5-7 min)

**File:** `demos/05-refactoring/messy_code.py`

**Goal:** Show Copilot identifying code smells and producing clean refactored code.

#### Steps:
1. **Open the file** — let the audience see the horror
2. **Ask Copilot Chat**: "What are the code smells in this file?"
   - It will enumerate: God function, poor naming, deep nesting, magic numbers,
     duplicated logic, no type hints, bare except, etc.
3. **Select the `do_stuff` function**
4. **Ask**: "Refactor this function following clean code principles"
   - Watch Copilot transform it into well-named functions with proper types
5. **Select the `calc` function**
6. **Use inline chat** (Cmd+I): "Simplify this by reducing nesting"
   - Show the before/after side by side
7. **Select the `make_report` function**
8. **Ask**: "Refactor this to use the Strategy pattern"
   - Show how Copilot applies design patterns

**Key talking points:**
- "Every codebase has code like this — Copilot makes refactoring approachable"
- "The `/fix` command is great for smaller issues — try it on your own code"
- "For your outsourced teams (Scenario 3): better code quality = less rework in reviews"

---

### Demo 6: Documentation Generation (3-5 min)

**File:** `demos/06-documentation/api_service.py`

**Goal:** Show Copilot generating professional documentation.

#### Steps:
1. **Open the file** — point out: "Zero documentation. Every method is a mystery."
2. **Select the entire `WeatherApiClient` class**
3. **Use Copilot Chat**: `/doc`
   - Copilot generates Google/NumPy-style docstrings for every method
4. **Ask**: "Generate a README.md with usage examples for this module"
   - Show it creates a complete documentation page
5. **Bonus (if time)**: Ask "Generate an OpenAPI spec for this service's endpoints"

**Key talking points:**
- "Documentation is the first thing to be skipped under deadline pressure"
- "Copilot makes documentation a 30-second task instead of a 30-minute chore"
- "For your COBOL code (Scenario 1): generate documentation for legacy systems
  that have none"

---

### Demo 7: COBOL-to-Java Conversion (5-7 min) — Scenario 1 Demo

**File:** `demos/07-cobol-to-java/customer-report.cbl`
**Discussion guide:** `scenarios/scenario1-cobol-migration.md`

**Goal:** Show a live COBOL-to-Java conversion and set up the Scenario 1 discussion.

#### Steps:
1. **Open the COBOL file** — let the audience absorb COBOL syntax
2. **Ask Copilot Chat**: "Explain what this COBOL program does in plain English"
   - Show that Copilot understands COBOL perfectly
3. **Ask**: "Convert this entire COBOL program to Java"
   - Watch the conversion happen — data structures become classes, paragraphs
     become methods, copybooks become enums
4. **Point out specific conversion quality:**
   - COBOL's `PIC S9(9)V99` → Java's `BigDecimal`
   - `EVALUATE TRUE` → Java `switch` or `if/else`
   - `88-level conditions` → Java enums or boolean methods
   - Report formatting preserved
5. **Ask**: "Now write JUnit 5 tests for this Java code"
6. **Transition to Scenario 1 discussion** (see below)

---

### Demo 8: Coding Agent (3-5 min) — Concept/Walkthrough

**File:** `demos/08-coding-agent/feature_request.md`

**Goal:** Explain the Coding Agent workflow and how it fits into development.

#### Steps:
1. **Open the feature request** — show it as a well-defined GitHub Issue
2. **Explain the workflow**:
   - "In GitHub, you would assign this issue to `@copilot`"
   - "Copilot Coding Agent reads the issue, creates a branch, implements the
     feature, writes tests, and opens a pull request"
   - "A human reviews the PR, provides feedback, and merges"
3. **If you have Coding Agent access**: Create the issue live and assign it
4. **If not**: Walk through the concept and show a pre-built example PR

**Key talking points:**
- "This is the most autonomous Copilot gets — and it still creates a PR for review"
- "Perfect for well-defined, scoped tasks"
- "It doesn't replace developers — it handles the implementation so they can
  focus on design, architecture, and review"

---

## Scenario Discussions (15-20 min)

After the demos, transition to the customer-specific scenarios. You may want to
tie each scenario back to a specific demo you just showed.

### Scenario 1: COBOL Migration
**Guide:** `scenarios/scenario1-cobol-migration.md`

**Key message:** Copilot is the best tool available for program-by-program COBOL
conversion, but it's an *accelerator* for a migration strategy, not a push-button
solution. The customer needs a phased approach (Strangler Fig pattern).

**Tie back to:** Demo 7 (COBOL conversion) and Demo 2 (code explanation for
understanding legacy systems before migrating them).

### Scenario 2: Measuring Impact
**Guide:** `scenarios/scenario2-measuring-impact.md`

**Key message:** Use a structured pilot program measuring three pillars:
quantitative metrics (PR cycle time, acceptance rate, DORA metrics), qualitative
metrics (developer satisfaction surveys), and business impact (ROI calculation).
The ROI math is compelling even with conservative assumptions.

**Tie back to:** Demo 4 (test generation — measurable quality improvement),
Demo 1 (code completion — measurable time savings).

### Scenario 3: Outsourcing & Junior Automation
**Guide:** `scenarios/scenario3-outsourcing-automation.md`

**Key message:** Reframe from "replace juniors" to "amplify everyone." Juniors
benefit the *most* from Copilot — it elevates them toward mid-level performance.
The right model is "more throughput from the same team" not "same throughput from
fewer people."

**Tie back to:** Demo 3 (Agent Mode — accelerates work but requires human review),
Demo 5 (refactoring — higher quality reduces rework cycles with outsourced teams).

---

## Prompt Engineering Tips to Sprinkle Throughout

Share these naturally during the demo, not as a separate section:

1. **Be specific**: "Write a function that validates an email address using regex"
   is better than "validate email"
2. **Provide context**: Open related files, use `@workspace` in chat to give Copilot
   full project context
3. **Iterate**: If the first suggestion isn't right, refine your prompt. "Make it
   async" or "Use a list comprehension instead"
4. **Use types and names**: `def calculate_tax(income: float, state: str) -> float:`
   gives Copilot far more to work with than `def calc(x, y)`
5. **Comments as prompts**: A well-written comment before code is the simplest form
   of prompt engineering
6. **Slash commands**: `/tests`, `/doc`, `/fix`, `/explain` — purpose-built for
   common tasks
7. **Reference files**: Use `#file:filename.py` in chat to reference specific files

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

---

## Closing (2-3 minutes)

**What to say:**
> "What you've seen today is a tool that meets developers where they already work —
> inside their editor. It doesn't change their workflow; it supercharges it.
> Whether you're modernizing COBOL, measuring developer productivity, or getting
> more from your development teams, Copilot delivers measurable, immediate value.
>
> The best way to see if it works for your team is to try it. I'd recommend
> starting with a focused pilot — we can help structure that — and letting the
> data speak for itself."

---

## Emergency Fallbacks

If Copilot isn't responding or gives poor suggestions during the demo:

1. **Network issues**: Tether to your phone. Copilot requires internet access.
2. **Poor suggestions**: Say "Let me show you prompt engineering in action" — refine
   the prompt and iterate. This is actually a *good* demo moment.
3. **Totally stuck**: Use the `_reference.py` files to show completed code and say
   "Here's what Copilot generated during my prep" — but always try live first.
4. **Agent Mode is slow**: Start it, narrate what's happening, and move to the
   next demo. Come back to show results.
