# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._peek_token_package._peek_token_src import _peek_token
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_statement_package._parse_statement_src import _parse_statement

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str | None
# }

# === main function ===
def _parse_if(parser_state: dict) -> dict:
    """Parse IF statement and return IF AST node."""
    # Step 1: Consume IF token
    if_token = _consume_token(parser_state, "IF")
    line = if_token["line"]
    column = if_token["column"]
    
    # Step 2: Parse condition expression
    condition = _parse_expression(parser_state)
    
    # Step 3: Parse then_block
    then_block = _parse_block(parser_state)
    
    # Step 4: Check for ELSE
    else_block = None
    next_token = _peek_token(parser_state)
    if next_token is not None and next_token["type"] == "ELSE":
        _consume_token(parser_state, "ELSE")
        else_block = _parse_block(parser_state)
    
    # Step 5: Return IF AST node
    return {
        "type": "IF",
        "condition": condition,
        "then_block": then_block,
        "else_block": else_block,
        "line": line,
        "column": column
    }

# === helper functions ===
def _parse_block(parser_state: dict) -> dict:
    """Parse a block of statements enclosed in braces or single statement."""
    next_token = _peek_token(parser_state)
    
    if next_token is None:
        last_pos = max(0, parser_state["pos"] - 1)
        tokens = parser_state["tokens"]
        if last_pos < len(tokens):
            line, column = tokens[last_pos]["line"], tokens[last_pos]["column"]
        else:
            line, column = 0, 0
        raise SyntaxError(f"Unexpected end of input at line {line}, column {column}")
    
    line = next_token["line"]
    column = next_token["column"]
    
    # If LBRACE, parse multiple statements until RBRACE
    if next_token["type"] == "LBRACE":
        _consume_token(parser_state, "LBRACE")
        statements = []
        
        while True:
            peek = _peek_token(parser_state)
            if peek is None:
                raise SyntaxError(f"Unexpected end of input at line {line}, column {column}")
            if peek["type"] == "RBRACE":
                _consume_token(parser_state, "RBRACE")
                break
            
            stmt = _parse_statement(parser_state)
            statements.append(stmt)
        
        return {
            "type": "BLOCK",
            "statements": statements,
            "line": line,
            "column": column
        }
    else:
        # Single statement as block
        stmt = _parse_statement(parser_state)
        return {
            "type": "BLOCK",
            "statements": [stmt],
            "line": line,
            "column": column
        }

# === OOP compatibility layer ===
