from enum import Enum
from dataclasses import dataclass
from typing import List, Union

class ASTNodeType(Enum):
    SELECT_STATEMENT = "SELECT_STATEMENT"
    COLUMN_LIST = "COLUMN_LIST"
    TABLE = "TABLE"
    WHERE_CLAUSE = "WHERE_CLAUSE"
    CONDITION = "CONDITION"
    BINARY_OPERATION = "BINARY_OPERATION"
    IDENTIFIER = "IDENTIFIER"
    LITERAL = "LITERAL"

@dataclass
class ASTNode:
    node_type: ASTNodeType
    value: Union[str, None] = None
    children: List['ASTNode'] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []

    def __repr__(self):
        return self._pretty_print()

    def _pretty_print(self, level=0):
        indent = "  " * level
        result = f"{indent}{self.node_type.name}"
        if self.value is not None:
            result += f": {self.value}"
        result += "\n"
        for child in self.children:
            result += child._pretty_print(level + 1)
        return result