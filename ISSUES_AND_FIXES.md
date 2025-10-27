# Issues Identified and Fixes Applied

| Issue | Type | Line(s) | Description | Fix Approach |
|--------|------|----------|-------------|---------------|
| Mutable default argument | Bug | ~45 | Used `logs=[]`, causing shared data between calls. | Changed default to `None` and initialized inside the function. |
| Global variable usage | Design | Whole file | Used global `stock_data`, causing side effects. | Replaced with `Inventory` class using instance variables. |
| Broad exception handling | Logic | ~90 | Used `except:` that hid real errors. | Added specific exceptions (`InventoryError`, `ItemNotFoundError`, etc.). |
| Unsafe file handling | Security | ~130 | Used `open()` without context manager. | Used `with open()` and added error handling. |
| Missing type hints and documentation | Style | Multiple | Functions lacked type hints and docstrings. | Added type hints and docstrings. |
| No input validation | Logic | ~60 | Accepted invalid quantities. | Added validation and raised `InventoryError`. |
