"""AST nodes for the HMP parser."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Any, Union


@dataclass(frozen=True)
class Node:
    """Base AST node."""
    line: int


@dataclass(frozen=True)
class Expression(Node):
    """Base class for expressions."""
    pass


@dataclass(frozen=True)
class Literal(Expression):
    """Literal value (string, number, list, etc)."""
    value: Any


@dataclass(frozen=True)
class Variable(Expression):
    """Variable reference."""
    name: str


@dataclass(frozen=True)
class InterpolatedString(Expression):
    """String with ${expr} interpolations."""
    parts: List[Union[str, Expression]]


@dataclass(frozen=True)
class Program(Node):
    """Root program node."""
    statements: Sequence["Statement"]


class Statement(Node):
    """Base class for statements."""


@dataclass(frozen=True)
class SetStatement(Statement):
    name: str
    value: Expression


@dataclass(frozen=True)
class CallStatement(Statement):
    tool: str
    params: Dict[str, Expression]
    target: Optional[str] = None


@dataclass(frozen=True)
class ImportStatement(Statement):
    path: str
    namespace: Optional[str]


@dataclass(frozen=True)
class ReturnStatement(Statement):
    value: Expression


@dataclass(frozen=True)
class IfStatement(Statement):
    condition: Expression
    body: Sequence[Statement]
    else_body: Sequence[Statement]


@dataclass(frozen=True)
class LoopTimesStatement(Statement):
    count: Expression
    body: Sequence[Statement]


@dataclass(frozen=True)
class WhileStatement(Statement):
    condition: Expression
    body: Sequence[Statement]


@dataclass(frozen=True)
class ForEachStatement(Statement):
    var_name: str
    iterable: Expression
    body: Sequence[Statement]


@dataclass(frozen=True)
class FunctionDef(Statement):
    name: str
    params: List[str]
    body: Sequence[Statement]


@dataclass(frozen=True)
class TryCatchStatement(Statement):
    body: Sequence[Statement]
    catch_body: Sequence[Statement]
    error_var: Optional[str] = "error"


@dataclass(frozen=True)
class ParallelStatement(Statement):
    body: Sequence[Statement]
