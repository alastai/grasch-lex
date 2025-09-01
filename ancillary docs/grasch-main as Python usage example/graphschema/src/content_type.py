from __future__ import annotations

from typing import List, Set, FrozenSet

from pydantic import BaseModel
from sortedcontainers import SortedDict, SortedSet

from data_types import *
from grasch_exceptions import *


@total_ordering
class AttributeType(Named, OrderableABC):
    def __init__(self, name: str, datatype: Datatype):
        # if type(self) is AttributeType:
        #     raise GraphSchemaTypeInitError(self.__class__.__name__,
        #         "is an abstract class and cannot be instantiated directly: use Label or PropertyType.")
        Named.__init__(self, name)
        self.__datatype = datatype

    @property
    def datatype(self) -> Datatype:
        return self.__datatype

    def __hash__(self):
        return hash((self.name, self.datatype))

    def __eq__(self, other: AttributeType):
        return (self.name, self.datatype) == (other.name, other.datatype)

    def __lt__(self, other: AttributeType):
        return False  # can never be ordered

    def __str__(self):
        return f"{self.__class__.__name__}{': '}\
                 {(self.name, str(self.datatype))}"

    def __repr__(self) -> object:
        return f"{'a'}{'b'}{self.__class__.__name__}\
                 {'(name='}{repr(self.name)}\
                 {', datatype='}{repr(self.datatype)}\
                 {')'}"

    class Compatible:
        def __init__(Compatible_self,
                     name: str,
                     firstDatatype: Datatype,
                     secondDatatype: Datatype,
                     leastCommonSupertype: Datatype):
            # if first and second are equal then we report the first as the LCS

            Compatible_self.__name = name
            Compatible_self.__firstDatatype = firstDatatype
            Compatible_self.__secondDatatype = secondDatatype
            Compatible_self.__leastCommonSupertype = leastCommonSupertype

        @property
        def name(Compatible_self) -> str:
            return Compatible_self.__name

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
                     firstName: str,
                     secondName: str,
                     firstDatatype: Datatype = None,
                     secondDatatype: Datatype = None):
            Incompatible_self.__firstName = firstName
            Incompatible_self.__secondName = secondName
            Incompatible_self.__firstDatatype = firstDatatype
            Incompatible_self.__secondDatatype = secondDatatype

        @property
        def differentNames(Incompatible_self) -> Tuple[str, str] | None:
            return Incompatible_self.__firstName, Incompatible_self.__secondName

        @property
        def incompatibleDatatypes(Incompatible_self) -> Tuple[Datatype, Datatype] | None:
            return Incompatible_self.__firstDatatype, Incompatible_self.__secondDatatype

        # TODO JSON dumping and loading

    def compatibleWith(self, other: AttributeType) -> AttributeType.Compatible | AttributeType.Incompatible:
        if not self.name == other.name:
            return AttributeType.Incompatible(self.name, other.name)

        datatypeCompatibility: Datatype.Compatible | Datatype.Incompatible = self.datatype.compatibleWith(
            other.datatype)
        if isinstance(datatypeCompatibility, Datatype.Compatible):
            return AttributeType.Compatible(self.name, self.datatype, other.datatype,
                                            datatypeCompatibility.leastCommonSupertype)

        return AttributeType.Incompatible(self.name, other.name, self.datatype, other.datatype)


class RecordTypeABC(OrderableABC):
    pass


