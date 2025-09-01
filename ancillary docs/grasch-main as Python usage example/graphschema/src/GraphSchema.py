from __future__ import annotations
import sys

# from grasch_exceptions import (GraphSchemaTypeInitError)
# from data_types import Datatype, AtomicPropertyDatatype, DatatypeCollection
# from content_type import *
from graph_type import *
# from lattice import *

def basicFunctionalTests():

    propertyType_cats1 = PropertyType(name="cats", datatype=STRING_LIST)
    propertyType_cats2 = PropertyType(name="cats", datatype=STRING_LIST)
    print("1   \n{propertyType_cats1}\n{propertyType_cats2}")
    contentTypeIdentifier = LabelsRecordType(['Pets'])
    mandatoryPropertyTypes = FlatPropertyTypes([propertyType_cats1, propertyType_cats2])

    petsKeyedContentType = KeyedContentType(identifierLabels=contentTypeIdentifier, mandatoryPropertyTypes=mandatoryPropertyTypes)
    print("2   ", petsKeyedContentType)
    petsNamedContentType = NamedContentType('Pets', mandatoryPropertyTypes=mandatoryPropertyTypes)
    print("3   ", petsNamedContentType)
    # petsNodeType = NodeType(petsContentType)
    # print("4   ", petsNodeType)
    # if isinstance(petsNodeType, ElementType): print("It's an node type")
    # print("5a  ", petsNodeType.elementType())
    # print("5b  ", petsNodeType.elementType().contentType())
    # petsCoexistWithPetsEdgeType = EdgeType(contentType=ContentType(identifierLabels={"COEXISTS_WITH"}),
    #                                        endpoints=(petsContentType, petsContentType))
    # print("6   ", petsCoexistWithPetsEdgeType)

def tryItOut():
    pass

    # piling enums on top of each other, and testing their supertypes
    # class A(Enum):
    #     AK = 1
    #
    # class B(A):
    #     BK = 2
    #
    # class C(B):
    #     CK = 3
    #     CK1 = 4
    #     CK2 = 5
    #
    # a: A = A.AK
    # b: B = B.BK
    # c: C = C.CK1

    #print(isinstance(C.CK1, A))  # Should print True since C is a subclass of A

def contentTypePartialOrdering():
    pass
    # STRING = Datatype(AtomicPropertyDatatypes.STRING)
    # STRING_LIST = Datatype(AtomicPropertyDatatypes.STRING, DatatypeCollection.LIST)
    # INTEGER = Datatype(AtomicPropertyDatatypes.INTEGER)
    #
    # propertyType_owner = PropertyType(name="owner", datatype=STRING)
    # propertyType_city = PropertyType(name="city", datatype=STRING)
    # propertyType_cats = PropertyType(name="cats", datatype=STRING_LIST)
    # propertyType_dogs = PropertyType(name="dogs", datatype=STRING_LIST)
    # propertyType_ferrets = PropertyType(name="ferrets", datatype=STRING_LIST)
    # propertyType_snakes = PropertyType(name="snakes", datatype=STRING_LIST)
    #
    # petsContentType = ContentType(identifierLabels={"Pets"}, mandatoryPropertyTypes={propertyType_owner},
    #                               optionalPropertyTypes={propertyType_cats, propertyType_dogs})
    #
    # extendedPetsContentType = ContentType(identifierLabels={"Pets", "Extended"},
    #                                       mandatoryPropertyTypes={propertyType_owner, propertyType_city},
    #                                       optionalPropertyTypes={propertyType_cats, propertyType_dogs,
    #                                                              propertyType_ferrets, propertyType_snakes})
    # print(repr(petsContentType))
    # print(repr(extendedPetsContentType))
    # if petsContentType < extendedPetsContentType: print("a small but critical things appears to have worked")


if __name__ == "__main__":
    basicFunctionalTests()
    # crudeInitialTests()
    # contentTypePartialOrdering()
    sys.exit()

def comparisonOfRecordsExample():
    pass

    # a123 = RecordType(sortedSet={1, 2, 3})
    # a456 = RecordType(sortedSet={1, 2, 3})
    # a12 = RecordType(sortedSet={1, 2})
    # a1245 = RecordType(sortedSet={1, 2, 4, 5})
    # b123 = RecordType(sortedSet={1, 2, 3})
    # compareRecordTypes(a12, a123)
    # compareRecordTypes(a123, b123)
    # compareRecordTypes(a12, a1245)
    # compareRecordTypes(a123, a456)

def compareRecordTypes(this: FlatRecordType, that: FlatRecordType):
    print(this, ":", that)
    if this == that:
        print("Equal")
    else:
        print("Not equal")
    if this < that:
        print("Less than")
    else:
        print("Not less than")
