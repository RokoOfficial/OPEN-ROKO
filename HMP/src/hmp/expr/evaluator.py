"""Avaliador seguro de expressoes usando AST."""

import ast
import operator
from typing import Any, Dict, Optional

from hmp.expr.cache import ExpressionCache

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,
    ast.Not: operator.not_,
}

_default_cache = ExpressionCache(maxsize=2000)


def get_default_cache() -> ExpressionCache:
    """Retorna o cache padrao de expressoes."""
    return _default_cache


def safe_eval_expr(
    expr_str: str, 
    variables: Optional[Dict] = None,
    cache: Optional[ExpressionCache] = None
) -> Any:
    """
    Avalia expressoes de forma segura sem usar eval().
    Usa cache de AST para expressoes repetidas.
    Resolve variaveis diretamente na AST (sem regex).
    """
    if variables is None:
        variables = {}
    
    if cache is None:
        cache = _default_cache

    cached_tree = cache.get_ast(expr_str)
    if cached_tree:
        return _eval_node(cached_tree, variables)

    try:
        tree = ast.parse(expr_str, mode='eval')
        cache.set_ast(expr_str, tree.body)
        return _eval_node(tree.body, variables)
    except (SyntaxError, ValueError, TypeError):
        return expr_str


def _eval_node(node: ast.AST, variables: Dict) -> Any:
    """Avalia um no da AST de forma segura - resolucao direta de variaveis."""

    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.Num):
        return node.n

    if isinstance(node, ast.Str):
        return node.s

    if isinstance(node, ast.List):
        return [_eval_node(elem, variables) for elem in node.elts]

    if isinstance(node, ast.Tuple):
        return tuple(_eval_node(elem, variables) for elem in node.elts)

    if isinstance(node, ast.Dict):
        return {
            _eval_node(k, variables): _eval_node(v, variables)
            for k, v in zip(node.keys, node.values)
        }

    if isinstance(node, ast.Name):
        name = node.id
        if name in ('True', 'true'):
            return True
        if name in ('False', 'false'):
            return False
        if name in ('None', 'null'):
            return None
        if name in variables:
            return variables[name]
        raise ValueError(f"Variavel nao definida: {name}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, variables)
        right = _eval_node(node.right, variables)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](left, right)
        raise ValueError(f"Operador nao suportado: {op_type}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, variables)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](operand)
        raise ValueError(f"Operador unario nao suportado: {op_type}")

    if isinstance(node, ast.Compare):
        left = _eval_node(node.left, variables)
        for op, comparator in zip(node.ops, node.comparators):
            right = _eval_node(comparator, variables)
            op_type = type(op)
            if op_type not in SAFE_OPERATORS:
                raise ValueError(f"Comparacao nao suportada: {op_type}")
            if not SAFE_OPERATORS[op_type](left, right):
                return False
            left = right
        return True

    if isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            for v in node.values:
                if not _eval_node(v, variables):
                    return False
            return True
        if isinstance(node.op, ast.Or):
            for v in node.values:
                if _eval_node(v, variables):
                    return True
            return False

    if isinstance(node, ast.Subscript):
        value = _eval_node(node.value, variables)
        if isinstance(node.slice, ast.Index):
            index = _eval_node(node.slice.value, variables)
        else:
            index = _eval_node(node.slice, variables)
        return value[index]

    if isinstance(node, ast.IfExp):
        test = _eval_node(node.test, variables)
        if test:
            return _eval_node(node.body, variables)
        return _eval_node(node.orelse, variables)

    if isinstance(node, ast.Call):
        raise ValueError("Chamadas de funcao nao permitidas em expressoes")

    if isinstance(node, ast.Attribute):
        raise ValueError("Acesso a atributos nao permitido em expressoes")

    raise ValueError(f"Tipo de expressao nao suportado: {type(node).__name__}")
