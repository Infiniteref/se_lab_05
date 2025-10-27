# Reflection – Lab 5: Static Code Analysis

1. The easiest issues to fix were formatting and style warnings such as missing spaces or docstrings.  
   The hardest part was refactoring the program to remove the global variable and redesign it as a class.

2. Pylint gave minor false positives for missing docstrings in short functions.  
   Bandit also gave generic warnings that were resolved after adding safe file handling.

3. Static analysis tools like Pylint, Flake8, and Bandit should be part of CI pipelines or pre-commit hooks to ensure all code meets quality and security standards automatically.

4. After applying the fixes, the code became modular, secure, and easier to maintain.  
   File handling is now safe, and all major tool warnings were resolved.