class FlatRecordType(RecordTypeABC, SortedDict[str, Datatype]):
    # This class ensures that sets of labels or of property types have distinct names

    def __init__(self, attributeTypes: FrozenSet[AttributeType]):
        duplicateAttributeTypeNames = self.attributeTypesWithDuplicateNames(attributeTypes)
        if duplicateAttributeTypeNames:
            raise DuplicateNameError("{Duplicate AttributeType names}")  # TODO need to store the duplicate list etc
        else:
            # RecordType is just a marker, no __init__ to call
            SortedDict.__init__(self,
                                ((attributeType.name, attributeType.datatype) for attributeType in attributeTypes))

    @staticmethod
    def attributeTypesWithDuplicateNames(attributeTypes: FrozenSet[AttributeType]) -> List[AttributeType]:
        setOfNames: Set[str] = set()
        duplicateNames: List[AttributeType] = []  # Use a Counter, to improve reporting
        for attributeType in attributeTypes:
            memberName = attributeType.name
            if memberName in setOfNames:
                duplicateNames.append(attributeType)
            else:
                setOfNames.add(memberName)
        return duplicateNames

    @property
    def attributes(self) -> [AttributeType]:
        return [AttributeType(key, value) for key, value in super().items()]

    @property
    def attributeNames(self) -> SortedSet[str]:
        return SortedSet(self.keys())

    @property
    def isEmpty(self) -> bool:
        return True if 0 == len(self) else False

    @property
    def isSingleton(self) -> bool:
        return True if 1 == len(self) else False

    @property
    def singletonMemberName(self) -> str | None:
        return self.attributeNames[0] if self.isSingleton else None

    def __add__(self, other: FlatRecordType):
        combinedAttributeTypes: Set[AttributeType] = set()
        selfNames = self.attributeNames
        otherNames = other.attributeNames
        if selfNames.isdisjoint(otherNames):
            #combined_items = self.items() | other.items()
            print(self.items())
            combined_items = set(self.items())
            print(combined_items)
            for item in combined_items:
                attributeType: AttributeType is None
                if item[1] is LabelDatatype:
                    attributeType = Label(item[0])
                else:
                    attributeType = PropertyType(item[0], item[1])
                combinedAttributeTypes.add(attributeType)
                return FlatRecordType(frozenset(combinedAttributeTypes))
        else:
            sharedNames = self.attributeNames.intersection(other.attributeNames)
            for sharedName in sharedNames:
                compatibility = self[sharedName].compatibleWith(other[sharedName])
                if isinstance(compatibility, Datatype.Compatible):
                    combinedAttributeTypes.add(AttributeType(sharedName, compatibility.leastCommonSupertype))
                else:
                    reason = f"PropertyType {sharedName} has incompatible datatypes {self[sharedName]} and {other[sharedName]}"
                    raise IncompatibleDatatypesError(reason)
            # all shared names processed, now remove shared names items from self and other and glue the three together
            selfNamesRetained = selfNames - sharedNames
            otherNamesRetained = otherNames - sharedNames
            for name in selfNamesRetained:
                combinedAttributeTypes.add(AttributeType(name, self[name]))
            for name in otherNamesRetained:
                combinedAttributeTypes.add(AttributeType(name, other[name]))
        return FlatRecordType(frozenset(combinedAttributeTypes))

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other: FlatRecordType):
        return dict(self) == dict(other)

    def __lt__(self, other: FlatRecordType):
        orderResult: FlatRecordType.Ordered | FlatRecordType.Unordered is None
        orderResult = self.orderAgainst(other)

        if isinstance(orderResult, FlatRecordType.Unordered):
            return False
        if isinstance(orderResult, FlatRecordType.Ordered):
            if orderResult.equal:
                return False
            if orderResult.subtype == self:
                return True

    def __str__(self):
        return f"{self.__class__.__name__}{': '}\
                 {(self.attributeNames, str(self.attributes))}"

    def __repr__(self) -> object:
        return f"{'a'}{'b'}{self.__class__.__name__}\
                 {'(attributes='}{repr(self.attributes)}{')'}"

    class Ordered:
        def __init__(Ordered_self, supertype: FlatRecordType, subtype: FlatRecordType):
            # if first and second are equal we make supertype = first

            Ordered_self.__supertype: FlatRecordType = supertype
            Ordered_self.__subtype: FlatRecordType = subtype

        @property
        def supertype(self) -> FlatRecordType:
            return self.__supertype

        @property
        def subtype(Ordered_self) -> FlatRecordType:
            return Ordered_self.__subtype

        @property
        def equal(Ordered_self) -> bool:
            return Ordered_self.supertype == Ordered_self.subtype

        # TODO JSON dumping and loading

    class Unordered:
        def __init__(Unordered_self,
                     firstNames: [str],
                     secondNames: [str],
                     incompatibleRecords: [AttributeType.Compatible | AttributeType.Incompatible] = None,
                     ):
            Unordered_self.__firstNames = firstNames
            Unordered_self.__secondNames = secondNames
            Unordered_self.__incompatibleRecords = incompatibleRecords

        @property
        def firstNames(Unordered_self) -> [str]:
            return Unordered_self.__firstNames

        @property
        def secondNames(Unordered_self) -> [str]:
            return Unordered_self.__secondNames

        @property
        def namesIncomparable(Unordered_self) -> bool:
            if Unordered_self.firstNames.issubset(Unordered_self.secondNames):
                return False
            if Unordered_self.secondNames.issubset(Unordered_self.firstNames):
                return False
            return True

        @property
        def incompatibleRecords(Unordered_self) -> bool:
            return Unordered_self.__incompatibleRecords

            # TODO JSON dumping and loading

    def orderAgainst(self, other: FlatRecordType) -> FlatRecordType.Ordered | FlatRecordType.Unordered:
        # The comparison of two Records S and T must observe these rules:

        # If T.names includes S.names then T is potentially higher than S; if S.names includes
        # T.names then S is potentially higher than T; if neither is true then S and T are
        # incomparable.

        # If they are potentially comparable, we take the intersection of S.names and T.names
        # and for each pair of identically named attributes in S and T we run a test for compatibility.
        # In the fullness of time this will include every aspect of 22.17 through 22.19 in the GQL spec,
        # for some selected set of supported GQL types. TODO For now, it will just test for type equality.

        selfNames = self.attributeNames
        otherNames = other.attributeNames

        if selfNames.issubset(otherNames):  # then self is potentially the supertype
            return self.confirmDenyActualSupertype(potentialSupertype=self, potentialSubtype=other)

        if selfNames.issubset(otherNames):  # therefore other is potentially the supertype
            return self.confirmDenyActualSupertype(potentialSupertype=other, potentialSubtype=self)

        # self does not include other, and other does not include self
        return FlatRecordType.Unordered(firstNames=selfNames, secondNames=otherNames)

    @staticmethod
    def confirmDenyActualSupertype(potentialSupertype: FlatRecordType,
                                   potentialSubtype: FlatRecordType) -> FlatRecordType.Ordered | FlatRecordType.Unordered:
        recordsCompatible = True
        incompatibleRecords: List[AttributeType.Compatible | AttributeType.Incompatible] = []

        potentialSupertypeNames = potentialSupertype.attributeNames
        potentialSubtypeNames = potentialSubtype.attributeNames

        for key in potentialSupertypeNames:
            attributeTypeCompatible: AttributeType.Compatible | AttributeType.Incompatible \
                = potentialSupertype[key].compatibleWith(potentialSubtype[key])
            if isinstance(attributeTypeCompatible, AttributeType.Compatible):
                incompatibleRecords.append(AttributeType.Compatible(key,
                                                                    potentialSupertype[key],
                                                                    potentialSubtype[key],
                                                                    attributeTypeCompatible.leastCommonSupertype))
            else:
                recordsCompatible = False
                incompatibleRecords.append(
                    AttributeType.Incompatible(key, potentialSupertype[key], potentialSubtype[key]))

            if recordsCompatible:
                return FlatRecordType.Ordered(supertype=potentialSupertype, subtype=potentialSubtype)

            return FlatRecordType.Unordered(firstNames=potentialSupertypeNames,
                                            secondNames=potentialSubtypeNames,
                                            incompatibleRecords=incompatibleRecords)


