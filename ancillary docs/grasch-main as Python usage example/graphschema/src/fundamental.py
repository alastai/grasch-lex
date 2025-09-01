from __future__ import annotations

from abc import ABC, abstractmethod
from functools import total_ordering
from typing import Protocol
from enum import Enum

class Named:
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

class ReportableABC(ABC):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self) -> object:
        pass

# @total_ordering is a misnomer. It should be called something like "InferComparators". If you implement __lt__
# such that it may return False (or NotImplemented) then the result is a partial order: something might be
# not equal and not less than, and therefore be "out of order" altogether.

@total_ordering
class OrderableABC(ReportableABC):
    class Relation(Enum):
        EQUAL = "EQUAL"
        LESS_THAN = "LESS_THAN"
        INCOMPARABLE = "INCOMPARABLE"

    class Order(Enum):
        PARTIAL = "PARTIAL"
        STRICT = "STRICT"
        TOTAL = "TOTAL"
        NONE = "NONE"

    #def __hash__(self):
    #    pass

    def __eq__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __comparable__(self, other) -> OrderableABC.Relation:
        if self.__eq__(other):
            return OrderableABC.Relation.EQUAL
        else:
            if self.__lt__(other):
                return OrderableABC.Relation.LESS_THAN
            else:
                return OrderableABC.Relation.INCOMPARABLE

    # for a given implementation of this ABC, if all three conditions above can result when
    # attempting to compare an object with another object of the same implementation, then
    # an instance of the class may be partially ordered; if the first (EQUAL) can never result
    # then every instance of the class is strictly ordered; if the third branch (INCOMPARABLE)
    # can never be reached then every instance is totally ordered. If for any two objects of any
    # instances of the class the result of an attempted comparison is INCOMPARABLE then the class
    # is unorderable.

    # An implementation should report the orderability of its instances using the method above, and should
    # test to ensure that it can be PARTIAL or TOTAL, and whether it is STRICT. When such a test passes
    # the method below should be re-implemented.

    # TODO sort out the orderability reporting
    # @abstractmethod
    # def hasOrder(self) -> [Orderable.Order]:
    #     return list(Orderable.Order.NONE)  # this has to be overridden: see comment above. An Orderable is orderable.