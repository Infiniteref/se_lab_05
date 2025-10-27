I fixed four issues; key ones:

Global mutable state → Inventory class (encapsulates state so tests won’t interfere).

Mutable default argument (logs=[]) removed; now logs: Optional[list].

Bare except replaced by specific exceptions and explicit InventoryError hierarchy.

Unsafe file I/O replaced with with open(...) and JSON validation/error handling.