"""
Inventory Management System — COMPLETED REFERENCE

This is the "answer key" for the presenter. Do NOT show this during the demo.
Use this if Copilot suggestions diverge and you need to get back on track.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Category(Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    GROCERIES = "groceries"
    HOME_GARDEN = "home_garden"
    SPORTS = "sports"


@dataclass
class Product:
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
        self._products: dict[str, Product] = {}

    def add_product(self, product: Product) -> bool:
        """Add a new product to inventory. Returns False if product ID already exists."""
        if product.id in self._products:
            return False
        self._products[product.id] = product
        return True

    def remove_product(self, product_id: str) -> bool:
        """Remove a product by ID. Returns False if product not found."""
        if product_id not in self._products:
            return False
        del self._products[product_id]
        return True

    def update_stock(self, product_id: str, quantity_change: int) -> bool:
        """Update stock level for a product. Positive to add, negative to remove."""
        if product_id not in self._products:
            return False
        product = self._products[product_id]
        new_quantity = product.quantity + quantity_change
        if new_quantity < 0:
            return False
        product.quantity = new_quantity
        if quantity_change > 0:
            product.last_restocked = datetime.now()
        return True

    def search_products(self, query: str, category: Optional[Category] = None) -> list[Product]:
        """Search products by name (case-insensitive) with optional category filter."""
        results = []
        for product in self._products.values():
            if query.lower() in product.name.lower():
                if category is None or product.category == category:
                    results.append(product)
        return results

    def get_low_stock_products(self) -> list[Product]:
        """Return products whose quantity is at or below their reorder threshold."""
        return [
            product for product in self._products.values()
            if product.quantity <= product.reorder_threshold
        ]

    def get_total_inventory_value(self) -> float:
        """Calculate the total value of all products in inventory."""
        return sum(p.price * p.quantity for p in self._products.values())

    def generate_inventory_report(self) -> str:
        """Generate a formatted inventory report showing all products and summary stats."""
        if not self._products:
            return "Inventory is empty."

        lines = []
        lines.append("=" * 60)
        lines.append("INVENTORY REPORT")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 60)
        lines.append("")

        for category in Category:
            category_products = [
                p for p in self._products.values() if p.category == category
            ]
            if not category_products:
                continue

            lines.append(f"--- {category.value.upper()} ---")
            for p in sorted(category_products, key=lambda x: x.name):
                stock_warning = " ⚠️ LOW STOCK" if p.quantity <= p.reorder_threshold else ""
                lines.append(
                    f"  {p.name:<30} | ${p.price:>8.2f} | Qty: {p.quantity:>5}{stock_warning}"
                )
            lines.append("")

        lines.append("=" * 60)
        lines.append(f"Total Products: {len(self._products)}")
        lines.append(f"Total Inventory Value: ${self.get_total_inventory_value():,.2f}")
        lines.append(f"Low Stock Items: {len(self.get_low_stock_products())}")
        lines.append("=" * 60)

        return "\n".join(lines)

    def apply_discount(self, category: Category, percent: float) -> int:
        """Apply a percentage discount to all products in a given category.
        Returns the number of products updated."""
        if not 0 < percent <= 100:
            raise ValueError("Discount percent must be between 0 and 100")
        count = 0
        for product in self._products.values():
            if product.category == category:
                product.price *= (1 - percent / 100)
                product.price = round(product.price, 2)
                count += 1
        return count


if __name__ == "__main__":
    manager = InventoryManager()

    # Add sample products
    products = [
        Product("E001", "Wireless Mouse", Category.ELECTRONICS, 29.99, 150),
        Product("E002", "USB-C Hub", Category.ELECTRONICS, 49.99, 8, reorder_threshold=10),
        Product("C001", "Running Shoes", Category.SPORTS, 89.99, 45),
        Product("C002", "Yoga Mat", Category.SPORTS, 24.99, 5, reorder_threshold=10),
        Product("G001", "Organic Coffee", Category.GROCERIES, 12.99, 200),
        Product("G002", "Almond Milk", Category.GROCERIES, 4.99, 3, reorder_threshold=15),
        Product("H001", "LED Desk Lamp", Category.HOME_GARDEN, 34.99, 60),
    ]

    for product in products:
        manager.add_product(product)

    print(manager.generate_inventory_report())

    print("\n🔍 Searching for 'mouse':")
    for p in manager.search_products("mouse"):
        print(f"  Found: {p.name} (${p.price})")

    print("\n⚠️ Low stock items:")
    for p in manager.get_low_stock_products():
        print(f"  {p.name}: {p.quantity} remaining (threshold: {p.reorder_threshold})")

    print("\n💰 Applying 15% discount to SPORTS...")
    count = manager.apply_discount(Category.SPORTS, 15)
    print(f"  Updated {count} products")
