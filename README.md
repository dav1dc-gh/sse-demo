# GitHub Copilot — Customer Demo Repository

A hands-on, live-coding demonstration of GitHub Copilot's capabilities for prospective customers.

## Quick Start

1. Open this repo in VS Code with GitHub Copilot and Copilot Chat extensions installed
2. Read **[PRESENTER_GUIDE.md](PRESENTER_GUIDE.md)** for the full demo playbook
3. Follow the demos in order (01 through 08)

## Repository Structure

```
PRESENTER_GUIDE.md              ← START HERE — full demo script with talking points

demos/
  01-code-completion/           ← Ghost text / autocomplete (the "wow" moment)
    inventory_manager_starter.py    — Skeleton file for live completion
    inventory_manager_reference.py  — Completed reference (presenter fallback)

  02-chat-and-explain/          ← Copilot Chat explains complex code
    legacy_processor.py             — Dense, undocumented financial code

  03-agent-mode/                ← Agent Mode builds from requirements
    requirements.md                 — Natural language spec for a REST API

  04-test-generation/           ← /tests command generates unit tests
    shopping_cart.py                — Feature-rich class for test generation

  05-refactoring/               ← Clean up messy code with Chat
    messy_code.py                   — Intentionally bad code to refactor

  06-documentation/             ← /doc command generates docstrings
    api_service.py                  — Undocumented API client module

  07-cobol-to-java/             ← Language translation (Scenario 1 tie-in)
    customer-report.cbl             — Real COBOL program to convert

  08-coding-agent/              ← Coding Agent (assign issues to Copilot)
    feature_request.md              — Sample issue for agent workflow

scenarios/                      ← Customer scenario discussion guides
  scenario1-cobol-migration.md      — COBOL → Java at scale
  scenario2-measuring-impact.md     — Proving ROI to management
  scenario3-outsourcing-automation.md — Outsourcing & junior dev concerns
```

## Prerequisites

- VS Code with GitHub Copilot + Copilot Chat extensions
- GitHub account with active Copilot subscription
- Python 3.11+ (for running demo code)
- Internet connection (Copilot requires it)

## Demo Duration

- **Live coding demos:** ~45-60 minutes
- **Scenario discussions + Q&A:** ~15-30 minutes
- **Total:** ~60-90 minutes
