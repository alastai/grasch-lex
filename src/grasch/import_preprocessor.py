#!/usr/bin/env python3
"""
DEPRECATED: This module has been renamed to canonicalizing_preprocessor.py

This file is kept for backward compatibility only.
Please update your imports to use canonicalizing_preprocessor instead.
"""

import warnings
from src.grasch.canonicalizing_preprocessor import *

warnings.warn(
    "import_preprocessor is deprecated and will be removed in a future version. "
    "Please use canonicalizing_preprocessor instead.",
    DeprecationWarning,
    stacklevel=2
)
