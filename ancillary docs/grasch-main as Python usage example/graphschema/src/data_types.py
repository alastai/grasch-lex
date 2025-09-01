from __future__ import annotations
from typing import Tuple

from fundamental import *

class AtomicDatatypeEnum:
    pass

class AtomicLabelDatatypeEnum(AtomicDatatypeEnum, Enum):
    LABEL = "LABEL"

class AtomicPropertyDatatypeEnum(AtomicDatatypeEnum, Enum):
    BOOLEAN = "BOOLEAN"
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    JSON = "JSON"

class DatatypeCollection(Enum):
    SCALAR = "SCALAR"
    LIST = "LIST"
    SET = "SET"

@total_ordering
class AtomicDatatype(OrderableABC):
    def __init__(self, atomicDatatypeEnum: AtomicDatatypeEnum):
        self.__atomicDatatypeEnum = atomicDatatypeEnum

    @property
    def atomicDatatypeEnum(self) -> AtomicDatatypeEnum:
        self.__atomicDatatypeEnum

    def __hash__(self):
        return hash(self.__atomicDatatypeEnum)

    def __str__(self):
        return f"{self.__class__.__name__}{': '}{self.__atomicDatatypeEnum}"

    def __repr__(self) -> object:
        return f"{self.__class__.__name__}\
    {', atomicDatatypeEnum='}{repr(self.atomicDatatypeEnum)}\
    {')'}"
    
@total_ordering
class Datatype(OrderableABC):
    def __init__(self,
                 atomicDatatype: AtomicDatatype,
                 collectionType: DatatypeCollection = DatatypeCollection.SCALAR):
        self.__atomicDatatype = atomicDatatype
        self.__collectionType = collectionType

    @property
    def atomicDatatype(self) -> AtomicDatatype:
        return self.__atomicDatatype

    @property
    def collectionType(self) -> DatatypeCollection:
        return self.__collectionType

    def __hash__(self):
        return hash((self.atomicDatatype, self.collectionType))

    def __eq__(self, other: Datatype):
        return (self.atomicDatatype(), self.collectionType()) == (other.atomicDatatype(), other.collectionType())

    def __lt__(self, other):
        return False # they are never orderable

    def __str__(self):
        return f"{self.__class__.__name__}{': '}{(self.atomicDatatype, self.collectionType)}"

    def __repr__(self) -> object:
        return f"{self.__class__.__name__}\
{'(name='}{repr(self.atomicDatatype)}\
{', datatype='}{repr(self.collectionType)}\
{')'}"

    class Compatible:
        def __init__(Compatible_self,
                     firstDatatype: Datatype,
                     secondDatatype: Datatype,
                     leastCommonSupertype: Datatype):
            # if first and second are equal then we report the first as the LCS

            Compatible_self.__firstDatatype = firstDatatype
            Compatible_self.__secondDatatype = secondDatatype
            Compatible_self.__leastCommonSupertype = leastCommonSupertype

        @property
        def firstDatatype(Compatible_self) -> Datatype:
            return Compatible_self.__firstDatatype

        @property
        def secondDatatype(Compatible_self) -> Datatype:
            return Compatible_self.__secondDatatype

        @property
        def equal(Compatible_self) -> bool:
            return Compatible_self.__firstDatatype == Compatible_self.__secondDatatype

        @property
        def leastCommonSupertype(Compatible_self) -> Datatype:
            return Compatible_self.__leastCommonSupertype

        # TODO JSON dumping and loading

    class Incompatible:
        def __init__(Incompatible_self,
                     firstDatatype: Datatype,
                     secondDatatype: Datatype):
            Incompatible_self.__firstDatatype = firstDatatype
            Incompatible_self.__secondDatatype = secondDatatype

        @property
        def incompatibleDatatypes(Incompatible_self) -> Tuple[Datatype, Datatype] | None:
            return Incompatible_self.__firstDatatype, Incompatible_self.__secondDatatype

        # TODO JSON dumping and loading

    def compatibleWith(self, other: Datatype) -> Datatype.Compatible | Datatype.Incompatible:
        # for the moment we equate compatibility of datatypes with equality of datatypes
        # in the fullness of time this is where we need to implement the rules of GQL:2024
        # 22.17 through 22.19 on value type compatibility.

        if not self.atomicDatatype == other.atomicDatatype:
            return Datatype.Incompatible(self, other)

        return Datatype.Compatible(self, other, self)

