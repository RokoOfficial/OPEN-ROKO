"""Tokenizador de scripts HMP."""

import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional


class TokenType(Enum):
    """Tipos de tokens do HMP."""
    SET = auto()
    CALL = auto()
    IMPORT = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    ENDIF = auto()
    LOOP = auto()
    TIMES = auto()
    ENDLOOP = auto()
    WHILE = auto()
    ENDWHILE = auto()
    FOR = auto()
    EACH = auto()
    IN = auto()
    ENDFOR = auto()
    FUNCTION = auto()
    ENDFUNCTION = auto()
    RETURN = auto()
    TRY = auto()
    CATCH = auto()
    ENDTRY = auto()
    PARALLEL = auto()
    ENDPARALLEL = auto()
    AS = auto()
    TO = auto()
    WITH = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    EXPRESSION = auto()
    OPERATOR = auto()
    COMMA = auto()
    EQUALS = auto()
    COMMENT = auto()
    NEWLINE = auto()
    EOF = auto()


@dataclass
class Token:
    """Representa um token do HMP."""
    type: TokenType
    value: str
    line: int
    column: int


class Tokenizer:
    """Tokenizador de scripts HMP."""
    
    KEYWORDS = {
        'SET': TokenType.SET,
        'TO': TokenType.TO,
        'CALL': TokenType.CALL,
        'WITH': TokenType.WITH,
        'IMPORT': TokenType.IMPORT,
        'AS': TokenType.AS,
        'IF': TokenType.IF,
        'THEN': TokenType.THEN,
        'ELSE': TokenType.ELSE,
        'ENDIF': TokenType.ENDIF,
        'LOOP': TokenType.LOOP,
        'TIMES': TokenType.TIMES,
        'ENDLOOP': TokenType.ENDLOOP,
        'WHILE': TokenType.WHILE,
        'ENDWHILE': TokenType.ENDWHILE,
        'FOR': TokenType.FOR,
        'EACH': TokenType.EACH,
        'IN': TokenType.IN,
        'ENDFOR': TokenType.ENDFOR,
        'FUNCTION': TokenType.FUNCTION,
        'ENDFUNCTION': TokenType.ENDFUNCTION,
        'RETURN': TokenType.RETURN,
        'TRY': TokenType.TRY,
        'CATCH': TokenType.CATCH,
        'ENDTRY': TokenType.ENDTRY,
        'PARALLEL': TokenType.PARALLEL,
        'ENDPARALLEL': TokenType.ENDPARALLEL,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """Tokeniza o codigo fonte."""
        self.tokens = []
        
        while self.pos < len(self.source):
            self._skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            char = self.source[self.pos]
            
            if char == '\n':
                self._add_token(TokenType.NEWLINE, '\n')
                self.pos += 1
                self.line += 1
                self.column = 1
                continue
            
            if char == '#':
                self._read_comment()
                continue
            
            if char == '"' or char == "'":
                self._read_string(char)
                continue
            
            if char == '$' and self._peek(1) == '{':
                self._read_expression()
                continue
            
            if char.isdigit() or (char == '-' and self._peek(1).isdigit()):
                self._read_number()
                continue
            
            if char.isalpha() or char == '_':
                self._read_identifier()
                continue
            
            if char == ',':
                self._add_token(TokenType.COMMA, ',')
                self.pos += 1
                self.column += 1
                continue
            
            if char == '=':
                self._add_token(TokenType.EQUALS, '=')
                self.pos += 1
                self.column += 1
                continue
            
            if char in '+-*/<>!':
                self._read_operator()
                continue
            
            self.pos += 1
            self.column += 1
        
        self._add_token(TokenType.EOF, '')
        return self.tokens
    
    def _peek(self, offset: int = 0) -> str:
        """Retorna caractere na posicao atual + offset."""
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return ''
    
    def _add_token(self, type: TokenType, value: str) -> None:
        """Adiciona um token a lista."""
        self.tokens.append(Token(type, value, self.line, self.column))
    
    def _skip_whitespace(self) -> None:
        """Pula espacos em branco (exceto newline)."""
        while self.pos < len(self.source) and self.source[self.pos] in ' \t\r':
            self.pos += 1
            self.column += 1
    
    def _read_comment(self) -> None:
        """Le um comentario ate o fim da linha."""
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos] != '\n':
            self.pos += 1
        value = self.source[start:self.pos]
        self._add_token(TokenType.COMMENT, value)
        self.column += len(value)
    
    def _read_string(self, quote: str) -> None:
        """Le uma string."""
        start = self.pos
        self.pos += 1
        
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char == quote:
                self.pos += 1
                break
            if char == '\\' and self.pos + 1 < len(self.source):
                self.pos += 2
            else:
                self.pos += 1
        
        value = self.source[start:self.pos]
        self._add_token(TokenType.STRING, value)
        self.column += len(value)
    
    def _read_expression(self) -> None:
        """Le uma expressao ${...}."""
        start = self.pos
        self.pos += 2
        depth = 1
        
        while self.pos < len(self.source) and depth > 0:
            char = self.source[self.pos]
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
            self.pos += 1
        
        value = self.source[start:self.pos]
        self._add_token(TokenType.EXPRESSION, value)
        self.column += len(value)
    
    def _read_number(self) -> None:
        """Le um numero."""
        start = self.pos
        
        if self.source[self.pos] == '-':
            self.pos += 1
        
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            self.pos += 1
        
        if self.pos < len(self.source) and self.source[self.pos] == '.':
            self.pos += 1
            while self.pos < len(self.source) and self.source[self.pos].isdigit():
                self.pos += 1
        
        value = self.source[start:self.pos]
        self._add_token(TokenType.NUMBER, value)
        self.column += len(value)
    
    def _read_identifier(self) -> None:
        """Le um identificador ou keyword."""
        start = self.pos
        
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char.isalnum() or char in '_.':
                self.pos += 1
            else:
                break
        
        value = self.source[start:self.pos]
        token_type = self.KEYWORDS.get(value.upper(), TokenType.IDENTIFIER)
        self._add_token(token_type, value)
        self.column += len(value)
    
    def _read_operator(self) -> None:
        """Le um operador."""
        start = self.pos
        
        two_char_ops = ['==', '!=', '<=', '>=', '&&', '||']
        if self.pos + 1 < len(self.source):
            two_char = self.source[self.pos:self.pos+2]
            if two_char in two_char_ops:
                self.pos += 2
                self._add_token(TokenType.OPERATOR, two_char)
                self.column += 2
                return
        
        self._add_token(TokenType.OPERATOR, self.source[self.pos])
        self.pos += 1
        self.column += 1
