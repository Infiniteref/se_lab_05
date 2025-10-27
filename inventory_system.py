"""
Cleaned and fixed version of Inventory System
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# custom error type
class InventoryError(Exception):
    """Custom exception for inventory operations."""

    pass


class Inventory:
    """A class to manage inventory items safely."""

    def __init__(self):
        self._data: Dict[str, int] = {}

    def add_item(self, item: str, qty: int, logs: Optional[List[str]] = None) -> None:
        """Add an item safely with input validation."""
        if not isinstance(item, str) or not isinstance(qty, int):
            raise InventoryError("Invalid input types")
        if qty < 0:
            raise InventoryError("Quantity must be non-negative")
        self._data[item] = self._data.get(item, 0) + qty
        log_msg = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Added {qty} {item}"
        if logs is not None:
            logs.append(log_msg)
        logger.info(log_msg)

    def remove_item(self, item: str, qty: int) -> None:
        """Remove item safely."""
        if item not in self._data:
            raise InventoryError("Item not found")
        if qty <= 0:
            raise InventoryError("Quantity must be positive")
        if self._data[item] < qty:
            raise InventoryError("Insufficient quantity")
        self._data[item] -= qty
        if self._data[item] == 0:
            del self._data[item]
        logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Removed {qty} {item}"
        )

    def save_data(self, filename: str = "inventory.json") -> None:
        """Save inventory to a JSON file safely."""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2)
            logger.info(f"Inventory saved to {filename}")
        except OSError as e:
            logger.error(f"Failed to save inventory: {e}")

    def load_data(self, filename: str = "inventory.json") -> None:
        """Load inventory safely from a JSON file."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise InventoryError("Invalid file structure")
            self._data = data
            logger.info(f"Inventory loaded from {filename}")
        except FileNotFoundError:
            logger.warning(f"{filename} not found. Starting with empty inventory.")
        except json.JSONDecodeError:
            logger.error("Invalid JSON format.")

    def display(self) -> None:
        """Display all items in inventory."""
        print("Current inventory:", self._data)


def main():
    inv = Inventory()
    inv.add_item("apple", 10)
    inv.remove_item("apple", 3)
    inv.add_item("banana", 5)
    inv.save_data()
    inv.load_data()
    inv.display()


if __name__ == "__main__":
    main()
