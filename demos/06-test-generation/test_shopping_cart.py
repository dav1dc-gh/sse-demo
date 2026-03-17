"""Unit tests for the ShoppingCart class."""

import pytest
from datetime import date, timedelta
from decimal import Decimal

from shopping_cart import (
    CartItem,
    DiscountCode,
    DiscountType,
    ShoppingCart,
    ShoppingCartError,
)


@pytest.fixture
def cart():
    return ShoppingCart()


@pytest.fixture
def populated_cart(cart):
    cart.add_item("SKU1", "Widget", 10.00, quantity=2)
    cart.add_item("SKU2", "Gadget", 5.50)
    cart.add_item("SKU3", "Groceries", 3.00, taxable=False)
    return cart


@pytest.fixture
def percentage_discount():
    return DiscountCode(
        code="SAVE10",
        discount_type=DiscountType.PERCENTAGE,
        value=Decimal("10"),
    )


@pytest.fixture
def fixed_discount():
    return DiscountCode(
        code="FIVE_OFF",
        discount_type=DiscountType.FIXED_AMOUNT,
        value=Decimal("5.00"),
    )


# ── add_item ──────────────────────────────────────────────────────────────


class TestAddItem:
    def test_single_item(self, cart):
        item = cart.add_item("SKU1", "Widget", 9.99)
        assert item.product_id == "SKU1"
        assert item.name == "Widget"
        assert item.unit_price == Decimal("9.99")
        assert item.quantity == 1
        assert item.taxable is True

    def test_default_quantity_is_one(self, cart):
        cart.add_item("SKU1", "Widget", 5.00)
        assert cart.item_count == 1

    def test_explicit_quantity(self, cart):
        item = cart.add_item("SKU1", "Widget", 10.00, quantity=5)
        assert item.quantity == 5
        assert cart.item_count == 5

    def test_returns_cart_item(self, cart):
        result = cart.add_item("SKU1", "Widget", 3.50)
        assert isinstance(result, CartItem)

    def test_taxable_false(self, cart):
        item = cart.add_item("SKU1", "Groceries", 4.99, taxable=False)
        assert item.taxable is False

    def test_zero_price(self, cart):
        item = cart.add_item("FREE1", "Freebie", 0.00)
        assert item.unit_price == Decimal("0")

    def test_subtotal_reflects_price_times_quantity(self, cart):
        item = cart.add_item("SKU1", "Widget", 7.50, quantity=3)
        assert item.subtotal == Decimal("22.50")

    def test_existing_item_increases_quantity(self, cart):
        cart.add_item("SKU1", "Widget", 10.00, quantity=2)
        item = cart.add_item("SKU1", "Widget", 10.00, quantity=3)
        assert item.quantity == 5

    def test_existing_item_is_single_entry(self, cart):
        cart.add_item("SKU1", "Widget", 10.00)
        cart.add_item("SKU1", "Widget", 10.00)
        assert len(cart.items) == 1

    def test_existing_item_preserves_original_price(self, cart):
        cart.add_item("SKU1", "Widget", 10.00)
        item = cart.add_item("SKU1", "Widget", 15.00)
        assert item.unit_price == Decimal("10.00")

    def test_multiple_different_items(self, cart):
        cart.add_item("SKU1", "Widget", 10.00)
        cart.add_item("SKU2", "Gadget", 20.00)
        cart.add_item("SKU3", "Doohickey", 5.00)
        assert len(cart.items) == 3
        assert cart.item_count == 3

    def test_zero_quantity_raises(self, cart):
        with pytest.raises(ShoppingCartError, match="Quantity must be positive"):
            cart.add_item("SKU1", "Widget", 10.00, quantity=0)

    def test_negative_quantity_raises(self, cart):
        with pytest.raises(ShoppingCartError, match="Quantity must be positive"):
            cart.add_item("SKU1", "Widget", 10.00, quantity=-1)

    def test_negative_price_raises(self, cart):
        with pytest.raises(ShoppingCartError, match="Price cannot be negative"):
            cart.add_item("SKU1", "Widget", -5.00)

    def test_invalid_add_does_not_modify_cart(self, cart):
        with pytest.raises(ShoppingCartError):
            cart.add_item("SKU1", "Widget", -1.00)
        assert len(cart.items) == 0

    def test_float_price_converted_to_decimal(self, cart):
        item = cart.add_item("SKU1", "Widget", 19.99)
        assert isinstance(item.unit_price, Decimal)
        assert item.unit_price == Decimal("19.99")