class LabelDatatype(AtomicDatatype):
    def __init__(self):
        atomicDatatype = AtomicDatatype(AtomicLabelDatatypeEnum.LABEL)
        super().__init__(atomicDatatype)

    # def __hash__(self):
    #     return hash(AtomicLabelDatatypeEnum.LABEL)
        
LABEL = LabelDatatype()

class PropertyDatatype(AtomicDatatype):
    def __init__(self, atomicPropertyDatatypeEnum: AtomicPropertyDatatypeEnum):
        atomicDatatype = AtomicDatatype(atomicPropertyDatatypeEnum)
        self.__atomicPropertyDatatypeEnum = atomicPropertyDatatypeEnum
        super().__init__(atomicDatatype)

    # def __hash__(self):
    #     return hash(self.__atomicPropertyDatatypeEnum)
        
BOOLEAN_PROPERTY_TYPE: PropertyDatatype = PropertyDatatype(AtomicPropertyDatatypeEnum.BOOLEAN)
STRING_PROPERTY_TYPE: PropertyDatatype = PropertyDatatype(AtomicPropertyDatatypeEnum.STRING)
INTEGER_PROPERTY_TYPE: PropertyDatatype = PropertyDatatype(AtomicPropertyDatatypeEnum.INTEGER)
FLOAT_PROPERTY_TYPE: PropertyDatatype = PropertyDatatype(AtomicPropertyDatatypeEnum.FLOAT)
DATE_PROPERTY_TYPE: PropertyDatatype = PropertyDatatype(AtomicPropertyDatatypeEnum.DATE)
TIME_PROPERTY_TYPE: PropertyDatatype = PropertyDatatype(AtomicPropertyDatatypeEnum.TIME)
DATETIME_PROPERTY_TYPE: PropertyDatatype = PropertyDatatype(AtomicPropertyDatatypeEnum.DATETIME)

BOOLEAN: Datatype = Datatype(BOOLEAN_PROPERTY_TYPE)
STRING: Datatype = Datatype(STRING_PROPERTY_TYPE)
INTEGER: Datatype = Datatype(INTEGER_PROPERTY_TYPE)
FLOAT: Datatype = Datatype(FLOAT_PROPERTY_TYPE)
DATE: Datatype = Datatype(DATE_PROPERTY_TYPE)
TIME: Datatype = Datatype(TIME_PROPERTY_TYPE)
DATETIME: Datatype = Datatype(DATETIME_PROPERTY_TYPE)

BOOLEAN_LIST: Datatype = Datatype(BOOLEAN_PROPERTY_TYPE, DatatypeCollection.LIST)
STRING_LIST: Datatype = Datatype(STRING_PROPERTY_TYPE, DatatypeCollection.LIST)
INTEGER_LIST: Datatype = Datatype(INTEGER_PROPERTY_TYPE, DatatypeCollection.LIST)
FLOAT_LIST: Datatype = Datatype(FLOAT_PROPERTY_TYPE, DatatypeCollection.LIST)
DATE_LIST: Datatype = Datatype(DATE_PROPERTY_TYPE, DatatypeCollection.LIST)
TIME_LIST: Datatype = Datatype(TIME_PROPERTY_TYPE, DatatypeCollection.LIST)
DATETIME_LIST: Datatype = Datatype(DATETIME_PROPERTY_TYPE, DatatypeCollection.LIST)

BOOLEAN_SET: Datatype = Datatype(BOOLEAN_PROPERTY_TYPE, DatatypeCollection.SET)
STRING_SET: Datatype = Datatype(STRING_PROPERTY_TYPE, DatatypeCollection.SET)
INTEGER_SET: Datatype = Datatype(INTEGER_PROPERTY_TYPE, DatatypeCollection.SET)
FLOAT_SET: Datatype = Datatype(FLOAT_PROPERTY_TYPE, DatatypeCollection.SET)
DATE_SET: Datatype = Datatype(DATE_PROPERTY_TYPE, DatatypeCollection.SET)
TIME_SET: Datatype = Datatype(TIME_PROPERTY_TYPE, DatatypeCollection.SET)
DATETIME_SET: Datatype = Datatype(DATETIME_PROPERTY_TYPE, DatatypeCollection.SET)

