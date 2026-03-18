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
    def add_product(self, product: Product) -> bool:
        """Add a new product to the inventory.

        Args:
            product (Product): The product to add.

        Returns:
            bool: True if the product was added successfully, False if a product with the same ID already exists.
        """
        if product.id in self._products:
            return False  # Product ID already exists
        self._products[product.id] = product
        return True

    # TODO: search products by name or category
    def search_products(self, name: Optional[str] = None, category: Optional[Category] = None) -> list[Product]:
        """Search for products by name or category.

        Args:
            name (Optional[str]): The name to search for (case-insensitive).
            category (Optional[Category]): The category to search for.

        Returns:
            list[Product]: A list of products matching the search criteria.
        """
        results = list(self._products.values())
        if name:
            results = [p for p in results if name.lower() in p.name.lower()]
        if category:
            results = [p for p in results if p.category == category]
        return results

    def get_low_stock_products(self) -> list[Product]:
        """Get a list of products that are low in stock based on their reorder threshold.

        Returns:
            list[Product]: A list of products that need to be restocked.
        """
        return [p for p in self._products.values() if p.quantity <= p.reorder_threshold]

    def generate_inventory_report(self) -> str:
        """Generate a formatted inventory report.

        Returns:
            str: A formatted string representing the inventory report.
        """
        report_lines = ["Inventory Report:"]
        for product in self._products.values():
            report_lines.append(
                f"ID: {product.id}, Name: {product.name}, Category: {product.category.value}, "
                f"Price: ${product.price:.2f}, Quantity: {product.quantity}, "
                f"Last Restocked: {product.last_restocked or 'N/A'}"
            )
        return "\n".join(report_lines)


# TODO: add main block with sample data
if __name__ == "__main__":
    inventory_manager = InventoryManager()

    # Sample products
    product1 = Product(id="P001", name="Smartphone", category=Category.ELECTRONICS, price=699.99, quantity=50)
    product2 = Product(id="P002", name="Jeans", category=Category.CLOTHING, price=49.99, quantity=200)
    product3 = Product(id="P003", name="Organic Apples", category=Category.GROCERIES, price=3.99, quantity=100)
    product4 = Product(id="P004", name="Laptop", category=Category.ELECTRONICS, price=1299.99, quantity=5)
    product5 = Product(id="P005", name="T-Shirt", category=Category.CLOTHING, price=19.99, quantity=500)
    product6 = Product(id="P006", name="Milk", category=Category.GROCERIES, price=4.49, quantity=50)
    product7 = Product(id="P007", name="Garden Soil", category=Category.HOME_GARDEN, price=12.99, quantity=30)
    product8 = Product(id="P008", name="Yoga Mat", category=Category.SPORTS, price=29.99, quantity=8)
    product9 = Product(id="P009", name="Coffee Maker", category=Category.HOME_GARDEN, price=89.99, quantity=15)
    product10 = Product(id="P010", name="Running Shoes", category=Category.SPORTS, price=149.99, quantity=3)

    # Add products to inventory
    inventory_manager.add_product(product1)
    inventory_manager.add_product(product2)
    inventory_manager.add_product(product3)
    inventory_manager.add_product(product4)
    inventory_manager.add_product(product5)
    inventory_manager.add_product(product6)
    inventory_manager.add_product(product7)
    inventory_manager.add_product(product8)
    inventory_manager.add_product(product9)
    inventory_manager.add_product(product10)

    # Generate and print inventory report
    print(inventory_manager.generate_inventory_report())