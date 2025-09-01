from __future__ import annotations
from fundamental import *
from typing import Set, Dict
from collections import defaultdict
from sortedcontainers import SortedDict

# A type lattice is built up of nodes and edges. It is the union of a join-semilattice and a meet-semilattice:
#  (meet at the bottom and join at the top) whose elements are of the same class (are the same type, e.g. content
#  type, node type, edge type), and whose order relation (subtype relation in this case, where "S is a subtype of T"
#  means "S is lower than T") is the same.
#
#  Correspondingly we have generic classes for type lattice nodes, edges, join-semilattice, meet-semilattice and
#  lattice. The bounds of the last three are elements in the set of types, so the supremum (top) is the maximum
#  (greatest) element, and the infimum (bottom) is the minimum (least) element in the set.
#
# We also have a specialized lattice whose bounds are ANY and NOTHING, which are outside the set, and which allow us to
# bound any set of types. This is called an AnyNothingTypeLattice
#
# A node or edge can exist outside a lattice (and therefore make up arbitrary lattice fragment: this is a kind of
# "pre-lattice", which does not necessarily have a unique upper or lower bound (top or bottom), but would form a lattice
# if those bounds exists). This is simply a partially ordered set, or poset.
#
# Therefore, we have a core class called TypePoset. It is specialized to add an upper bound, by the class JoinSemiTypeLattice,
# and to add a lower bound by the class MeetSemiTypeLattice. TypeLattice inherits from both of these. AnyNothingTypeLattice
# specializes TypeLattice by fixing the bounds as the constants LatticeLimit.ANY and LatticeLimit.NOTHING. It is a feature
# of every subtype relation in this library that every element is less than ANY and greater than NOTHING, even if the element
# is the maximum (natural supremum) or minimum (natural infimum) of the set which underlies the subtype relation.

class LatticeBound(Enum):
    ANY = "TOP"
    NOTHING = "BOTTOM"

class TypeLatticeNode[ORDERABLE: OrderableABC]:
    # This class wraps the real objects, and provides
    # generic operations relating to its relationship with
    # its parent lattice, once merged. Its comparator
    # functions delegate to those of  the wrapped Orderable.

    def __init__(self, value: ORDERABLE, lattice: TypeLattice[ORDERABLE] = None):
        self.__value = value
        self.__lattice = lattice

    @property
    def value(self) -> ORDERABLE:
        return self.__value

    @property
    def lattice(self) -> TypeLattice[ORDERABLE]:
        return self.__lattice

    @property
    def latticed(self) -> bool:
        return False if self.lattice is None else True

    @lattice.setter
    def lattice(self, lattice: TypeLattice[ORDERABLE]):
        self.__lattice = lattice  # only used by merge operation on the lattice

    def wrapsType(self, _type: type) -> bool:
        return isinstance(self.value, _type)

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: ORDERABLE):
        if TypeLatticeNode.wrapsType(other, type(ORDERABLE)):
            return self.value == other.value
        return False

    def __lt__(self, other: ORDERABLE):
        if TypeLatticeNode.wrapsType(other, type(ORDERABLE)):
            return other.value < self.value
        else:
            return False

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        if hasattr(self.value, "__repr__"):
            f"{self.__class__.__name__}{'('}\
    {(repr(self.value))}"
        else:
            pass

class TypeLatticeEdge[LATTICE_NODE: OrderableABC]:
    def __init__(self,
                 lattice: 'AnyNothingTypeLattice[LATTICE_NODE]',
                 higher: TypeLatticeNode[LATTICE_NODE],
                 lower: TypeLatticeNode[LATTICE_NODE]):
        self.__lattice = lattice
        self.__higher = higher
        self.__lower = lower

    @property
    def lattice(self) -> 'AnyNothingTypeLattice[LATTICE_NODE]':
        return self.__lattice

    @property
    def higher(self) -> TypeLatticeNode[LATTICE_NODE]:
        return self.__higher

    @property
    def lower(self) -> TypeLatticeNode[LATTICE_NODE]:
        return self.__lower

class MergeStatus(Enum):
    STARTED = 'STARTED'
    ABORTED = 'ABORTED'
    ACCOMPLISHED = 'ACCOMPLISHED'

class TypeLatticeNodeIncidentEdges[LATTICE_NODE: OrderableABC]:
    def __init__(self, poset: 'TypePoset[LATTICE_NODE]', node: TypeLatticeNode[LATTICE_NODE]):
        self.__state = MergeStatus.STARTED
        self.__node = node
        self.__superTypes: list[TypeLatticeNode[LATTICE_NODE]] = []
        self.__subTypes: list[TypeLatticeNode[LATTICE_NODE]] = []

        # This class holds the state of a node while it is being merged into a type pre-lattice (poset).
        # So for the operation TypePoset.mergeNode(self, node) node is a class of this type.
        # The lists of super and subtypes provide a diagnostic aid while testing or visualizing merges.
        # The actual state of the merge-accomplished graph is held in the instance of TypePoset.


    @property
    def mergeStatus(self) -> MergeStatus:
        return self.__state

    @mergeStatus.setter
    def mergeStatus(self, status: MergeStatus):
        self.__state = status

    @property
    def superTypes(self) -> [TypeLatticeNode[LATTICE_NODE]]:
        return self.__superTypes

    @property
    def subTypes(self) -> [TypeLatticeNode[LATTICE_NODE]]:
        return self.__subTypes

    def addSuperType(self, superType: TypeLatticeNode[LATTICE_NODE]):
        self.superTypes.extend(superType)

    def addSubType(self, subType: TypeLatticeNode[LATTICE_NODE]):
        self.subTypes.extend(subType)