# ── remove_item ───────────────────────────────────────────────────────────


class TestRemoveItem:
    def test_removes_existing_item(self, cart):
        cart.add_item("SKU1", "Widget", 10.00)
        cart.remove_item("SKU1")
        assert len(cart.items) == 0

    def test_remove_nonexistent_raises(self, cart):
        with pytest.raises(ShoppingCartError, match="not in cart"):
            cart.remove_item("FAKE")

    def test_remove_one_leaves_others(self, populated_cart):
        populated_cart.remove_item("SKU1")
        ids = [item.product_id for item in populated_cart.items]
        assert "SKU1" not in ids
        assert len(populated_cart.items) == 2


# ── update_quantity ───────────────────────────────────────────────────────


class TestUpdateQuantity:
    def test_update_increases_quantity(self, cart):
        cart.add_item("SKU1", "Widget", 10.00, quantity=1)
        item = cart.update_quantity("SKU1", 5)
        assert item.quantity == 5

    def test_update_decreases_quantity(self, cart):
        cart.add_item("SKU1", "Widget", 10.00, quantity=5)
        item = cart.update_quantity("SKU1", 2)
        assert item.quantity == 2

    def test_update_to_zero_removes_item(self, cart):
        cart.add_item("SKU1", "Widget", 10.00)
        result = cart.update_quantity("SKU1", 0)
        assert result is None
        assert len(cart.items) == 0

    def test_update_negative_raises(self, cart):
        cart.add_item("SKU1", "Widget", 10.00)
        with pytest.raises(ShoppingCartError, match="Quantity cannot be negative"):
            cart.update_quantity("SKU1", -1)

    def test_update_nonexistent_raises(self, cart):
        with pytest.raises(ShoppingCartError, match="not in cart"):
            cart.update_quantity("FAKE", 1)


# ── subtotal ──────────────────────────────────────────────────────────────


class TestSubtotal:
    def test_empty_cart(self, cart):
        assert cart.subtotal == Decimal("0")

    def test_single_item(self, cart):
        cart.add_item("SKU1", "Widget", 10.00, quantity=3)
        assert cart.subtotal == Decimal("30.00")

    def test_multiple_items(self, populated_cart):
        # 10*2 + 5.50*1 + 3*1 = 28.50
        assert populated_cart.subtotal == Decimal("28.50")


# ── apply_discount / remove_discount ──────────────────────────────────────


class TestDiscount:
    def test_percentage_discount(self, cart, percentage_discount):
        cart.add_item("SKU1", "Widget", 100.00)
        amount = cart.apply_discount(percentage_discount)
        assert amount == Decimal("10.00")

    def test_fixed_discount(self, cart, fixed_discount):
        cart.add_item("SKU1", "Widget", 100.00)
        amount = cart.apply_discount(fixed_discount)
        assert amount == Decimal("5.00")

    def test_fixed_discount_capped_at_subtotal(self, cart):
        cart.add_item("SKU1", "Widget", 3.00)
        big_discount = DiscountCode(
            code="BIG", discount_type=DiscountType.FIXED_AMOUNT, value=Decimal("50")
        )
        amount = cart.apply_discount(big_discount)
        assert amount == Decimal("3.00")

    def test_expired_discount_raises(self, cart):
        cart.add_item("SKU1", "Widget", 10.00)
        expired = DiscountCode(
            code="OLD",
            discount_type=DiscountType.PERCENTAGE,
            value=Decimal("10"),
            expires_at=date.today() - timedelta(days=1),
        )
        with pytest.raises(ShoppingCartError, match="expired"):
            cart.apply_discount(expired)

    def test_max_uses_reached_raises(self, cart):
        cart.add_item("SKU1", "Widget", 10.00)
        used_up = DiscountCode(
            code="DONE",
            discount_type=DiscountType.PERCENTAGE,
            value=Decimal("10"),
            max_uses=5,
            current_uses=5,
        )
        with pytest.raises(ShoppingCartError, match="expired|max uses"):
            cart.apply_discount(used_up)

    def test_min_order_not_met_raises(self, cart):
        cart.add_item("SKU1", "Widget", 5.00)
        discount = DiscountCode(
            code="MIN50",
            discount_type=DiscountType.PERCENTAGE,
            value=Decimal("10"),
            min_order_amount=Decimal("50"),
        )
        with pytest.raises(ShoppingCartError, match="minimum"):
            cart.apply_discount(discount)

    def test_remove_discount(self, cart, percentage_discount):
        cart.add_item("SKU1", "Widget", 100.00)
        cart.apply_discount(percentage_discount)
        cart.remove_discount()
        assert cart.total == cart.subtotal + cart.tax_amount