class PropertyTypesRecordType(FlatRecordType):
    def __init__(self, propertyTypeSet: FrozenSet[PropertyType]):
        # RecordType is just a marker, no __init__ to call
        SortedDict.__init__(self, ((propertyType.name, propertyType.datatype) for propertyType in propertyTypeSet))


class Label(AttributeType):
    def __init__(self, name: str):
        super().__init__(name, LABEL)


class LabelsRecordType(FlatRecordType):
    def __init__(self, labels: List[str]):
        labelSet: Set[Label] = set()
        for label in labels:
            labelSet.add(Label(label))

        super().__init__(frozenset(labelSet))

    def labels(self) -> [Label]:
        return list(super().attributes)

    # A set of labels LS is ordered below a set LT if the names of LT are a subset of LS
    # Attributes provides a method to carry out this test

    def __hash__(self):
        hash(super().attributes)


NO_LABELS = LabelsRecordType([])


class PropertyType(AttributeType):
    def __init__(self, name: str, datatype: Datatype):
        super().__init__(name, datatype)


class PropertyTypesModel(PropertyTypesRecordType):
    def __init__(self, baseModel: BaseModel):
        self.__baseModel = BaseModel


class JSONSchemaPropertyTypes(PropertyTypesRecordType):
    def __init__(self, JSONSchema: str):
        self.__JSONSchema = JSONSchema


class FlatPropertyTypes(PropertyTypesRecordType):
    def __init__(self, propertyTypeSet: List[PropertyType]):
        FlatRecordType.__init__(self, frozenset(propertyTypeSet))

    def propertyTypes(self) -> [PropertyType]:
        return list(super().attributes)


