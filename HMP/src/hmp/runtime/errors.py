"""Excecoes do HMP."""


class HMPError(Exception):
    """Excecao base do HMP."""
    
    def __init__(self, message: str, line: int = None, column: int = None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        if self.line is not None:
            if self.column is not None:
                return f"[Linha {self.line}, Coluna {self.column}] {self.message}"
            return f"[Linha {self.line}] {self.message}"
        return self.message


class HMPSyntaxError(HMPError):
    """Erro de sintaxe do HMP."""
    pass


class HMPRuntimeError(HMPError):
    """Erro de runtime do HMP."""
    pass


class HMPLimitError(HMPError):
    """Erro de limite excedido do HMP."""
    pass
