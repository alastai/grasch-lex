"""
Constraint system for LEX extensions.
"""

from typing import List


class KeyConstraint:
    """LEX key constraint for element types"""
    def __init__(self, element_type: str, key_attributes: List[str]):
        self.element_type = element_type
        self.key_attributes = key_attributes