NO_PROPERTY_TYPES = FlatPropertyTypes(set())


# module GraphSchemaRecordTypes

def orderRecordTypes(first: FlatRecordType, second: FlatRecordType) \
        -> FlatRecordType.Ordered | FlatRecordType.Unordered:
    return first.orderAgainst(second)


class ContentTypeInterface(Protocol):
    @property
    def labels(self) -> LabelsRecordType:
        ...

    @property
    def mandatoryPropertyTypes(self) -> FlatPropertyTypes:
        ...

    @property
    def optionalPropertyTypes(self) -> FlatPropertyTypes:
        ...

    @property
    def keyedContentTypes(self) -> SortedDict[LabelsRecordType, KeyedContentTypeInterface]:
        ...


class KeyedContentTypeInterface(ContentTypeInterface):
    @property
    def name(self) -> str | None:
        if self.keyLabels.isSingleton:
            return self.keyLabels.singletonMemberName

    @property
    def keyLabels(self) -> LabelsRecordType:
        ...

    @property
    def otherLabels(self) -> LabelsRecordType:
        ...

    @property
    def mandatoryPropertyTypes(self) -> FlatPropertyTypes:
        pass

    @property
    def optionalPropertyTypes(self) -> FlatPropertyTypes:
        pass


@total_ordering
class ContentType(OrderableABC, ContentTypeInterface):
    def __init__(self,
                 labels: LabelsRecordType = None,
                 mandatoryPropertyTypes: FlatPropertyTypes = None,
                 optionalPropertyTypes: FlatPropertyTypes = None):

        if labels is None:
            labels = NO_LABELS
        if mandatoryPropertyTypes is None:
            mandatoryPropertyTypes = NO_PROPERTY_TYPES
        if optionalPropertyTypes is None:
            optionalPropertyTypes = NO_PROPERTY_TYPES

        self.__labels = labels
        self.__mandatoryPropertyTypes = mandatoryPropertyTypes
        self.__optionalPropertyTypes = optionalPropertyTypes

    def __hash__(self):
        return hash((self.labels, self.mandatoryPropertyTypes, self.optionalPropertyTypes))

    def __eq__(self, other: ContentType):
        return (self.labels, self.mandatoryPropertyTypes, self.optionalPropertyTypes) == \
            (other.labels, other.mandatoryPropertyTypes, other.optionalPropertyTypes)

    def __lt__(self, other: ContentType):
        return (self.labels, self.mandatoryPropertyTypes, self.optionalPropertyTypes) < \
            (other.labels, other.mandatoryPropertyTypes, other.optionalPropertyTypes)
        # some hairy stuff about having a subset of contained KeyedContentTypes ...

    def __str__(self):
        labels = "No labels" if self.labels == [] else str(self.labels)
        mandatoryPropertyTypes = "No mandatory properties" if self.mandatoryPropertyTypes == [] else list(
            str(propertyType) for propertyType in self.mandatoryPropertyTypes)
        optionalPropertyTypes = "No optional properties" if self.optionalPropertyTypes == [] else list(
            str(propertyType) for propertyType in self.optionalPropertyTypes)

        return f"{self.__class__.__name__}{': '}{(labels, mandatoryPropertyTypes, optionalPropertyTypes)}"

    def __repr__(self):
        labels = "[]" if self.labels == [] else str(self.labels)
        mandatoryPropertyTypes = "[]" if self.mandatoryPropertyTypes == [] \
            else list(str(propertyType) for propertyType in self.mandatoryPropertyTypes)
        optionalPropertyTypes = "[]" if self.optionalPropertyTypes == [] \
            else list(str(propertyType) for propertyType in self.optionalPropertyTypes)

        return (f"{self.__class__.__name__}{'('}"
                f"{"labels = ", labels, ", mandatoryPropertyTypes = ", mandatoryPropertyTypes, ", mandatoryPropertyTypes = ", optionalPropertyTypes}")

    @property
    def mandatoryPropertyTypes(self) -> [PropertyType]:
        return list(self.__mandatoryPropertyTypes)

    @property
    def optionalPropertyTypes(self) -> [PropertyType]:
        return list(self.__optionalPropertyTypes)

    def hasOrder(self) -> [OrderableABC.Order]:
        pass  # TODO presumably this is well behaved


