# Coding Agent Demo — Feature Request (GitHub Issue)

## Demo Instructions

This demo showcases **GitHub Copilot Coding Agent** — the ability to assign
a GitHub Issue to Copilot and have it autonomously create a pull request
with the implementation.

### How to Demo

1. **Show this issue text** to the audience and explain this would normally
   be a GitHub Issue assigned to a developer
2. **Explain**: With Coding Agent, you can assign this issue directly to
   `@copilot` in GitHub, and it will:
   - Read the issue and understand the requirements
   - Create a feature branch
   - Implement the code changes
   - Write tests
   - Open a pull request with a description
3. **If you have Coding Agent access**, create a real issue in the demo repo
   and assign it to Copilot to show the live workflow
4. **If not**, walk through the concept and show a previously created PR

---

## Feature Request: Add Email Notification Service

### Description
We need a new notification service that sends email alerts when inventory
items fall below their reorder threshold. This should integrate with our
existing `InventoryManager` class.

### Requirements

1. Create a new `NotificationService` class in a separate file
2. The service should:
   - Accept a list of `Product` items that are low on stock
   - Format an HTML email with a table of low-stock items
   - Include product name, current quantity, reorder threshold, and supplier info
   - Support configurable recipients (TO, CC)
   - Log all notifications sent
3. Create an `InventoryMonitor` class that:
   - Periodically checks inventory levels using `InventoryManager.get_low_stock_products()`
   - Triggers notifications only for newly low-stock items (not already notified)
   - Maintains a cooldown period to prevent notification spam (default: 24 hours)
4. Add comprehensive unit tests with mocked email sending
5. Add type hints throughout and docstrings for public methods

### Acceptance Criteria
- [ ] `NotificationService` class created with email formatting
- [ ] `InventoryMonitor` class with deduplication logic
- [ ] Unit tests with >80% coverage
- [ ] No external dependencies beyond Python standard library + existing project deps
- [ ] Code follows existing project conventions
