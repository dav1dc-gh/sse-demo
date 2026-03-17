"""
Inventory Management System

This module provides an inventory management system for a retail store.
It supports adding products, updating stock levels, searching inventory,
and generating reports.

DEMO INSTRUCTIONS:
==================
1. Open this file and place your cursor at the end of each section
2. Watch Copilot suggest the implementation based on the docstrings/comments
3. Accept suggestions with Tab, or cycle through alternatives with Alt+[ / Alt+]
4. Show how Copilot understands context from prior code in the same file
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Category(Enum):
    """Product categories for the retail store."""
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    GROCERIES = "groceries"
    HOME_GARDEN = "home_garden"
    SPORTS = "sports"


@dataclass
class Product:
    """Represents a product in inventory."""
    id: str
    name: str
    category: Category
    price: float
    quantity: int
    reorder_threshold: int = 10
    last_restocked: Optional[datetime] = None


# DEMO STEP 1: Place cursor here and let Copilot generate the class
# TIP: Type "class InventoryManager:" and pause — Copilot will suggest the full class

class InventoryManager:
    """Manages the store's product inventory with CRUD operations and reporting."""

    def __init__(self):
        """Initialize the inventory manager with an empty product store."""
        self._products: dict[str, Product] = {}

    # DEMO STEP 2: Type the method signature below and let Copilot fill in the body
    # def add_product(self, product: Product) -> bool:

    # DEMO STEP 3: Type a comment like "# Search products by name or category"
    # and let Copilot generate the search method

    # DEMO STEP 4: Type "def get_low_stock_products" and watch Copilot
    # understand it should use the reorder_threshold field

    # DEMO STEP 5: Type "def generate_inventory_report" and let Copilot
    # generate a full reporting method with formatted output

    # DEMO STEP 6: Type "def apply_discount(self, category: Category, percent: float)"
    # Copilot should generate logic that applies a percentage discount
    # to all products in a given category


# DEMO STEP 7: After the class is built, type at the bottom of the file:
# if __name__ == "__main__":
# and let Copilot generate a complete usage example with sample data
