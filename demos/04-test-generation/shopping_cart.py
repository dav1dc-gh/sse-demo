"""
Shopping Cart — Test Generation Demo

This module implements a fully working shopping cart with pricing logic,
discount codes, tax calculation, and checkout validation.

DEMO INSTRUCTIONS:
==================
1. Open this file alongside Copilot Chat
2. Select the entire ShoppingCart class
3. Use the Copilot Chat command: /tests
4. Watch Copilot generate comprehensive test cases covering:
   - Adding/removing items
   - Quantity updates
   - Discount code application
   - Tax calculations
   - Edge cases (empty cart, invalid quantities, expired discounts)
5. Run the generated tests to show they pass

ALTERNATIVE APPROACH:
- Right-click on a method → Copilot → Generate Tests
- Or use inline chat (Cmd+I / Ctrl+I) and type "write unit tests for this"
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Optional


class DiscountType(Enum):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"
    BUY_X_GET_Y = "buy_x_get_y"


@dataclass
class CartItem:
    product_id: str
    name: str
    unit_price: Decimal
    quantity: int
    taxable: bool = True

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity


@dataclass
class DiscountCode:
    code: str
    discount_type: DiscountType
    value: Decimal
    min_order_amount: Decimal = Decimal("0")
    expires_at: Optional[date] = None
    max_uses: Optional[int] = None
    current_uses: int = 0

    @property
    def is_valid(self) -> bool:
        if self.expires_at and date.today() > self.expires_at:
            return False
        if self.max_uses is not None and self.current_uses >= self.max_uses:
            return False
        return True


class ShoppingCartError(Exception):
    pass


class ShoppingCart:
    TAX_RATE = Decimal("0.0825")  # 8.25% sales tax

    def __init__(self):
        self._items: dict[str, CartItem] = {}
        self._discount: Optional[DiscountCode] = None

    @property
    def items(self) -> list[CartItem]:
        return list(self._items.values())

    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self._items.values())

    def add_item(self, product_id: str, name: str, price: float, quantity: int = 1, taxable: bool = True) -> CartItem:
        """Add an item to the cart, or increase quantity if it already exists."""
        if quantity <= 0:
            raise ShoppingCartError("Quantity must be positive")
        if price < 0:
            raise ShoppingCartError("Price cannot be negative")

        unit_price = Decimal(str(price))

        if product_id in self._items:
            self._items[product_id].quantity += quantity
        else:
            self._items[product_id] = CartItem(
                product_id=product_id,
                name=name,
                unit_price=unit_price,
                quantity=quantity,
                taxable=taxable,
            )
        return self._items[product_id]

    def remove_item(self, product_id: str) -> None:
        """Remove an item entirely from the cart."""
        if product_id not in self._items:
            raise ShoppingCartError(f"Product {product_id} not in cart")
        del self._items[product_id]

    def update_quantity(self, product_id: str, quantity: int) -> CartItem:
        """Set the quantity of an item. Removes the item if quantity is 0."""
        if product_id not in self._items:
            raise ShoppingCartError(f"Product {product_id} not in cart")
        if quantity < 0:
            raise ShoppingCartError("Quantity cannot be negative")
        if quantity == 0:
            self.remove_item(product_id)
            return None
        self._items[product_id].quantity = quantity
        return self._items[product_id]

    def apply_discount(self, discount: DiscountCode) -> Decimal:
        """Apply a discount code to the cart. Returns the discount amount."""
        if not discount.is_valid:
            raise ShoppingCartError("Discount code is expired or has reached max uses")

        subtotal = self.subtotal
        if subtotal < discount.min_order_amount:
            raise ShoppingCartError(
                f"Order minimum of ${discount.min_order_amount} not met "
                f"(current: ${subtotal})"
            )

        self._discount = discount
        return self._calculate_discount()

    def remove_discount(self) -> None:
        """Remove the currently applied discount."""
        self._discount = None

    @property
    def subtotal(self) -> Decimal:
        """Total before tax and discounts."""
        return sum(
            (item.subtotal for item in self._items.values()),
            Decimal("0"),
        )

    def _calculate_discount(self) -> Decimal:
        """Calculate the discount amount based on the applied code."""
        if not self._discount:
            return Decimal("0")

        subtotal = self.subtotal
        if self._discount.discount_type == DiscountType.PERCENTAGE:
            discount = subtotal * (self._discount.value / Decimal("100"))
        elif self._discount.discount_type == DiscountType.FIXED_AMOUNT:
            discount = min(self._discount.value, subtotal)
        else:
            discount = Decimal("0")

        return discount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def tax_amount(self) -> Decimal:
        """Calculate tax on taxable items after discount proportional allocation."""
        taxable_subtotal = sum(
            (item.subtotal for item in self._items.values() if item.taxable),
            Decimal("0"),
        )
        subtotal = self.subtotal
        if subtotal == 0:
            return Decimal("0")

        discount = self._calculate_discount()
        # Allocate discount proportionally across taxable vs non-taxable
        taxable_ratio = taxable_subtotal / subtotal if subtotal else Decimal("0")
        taxable_discount = discount * taxable_ratio
        taxable_after_discount = taxable_subtotal - taxable_discount

        tax = taxable_after_discount * self.TAX_RATE
        return tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def total(self) -> Decimal:
        """Final total: subtotal - discount + tax."""
        return self.subtotal - self._calculate_discount() + self.tax_amount

    def checkout_summary(self) -> dict:
        """Generate a summary dict suitable for an order confirmation."""
        return {
            "items": [
                {
                    "product_id": item.product_id,
                    "name": item.name,
                    "unit_price": float(item.unit_price),
                    "quantity": item.quantity,
                    "subtotal": float(item.subtotal),
                }
                for item in self._items.values()
            ],
            "subtotal": float(self.subtotal),
            "discount": float(self._calculate_discount()),
            "discount_code": self._discount.code if self._discount else None,
            "tax": float(self.tax_amount),
            "total": float(self.total),
            "item_count": self.item_count,
        }

    def clear(self) -> None:
        """Remove all items and discounts from the cart."""
        self._items.clear()
        self._discount = None
