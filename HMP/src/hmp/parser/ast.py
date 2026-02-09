"""AST nodes for the HMP parser."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence


@dataclass(frozen=True)
class Node:
    """Base AST node."""
    line: int


@dataclass(frozen=True)
class Program(Node):
    """Root program node."""
    statements: Sequence["Statement"]


class Statement(Node):
    """Base class for statements."""


@dataclass(frozen=True)
class SetStatement(Statement):
    name: str
    value: str


@dataclass(frozen=True)
class CallStatement(Statement):
    tool: str
    params: Optional[str]


@dataclass(frozen=True)
class ImportStatement(Statement):
    path: str
    namespace: Optional[str]


@dataclass(frozen=True)
class ReturnStatement(Statement):
    value: str


@dataclass(frozen=True)
class IfStatement(Statement):
    condition: str
    body: Sequence[Statement]
    else_body: Sequence[Statement]


@dataclass(frozen=True)
class LoopTimesStatement(Statement):
    count: str
    body: Sequence[Statement]


@dataclass(frozen=True)
class WhileStatement(Statement):
    condition: str
    body: Sequence[Statement]


@dataclass(frozen=True)
class ForEachStatement(Statement):
    var_name: str
    iterable: str
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


@dataclass(frozen=True)
class ParallelStatement(Statement):
    body: Sequence[Statement]
