from __future__ import annotations

from content_type import *
from lattice import *


@total_ordering
class ElementType: # a content type cannot be a member of a schema graph
                   # every element in a schema graph is an element type and
                   # has an associated content type.
    def __init__(self,
                 contentType: ContentType):
        self.__contentType = contentType
        if contentType is None:
            raise GraphSchemaTypeInitError(self.__class__.__name__, "No content type specified")

    def __hash__(self):
        return hash(self.contentType)

    def __eq__(self, other):
        if isinstance(other, ElementType):
            return self.contentType == other.contentType
        return False

    def __lt__(self, other: ElementType):
        return self.contentType < other.contentType
        # some hairy stuff about having a subset of contained KeyedContentTypes ...

    def __str__(self):
        return f"{self.__class__.__name__}{': '}\{self.contentType}"

    @property
    def contentType(self) -> ContentType:
        return self.__contentType

@total_ordering
class NodeType(ElementType):
    def __init__(self,
                 contentType: ContentType):
        if contentType is None:
            raise GraphSchemaTypeInitError(self.__class__.__name__, "No content type specified")

        super().__init__(contentType=contentType)

    def __hash__(self):
        return hash((super().__hash__()))

    def __eq__(self, other: NodeType):
        return self.elementType == other.elementType

    def __str__(self):
        return f"{self.__class__.__name__}{': '}\
    {super()}"

    @property
    def elementType(self) -> ElementType:
        return super()

@total_ordering
class EdgeType(ElementType):
    def __init__(self,
                 contentType: ContentType,
                 endpoints: Tuple[NodeType, NodeType],
                 tail: NodeType = None,
                 head: NodeType = None):
        if contentType is None:
            raise GraphSchemaTypeInitError(self.__class__.__name__, "No content type specified")
        if endpoints is None:
            raise GraphSchemaTypeInitError(self.__class__.__name__,"No endpoints specified")
        if (tail is None and head is not None or
            head is None and tail is not None):
            raise GraphSchemaTypeInitError(self.__class__.__name__, "One of tail or head is None but not both")
        if tail not in endpoints and head not in endpoints:
            raise GraphSchemaTypeInitError(self.__class__.__name__, "Neither tail nor head is in endpoints")
        if tail not in endpoints:
            raise GraphSchemaTypeInitError(self.__class__.__name__, "tail is not in endpoints")
        if tail not in endpoints:
            raise GraphSchemaTypeInitError(self.__class__.__name__, "head is not in endpoints")

        ElementType.__init__(self, contentType=contentType)
        self.__endpoints = endpoints
        self.__tail = tail
        self.__head = head

    @property
    def contentType(self) -> ContentType:
        return self.elementType.contentType

    @property
    def elementType(self) -> ElementType:
        return super()

    @property
    def endpoints(self) -> Tuple[NodeType, NodeType]:
        return self.__endpoints

    @property
    def tail(self) -> NodeType | None:
        return self.__tail

    @property
    def head(self) -> NodeType | None:
        return self.__head

    @property
    def directed(self) -> bool:
        if self.tail is None:
            return False

    @property
    def undirected(self) -> bool:
        return not self.directed

    def directedEdge(self) -> DirectedEdgeType | None:
        pass

    def directedEndpoints(self) -> Tuple[NodeType, NodeType] | None:
        return None if self.tail is None else (self.tail, self.head)

    def __hash__(self):
        return hash((super().__hash__(), self.endpoints, self.tail, self.head))

    def __eq__(self, other: EdgeType):
        return (self.elementType == other.elementType and
                self.endpoints == other.endpoints and
                self.tail == other.tail and
                self.head == other.head)

    def __str__(self):
        return f"{self.__class__.__name__}{': '}\
    {super()}"

@total_ordering
class DirectedEdgeType(EdgeType):
    def __init__(self,
                 contentType: ContentType,
                 tail: NodeType,
                 head: NodeType):
        if tail is None:
            raise GraphSchemaTypeInitError(self.__class__.__name__, "tail is None")
        if head is None:
            raise GraphSchemaTypeInitError(self.__class__.__name__, "head is None")

        EdgeType.__init__(self, contentType=contentType, endpoints=(tail, head), tail=tail, head=head)

    def __hash__(self):
        return hash(super().__hash__())

    def __eq__(self, other):
        return super() == super(EdgeType, other)

    def __str__(self):
        return f"{self.__class__.__name__}{': '}\
    {super()}"

@total_ordering
class GraphType(Named):
    def __init__(self, name: str, nodeTypes: FrozenSet[NodeType], edgeTypes: FrozenSet[EdgeType]):
        Named.__init__(self, name)
        self.__nodeTypes = nodeTypes
        self.__edgeTypes = edgeTypes
        # self.establishContentTypesLattice() TODO

    @property
    def nodeTypes(self) -> [NodeType]:
        return list(self.__nodeTypes)

    @property
    def edgeTypes(self) -> [EdgeType]:
        return list(self.__edgeTypes)

    @property
    def contentTypesLattice(self) -> AnyNothingTypeLattice[ContentType]:
        pass

    # def establishContentTypesLattice(self):
    #     self.__lattice = AnyNothingTypeLattice[ContentType](self.nodeTypes.contentTypes + self.edgeTypes.contentTypes)
    #     return self.__lattice

    def __hash__(self):
        return hash((self.name, self.nodeTypes, self.edgeTypes))

    def __eq__(self, other: GraphType):
        pass

    def __lt__(self, other: GraphType):
        pass
        # some hairy stuff about having a subset of contained KeyedContentTypes ...

    def __str__(self):
        return f"{self.__class__.__name__}{': '}{self.name}{self.nodeTypes}{self.edgeTypes}"

    def __repr__(self): # TODO transmute to repr format
        return f"{self.__class__.__name__}{': '}{self.name}{self.nodeTypes}{self.edgeTypes}"

