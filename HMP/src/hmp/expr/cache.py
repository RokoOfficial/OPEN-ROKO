"""Cache LRU para expressoes AST pre-compiladas."""

from collections import OrderedDict
from typing import Dict, Optional
import ast


class ExpressionCache:
    """Cache LRU verdadeiro para expressoes AST pre-compiladas usando OrderedDict."""

    def __init__(self, maxsize: int = 1000):
        self._cache: OrderedDict = OrderedDict()
        self._maxsize = maxsize
        self._hits = 0
        self._misses = 0

    def get_ast(self, expr_str: str) -> Optional[ast.AST]:
        """Retorna AST cacheada ou None - move para o final (mais recente) em caso de hit."""
        if expr_str in self._cache:
            self._hits += 1
            self._cache.move_to_end(expr_str)
            return self._cache[expr_str]
        return None

    def set_ast(self, expr_str: str, tree: ast.AST) -> None:
        """Armazena AST no cache - remove o mais antigo (LRU) se cheio."""
        if expr_str in self._cache:
            self._cache.move_to_end(expr_str)
            self._cache[expr_str] = tree
            return

        if len(self._cache) >= self._maxsize:
            self._cache.popitem(last=False)

        self._cache[expr_str] = tree
        self._misses += 1

    def stats(self) -> Dict[str, int]:
        """Retorna estatisticas do cache."""
        total = self._hits + self._misses
        return {
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": round(self._hits / total * 100, 2) if total > 0 else 0,
            "size": len(self._cache)
        }

    def clear(self) -> None:
        """Limpa o cache."""
        self._cache.clear()
        self._hits = 0
        self._misses = 0
