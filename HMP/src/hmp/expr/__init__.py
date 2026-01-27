"""Modulo de avaliacao de expressoes."""

from hmp.expr.cache import ExpressionCache
from hmp.expr.evaluator import safe_eval_expr, SAFE_OPERATORS

__all__ = ["ExpressionCache", "safe_eval_expr", "SAFE_OPERATORS"]
