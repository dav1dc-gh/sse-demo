"""
Inventory Management System

This module provides an inventory management system for a retail store.
It supports adding products, updating stock levels, searching inventory,
and generating reports.
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


class InventoryManager:
    """Manages the store's product inventory with CRUD operations and reporting."""

    def __init__(self):
        """Initialize the inventory manager with an empty product store."""
        self._products: dict[str, Product] = {}

    # TODO: add_product(self, product: Product) -> bool

    # TODO: search products by name or category

    # TODO: get_low_stock_products — use reorder_threshold

    # TODO: generate_inventory_report — formatted output


# TODO: add main block with sample data