@total_ordering
class KeyedContentType(ContentType):
    def __init__(self,
                 identifierLabels: LabelsRecordType = None,
                 otherLabels: LabelsRecordType = None,
                 mandatoryPropertyTypes: FlatPropertyTypes = None,
                 optionalPropertyTypes: FlatPropertyTypes = None):

        if identifierLabels is None:
            identifierLabels = NO_LABELS
        if otherLabels is None:
            otherLabels = NO_LABELS
        if mandatoryPropertyTypes is None:
            mandatoryPropertyTypes = NO_PROPERTY_TYPES
        if optionalPropertyTypes is None:
            optionalPropertyTypes = NO_PROPERTY_TYPES

        # TODO this fails because of attempted direct init of AttributeType
        #  print(identifierLabels) #, otherLabels, mandatoryPropertyTypes, optionalPropertyTypes)
        super().__init__(identifierLabels + otherLabels, mandatoryPropertyTypes, optionalPropertyTypes)

        self.__identifierLabels = identifierLabels
        self.__otherLabels = otherLabels

    def __hash__(self):
        return hash((self.labels, self.mandatoryPropertyTypes, self.optionalPropertyTypes))

    def __eq__(self, other: ContentType):
        return (self.labels, self.mandatoryPropertyTypes, self.optionalPropertyTypes) == \
            (other.labels, other.mandatoryPropertyTypes, other.optionalPropertyTypes)

    def __lt__(self, other: ContentType):
        return (self.labels, self.mandatoryPropertyTypes, self.optionalPropertyTypes) < \
            (other.labels, other.mandatoryPropertyTypes, other.optionalPropertyTypes)
        # some hairy stuff about having a subset of contained KeyedContentTypes ...

    def __str__(self):
        name = "No name " if self.name() is None else str(self.name())
        identifierLabels = "No identifier labels" if self.identifierLabels() == [] else str(self.identifierLabels())
        otherLabels = "No non-identifier labels" if self.otherLabels() == [] else str(self.otherLabels())
        mandatoryPropertyTypes = "No mandatory properties" if self.mandatoryPropertyTypes == [] else list(
            str(propertyType) for propertyType in self.mandatoryPropertyTypes)
        optionalPropertyTypes = "No optional properties" if self.optionalPropertyTypes == [] else list(
            str(propertyType) for propertyType in self.optionalPropertyTypes)

        return f"{self.__class__.__name__}{': '}\
{(name, identifierLabels, otherLabels, mandatoryPropertyTypes, optionalPropertyTypes)}"

    def __repr__(self):
        name = "" if self.name() == "No name" else str(self.name())
        identifierLabels = "[]" if self.identifierLabels() == [] else str(self.identifierLabels())
        otherLabels = "[]" if self.otherLabels() == [] else str(self.otherLabels())
        mandatoryPropertyTypes = "[]" if self.mandatoryPropertyTypes == [] else list(
            str(propertyType) for propertyType in self.mandatoryPropertyTypes)
        optionalPropertyTypes = "[]" if self.optionalPropertyTypes == [] else list(
            str(propertyType) for propertyType in self.optionalPropertyTypes)

        return f"{self.__class__.__name__}{'('}\
{("name = ", name, ", \
identifierLabels = ", identifierLabels, ", otherLabels = ", otherLabels,
  ", mandatoryPropertyTypes = ", mandatoryPropertyTypes, ", mandatoryPropertyTypes = ", optionalPropertyTypes)}"

    def name(self) -> str:
        if len(self.__identifierLabels) == 1:
            return list(self.__identifierLabels)[0]
        else:
            return "No name"

    def identifierLabels(self) -> [str]:
        return list(self.__identifierLabels)

    def otherLabels(self) -> [str]:
        return list(self.__otherLabels)

    def hasOrder(self) -> [OrderableABC.Order]:
        pass  # TODO presumably this is well behaved


@total_ordering
class NamedContentType(KeyedContentType):
    def __init__(self,
                 name: str,
                 otherLabels: LabelsRecordType = None,
                 mandatoryPropertyTypes: FlatPropertyTypes = None,
                 optionalPropertyTypes: FlatPropertyTypes = None):

        identifierLabels = LabelsRecordType([name])
        if otherLabels is None:
            otherLabels = NO_LABELS
        if mandatoryPropertyTypes is None:
            mandatoryPropertyTypes = NO_PROPERTY_TYPES
        if optionalPropertyTypes is None:
            optionalPropertyTypes = NO_PROPERTY_TYPES

        self.__identifierLabels = identifierLabels
        self.__otherLabels = otherLabels

        super().__init__(identifierLabels, otherLabels, mandatoryPropertyTypes, optionalPropertyTypes)
