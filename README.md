# GitHub Copilot — Customer Demo Repository

A hands-on, live-coding demonstration of GitHub Copilot's capabilities for prospective customers.

## Quick Start

1. Open this repo in VS Code with GitHub Copilot and Copilot Chat extensions installed
2. Read **[PRESENTER_GUIDE.md](docs/PRESENTER_GUIDE.md)** for the full demo playbook
3. Follow the demos in order (01 through 08)

## Repository Structure

```
docs/
  PRESENTER_GUIDE.md              ← START HERE — full demo script with talking points
  SCENARIO_GUIDE.md               ← Deep-dive prep notes for the 3 customer scenarios
  scenario1-cobol-migration.md    — COBOL → Java at scale
  scenario2-measuring-impact.md   — Proving ROI to management
  scenario3-outsourcing-automation.md — Outsourcing & junior dev concerns

demos/
  01-code-completion/           ← Ghost text / autocomplete (the "wow" moment)
    inventory_manager_starter.py    — Skeleton file for live completion
    inventory_manager_reference.py  — Completed reference (presenter fallback)

  02-chat-and-explain/          ← Copilot Chat explains complex code
    legacy_processor.py             — Dense, undocumented financial code

  03-refactoring/               ← Clean up messy code with Chat
    messy_code.py                   — Intentionally bad code to refactor

  04-documentation/             ← /doc command generates docstrings
    api_service.py                  — Undocumented API client module

  05-agent-mode/                ← Agent Mode builds from requirements
    requirements.md                 — Natural language spec for a REST API

  06-test-generation/           ← /tests command generates unit tests
    shopping_cart.py                — Feature-rich class for test generation

  07-cobol-to-java/             ← Language translation (Scenario 1 tie-in)
    customer-report.cbl             — Real COBOL program to convert

  08-coding-agent/              ← Coding Agent (assign issues to Copilot)
    feature_request.md              — Sample issue for agent workflow
```

## Prerequisites

- VS Code with GitHub Copilot + Copilot Chat extensions
- GitHub account with active Copilot subscription
- Python 3.11+ (for running demo code)
- Internet connection (Copilot requires it)

## Demo Duration

- **Live coding demos + scenario discussion:** ~25-30 minutes
- Additional bonus material in the repo can extend to 45-60 minutes if needed