# ── tax_amount ────────────────────────────────────────────────────────────


class TestTax:
    def test_empty_cart_zero_tax(self, cart):
        assert cart.tax_amount == Decimal("0")

    def test_taxable_item(self, cart):
        cart.add_item("SKU1", "Widget", 100.00)
        # 100 * 0.0825 = 8.25
        assert cart.tax_amount == Decimal("8.25")

    def test_non_taxable_item_no_tax(self, cart):
        cart.add_item("SKU1", "Groceries", 100.00, taxable=False)
        assert cart.tax_amount == Decimal("0")

    def test_mixed_taxable_items(self, cart):
        cart.add_item("SKU1", "Widget", 100.00, taxable=True)
        cart.add_item("SKU2", "Food", 50.00, taxable=False)
        # Only the 100 is taxable → 100 * 0.0825 = 8.25
        assert cart.tax_amount == Decimal("8.25")

    def test_tax_with_percentage_discount(self, cart, percentage_discount):
        cart.add_item("SKU1", "Widget", 100.00, taxable=True)
        cart.apply_discount(percentage_discount)  # 10% off
        # Taxable after discount = 90 → 90 * 0.0825 = 7.43 (rounded)
        assert cart.tax_amount == Decimal("7.43")


# ── total ─────────────────────────────────────────────────────────────────


class TestTotal:
    def test_empty_cart(self, cart):
        assert cart.total == Decimal("0")

    def test_single_taxable_item(self, cart):
        cart.add_item("SKU1", "Widget", 100.00)
        # 100 + 8.25 = 108.25
        assert cart.total == Decimal("108.25")

    def test_total_with_discount(self, cart, percentage_discount):
        cart.add_item("SKU1", "Widget", 100.00)
        cart.apply_discount(percentage_discount)  # 10% off → discount 10
        # 100 - 10 + 7.43 = 97.43
        assert cart.total == Decimal("97.43")


# ── checkout_summary ──────────────────────────────────────────────────────


class TestCheckoutSummary:
    def test_empty_cart_summary(self, cart):
        summary = cart.checkout_summary()
        assert summary["items"] == []
        assert summary["subtotal"] == 0.0
        assert summary["discount"] == 0.0
        assert summary["discount_code"] is None
        assert summary["tax"] == 0.0
        assert summary["total"] == 0.0
        assert summary["item_count"] == 0

    def test_summary_structure(self, populated_cart):
        summary = populated_cart.checkout_summary()
        assert len(summary["items"]) == 3
        assert summary["item_count"] == 4  # 2 + 1 + 1
        assert summary["subtotal"] == float(populated_cart.subtotal)
        assert summary["tax"] == float(populated_cart.tax_amount)
        assert summary["total"] == float(populated_cart.total)

    def test_summary_item_fields(self, cart):
        cart.add_item("SKU1", "Widget", 10.00, quantity=2)
        item_data = cart.checkout_summary()["items"][0]
        assert item_data["product_id"] == "SKU1"
        assert item_data["name"] == "Widget"
        assert item_data["unit_price"] == 10.0
        assert item_data["quantity"] == 2
        assert item_data["subtotal"] == 20.0

    def test_summary_includes_discount_code(self, cart, percentage_discount):
        cart.add_item("SKU1", "Widget", 100.00)
        cart.apply_discount(percentage_discount)
        summary = cart.checkout_summary()
        assert summary["discount_code"] == "SAVE10"
        assert summary["discount"] == 10.0


# ── clear ─────────────────────────────────────────────────────────────────


class TestClear:
    def test_clear_removes_all_items(self, populated_cart):
        populated_cart.clear()
        assert len(populated_cart.items) == 0
        assert populated_cart.item_count == 0

    def test_clear_removes_discount(self, cart, percentage_discount):
        cart.add_item("SKU1", "Widget", 100.00)
        cart.apply_discount(percentage_discount)
        cart.clear()
        assert cart.checkout_summary()["discount_code"] is None

    def test_clear_resets_totals(self, populated_cart):
        populated_cart.clear()
        assert populated_cart.subtotal == Decimal("0")
        assert populated_cart.tax_amount == Decimal("0")
        assert populated_cart.total == Decimal("0")
