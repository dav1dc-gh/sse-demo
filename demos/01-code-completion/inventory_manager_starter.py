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
        results = []
        for product in self._products.values():
            if name and name.lower() not in product.name.lower():
                continue
            if category and product.category != category:
                continue
            results.append(product)
        return results

    def get_low_stock_products(self) -> list[Product]:
        """Get a list of products that are low in stock.

        Returns:
            list[Product]: A list of products with stock below their reorder threshold.
        """
        return [product for product in self._products.values() if product.quantity < product.reorder_threshold]

    # TODO: generate_inventory_report — formatted output
    def generate_inventory_report(self) -> str:
        """Generate a formatted inventory report.

        Returns:
            str: A formatted string representing the inventory report.
        """
        report_lines = ["Inventory Report:", "ID | Name | Category | Price | Quantity | Last Restocked"]
        for product in self._products.values():
            last_restocked = product.last_restocked.strftime("%Y-%m-%d") if product.last_restocked else "N/A"
            report_lines.append(f"{product.id} | {product.name} | {product.category.value} | ${product.price:.2f} | {product.quantity} | {last_restocked}")
        return "\n".join(report_lines)


# TODO: add main block with sample data
if __name__ == "__main__":
    inventory_manager = InventoryManager()

    # Sample products
    product1 = Product(id="P001", name="Smartphone", category=Category.ELECTRONICS, price=699.99, quantity=50)
    product2 = Product(id="P002", name="Jeans", category=Category.CLOTHING, price=49.99, quantity=200)
    product3 = Product(id="P003", name="Organic Apples", category=Category.GROCERIES, price=3.99, quantity=100)
    product4 = Product(id="P004", name="Laptop", category=Category.ELECTRONICS, price=1299.99, quantity=25)
    product5 = Product(id="P005", name="Running Shoes", category=Category.SPORTS, price=89.99, quantity=75)
    product6 = Product(id="P006", name="Office Chair", category=Category.HOME_GARDEN, price=249.99, quantity=15)
    product7 = Product(id="P007", name="T-Shirt", category=Category.CLOTHING, price=19.99, quantity=300)
    product8 = Product(id="P008", name="Coffee Beans", category=Category.GROCERIES, price=12.99, quantity=50)
    product9 = Product(id="P009", name="Yoga Mat", category=Category.SPORTS, price=34.99, quantity=40)
    product10 = Product(id="P010", name="Desk Lamp", category=Category.HOME_GARDEN, price=59.99, quantity=8)

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