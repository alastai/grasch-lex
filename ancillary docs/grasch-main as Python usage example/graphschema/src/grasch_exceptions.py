class GraphSchemaError(Exception):
    def __init__(self, reason: str):
        super().__init__(reason)

class DuplicateNameError(GraphSchemaError):
    pass

class IncompatibleDatatypesError(GraphSchemaError):
    pass

class IncomparableError(GraphSchemaError):
    pass

class GraphSchemaTypeInitError(GraphSchemaError):
    def __init__(self, typeClassName: str, reason: str):
        super().__init__(reason)
        self.__typeClassName = typeClassName

    @property
    def typeClassName (self) -> str:
        return self.__typeClassName

    def __str__(self):
        return f"Failed to initialize type {self.typeClassName}: {super().__str__()}"