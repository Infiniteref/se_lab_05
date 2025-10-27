"""
inventory_system.py
Cleaned and refactored inventory manager suitable for the Lab 5 static analysis exercise.
Fixes applied:
 - Encapsulated global mutable state into Inventory class (no module-level mutable dict).
 - Removed mutable default argument.
 - Used safe file I/O (with open) and JSON serialization handling.
 - Added input validation and explicit exceptions instead of bare except.
 - Removed use of eval and other unsafe constructs.
 - Added logging and type hints.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)
# Basic logging configuration (can be reconfigured by caller)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class InventoryError(Exception):
    """Base class for inventory related errors."""


class ItemNotFoundError(InventoryError):
    pass


class InvalidItemError(InventoryError):
    pass


class Inventory:
    def __init__(self, initial: Optional[Dict[str, int]] = None):
        """
        initial: optional mapping from item name -> quantity (quantities must be ints >= 0)
        """
        self._data: Dict[str, int] = {}
        if initial:
            for k, v in initial.items():
                self.add_item(k, v)

    def add_item(self, item: str, qty: int, logs: Optional[List[str]] = None) -> None:
        """
        Add qty of item to inventory. qty must be an integer (can be positive).
        logs: optional list to append human-readable log lines.
        """
        if not isinstance(item, str) or not item:
            raise InvalidItemError("item name must be a non-empty string")
        if not isinstance(qty, int):
            raise InvalidItemError("qty must be an integer")
        if qty < 0:
            # Negative addition is confusing — treat it as an error (explicit)
            raise InvalidItemError(
                "qty must be non-negative; use remove_item to reduce quantity"
            )

        previous = self._data.get(item, 0)
        self._data[item] = previous + qty
        log_line = f"{datetime.now().isoformat()}: Added {qty} of {item} (was {previous}, now {self._data[item]})"
        logger.info(log_line)
        if logs is not None:
            logs.append(log_line)

    def remove_item(self, item: str, qty: int) -> None:
        """
        Remove qty from item. Raises ItemNotFoundError if item missing,
        raises InvalidItemError if qty invalid, or InventoryError if insufficient qty.
        """
        if not isinstance(item, str) or not item:
            raise InvalidItemError("item name must be a non-empty string")
        if not isinstance(qty, int):
            raise InvalidItemError("qty must be an integer")
        if qty <= 0:
            raise InvalidItemError("qty to remove must be positive")

        if item not in self._data:
            raise ItemNotFoundError(f"Item '{item}' not found")

        if self._data[item] < qty:
            raise InventoryError(
                f"Insufficient quantity of '{item}' (have {self._data[item]}, need {qty})"
            )

        self._data[item] -= qty
        logger.info(
            "%s: Removed %d of %s (remaining %d)",
            datetime.now().isoformat(),
            qty,
            item,
            self._data[item],
        )
        if self._data[item] == 0:
            # remove key when qty reaches 0
            self._data.pop(item, None)

    def get_qty(self, item: str) -> int:
        """Return quantity (0 if missing)."""
        if not isinstance(item, str) or not item:
            raise InvalidItemError("item name must be a non-empty string")
        return self._data.get(item, 0)

    def check_low_items(self, threshold: int = 5) -> List[str]:
        """Return list of items whose quantity is strictly less than threshold."""
        if not isinstance(threshold, int) or threshold < 0:
            raise InvalidItemError("threshold must be a non-negative integer")
        return [k for k, v in self._data.items() if v < threshold]

    def to_dict(self) -> Dict[str, int]:
        """Return a shallow copy of inventory data."""
        return dict(self._data)

    def print_report(self) -> None:
        """Nicely print the inventory."""
        print("Items Report")
        if not self._data:
            print("  (no items)")
            return
        for name, qty in sorted(self._data.items()):
            print(f"  {name} -> {qty}")

    def save(self, filename: str = "inventory.json") -> None:
        """Save inventory to filename using safe file I/O."""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
            logger.info("Inventory saved to %s", filename)
        except OSError as e:
            logger.exception("Failed to save inventory to %s: %s", filename, e)
            raise

    def load(self, filename: str = "inventory.json") -> None:
        """Load inventory from filename. Existing in-memory data will be replaced."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise InventoryError("Inventory file did not contain a JSON object")
            # Validate contents: keys -> str, values -> int >= 0
            sanitized: Dict[str, int] = {}
            for k, v in data.items():
                if not isinstance(k, str):
                    raise InventoryError("Invalid item name in file (must be string)")
                if not isinstance(v, int) or v < 0:
                    raise InventoryError(
                        "Invalid quantity in file (must be non-negative integer)"
                    )
                sanitized[k] = v
            self._data = sanitized
            logger.info("Inventory loaded from %s", filename)
        except FileNotFoundError:
            logger.warning(
                "Inventory file %s not found — starting with empty inventory", filename
            )
        except json.JSONDecodeError as e:
            logger.exception("Inventory file %s is not valid JSON: %s", filename, e)
            raise


def main() -> None:
    inv = Inventory()
    # Example usage that is valid and safe
    try:
        inv.add_item("apple", 10)
        # valid removal
        inv.remove_item("apple", 3)
        # gracefully handle missing item
        try:
            inv.remove_item("orange", 1)
        except ItemNotFoundError:
            logger.info("Tried to remove 'orange' but it was not present — continuing")

        # invalid calls are now explicit errors (we do not hide them)
        # inv.add_item("banana", -2)  # would raise InvalidItemError
        # inv.add_item(123, "ten")    # would raise InvalidItemError

        print("Apple stock:", inv.get_qty("apple"))
        print("Low items:", inv.check_low_items(5))
        inv.save()  # write to inventory.json
        inv.load()  # read back (safe)
        inv.print_report()
    except InventoryError as e:
        logger.error("Inventory operation failed: %s", e)


if __name__ == "__main__":
    main()