class TypePoset[LATTICE_NODE: OrderableABC]:
    def __init__(self, nodes: Set[TypeLatticeNode[LATTICE_NODE]]):
        # This class is pre-initialized in an empty state, and populated by merging nodes into it.

        self.__nodes: Set[TypeLatticeNode[LATTICE_NODE]] = set()  # mergeNodes assumes a prior set
        self.__edges: Dict[TypeLatticeNode[LATTICE_NODE], list[TypeLatticeEdge[LATTICE_NODE]]] = defaultdict(list)
        self.__maximal: Set[TypeLatticeNode[LATTICE_NODE]] = set()
        self.__minimal: Set[TypeLatticeNode[LATTICE_NODE]] = set()
        self.__internal: Set[TypeLatticeNode[LATTICE_NODE]] = set()

        self.mergeNodes(nodes)

    # The core of a type lattice, this representation of a partially ordered set (poset) has no bounds.
    # It is described in "TypePoset structure and algorithm for merging type nodes" @
    # https://docs.google.com/document/d/1RHybczWbLdBXo0h9HePJ5tSXSXDD_XIs7myW4dxmSSQ/edit?usp=sharing

    @property
    def nodes(self) -> Set[TypeLatticeNode[LATTICE_NODE]]:
        return self.__nodes

    @property
    def edges(self) -> defaultdict[TypeLatticeNode[LATTICE_NODE], [TypeLatticeEdge[LATTICE_NODE]]](list):
        return self.__edges

    @property
    def maximal(self) -> defaultdict[TypeLatticeNode[LATTICE_NODE], [TypeLatticeEdge[LATTICE_NODE]]](list):
        return self.__maximal

    @property
    def internal(self) -> Set[TypeLatticeNode[LATTICE_NODE]]:
        return self.__internal

    @property
    def minimal(self) -> Set[TypeLatticeNode[LATTICE_NODE]]:
        return self.__minimal

    # def establishIncidentEdges(self,
    #                            workInProgress: TypeLatticeNodeIncidentEdges[LATTICE_NODE],
    #                            depth: int) \
    #         -> TypeLatticeNodeIncidentEdges[LATTICE_NODE]:
    #
    #
    #     node = workInProgress.node
    #
    #     if 0 == depth:
    #         currentLevel = self.level["TOP"]
    #     else:
    #         currentLevel = self.level[depth]
    #
    #     for currentLevelNode in currentLevel:
    #         superior: TypeLatticeNode[LATTICE_NODE] is None
    #
    #         if node == currentLevelNode:
    #             workInProgress.mergeStatus(MergeStatus.ABORTED)
    #             break
    #         if node < currentLevelNode:
    #             superior = currentLevelNode
    #             break
    #
    #         if superior is not None:
    #             pass

    def mergeNode(self, node: TypeLatticeNode[LATTICE_NODE]) -> [TypeLatticeNodeIncidentEdges]:
        nodeIncidentEdges = TypeLatticeNodeIncidentEdges(self, node)
        # here goes the horrible algo

    def mergeNodes(self, nodes: Set[TypeLatticeNode[LATTICE_NODE]]):
        self.nodes.union(nodes)  # add the new nodes to the graph
        for node in nodes:
            self.mergeNode(node)  # upon successful completion, the appropriate edges will also have been added

class TypeLatticeNodeIncidentEdgesX[LATTICE_NODE: OrderableABC]:
    def __init__(self,
                 lattice: 'AnyNothingTypeLattice[LATTICE_NODE]',
                 node: TypeLatticeNode[LATTICE_NODE],
                 edges: Set[TypeLatticeEdge[LATTICE_NODE]] = None):
        self.__lattice = lattice
        self.__node = node
        self.__edges = edges

    @property
    def element(self) -> TypeLatticeNode[LATTICE_NODE]:
        return self.__node

    @property
    def lattice(self) -> 'AnyNothingTypeLattice[LATTICE_NODE]':
        return self.__lattice

    def __hash__(self):
        return hash((self.element, self.lattice))

    def __eq__(self, other: TypeLatticeNodeIncidentEdgesX[LATTICE_NODE]):
        return (self.element, self.lattice) == (other.element, self.lattice)

    def __str__(self):
        return f"{self.__class__.__name__}{': '}\
{(self.element,
  str(self.lattice))}"

    def __repr__(self) -> object:
        return f"{'a'}{'b'}{self.__class__.__name__}\
                 {'(node='}{repr(self.element)}\
                 {', datatype='}{repr(self.lattice)}\
                 {')'}"

class JoinSemiTypeLattice[ORDERABLE: OrderableABC]:
    pass

class MeetSemiTypeLattice[ORDERABLE: OrderableABC]:
    pass

class TopHalfTypeLattice[ORDERABLE: OrderableABC](JoinSemiTypeLattice[ORDERABLE]):
    pass  # a typedef, a name you might prefer

class BottomHalfTypeLattice[ORDERABLE: OrderableABC](MeetSemiTypeLattice[ORDERABLE]):
    pass  # a typedef, a name you might prefer

class TypeLattice[ORDERABLE: OrderableABC](TopHalfTypeLattice[ORDERABLE], BottomHalfTypeLattice[ORDERABLE]):
    def __init__(self, poset: TypePoset[ORDERABLE], supremum: LatticeBound, infimum: LatticeBound):
        self.__poset = poset
        self.__supremum = supremum
        self.__infimum = infimum

    @property
    def supremum(self) -> LatticeBound:
        return self.__supremum

    @property
    def infimum(self) -> LatticeBound:
        return self.__infimum

class AnyNothingTypeLattice[ORDERABLE: OrderableABC](TypeLattice[ORDERABLE]):
    def __init__(self, poset: TypePoset[ORDERABLE]):
        super().__init__(poset, LatticeBound.ANY, LatticeBound.NOTHING)

