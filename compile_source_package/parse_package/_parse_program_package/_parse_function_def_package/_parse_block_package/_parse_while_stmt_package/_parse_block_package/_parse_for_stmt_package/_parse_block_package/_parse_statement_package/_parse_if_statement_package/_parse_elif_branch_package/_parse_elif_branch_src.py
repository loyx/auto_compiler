# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block

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
#   "error": str
# }

# === main function ===
def _parse_elif_branch(parser_state: ParserState, if_token: Token) -> Dict[str, Any]:
    """Parse a single ELIF branch."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 1. Consume ELIF token
    if pos >= len(tokens) or tokens[pos]["type"] != "ELIF":
        raise SyntaxError(f"{filename}:{if_token['line']}:{if_token['column']}: Expected ELIF token")
    elif_token = tokens[pos]
    pos += 1
    
    # 2. Consume LPAREN token
    if pos >= len(tokens) or tokens[pos]["type"] != "LPAREN":
        raise SyntaxError(f"{filename}:{elif_token['line']}:{elif_token['column']}: Expected '(' after ELIF")
    pos += 1
    
    # 3. Parse condition expression
    condition = _parse_expression(parser_state)
    pos = parser_state["pos"]
    
    # 4. Consume RPAREN token
    if pos >= len(tokens) or tokens[pos]["type"] != "RPAREN":
        raise SyntaxError(f"{filename}:{elif_token['line']}:{elif_token['column']}: Expected ')' after condition")
    pos += 1
    
    # 5. Consume COLON token
    if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
        raise SyntaxError(f"{filename}:{elif_token['line']}:{elif_token['column']}: Expected ':' after ELIF condition")
    pos += 1
    
    # 6. Consume LBRACE token
    if pos >= len(tokens) or tokens[pos]["type"] != "LBRACE":
        raise SyntaxError(f"{filename}:{elif_token['line']}:{elif_token['column']}: Expected '{{' after ':'")
    pos += 1
    
    # 7. Parse block statements
    block = _parse_block(parser_state)
    pos = parser_state["pos"]
    
    # 8. Consume RBRACE token
    if pos >= len(tokens) or tokens[pos]["type"] != "RBRACE":
        raise SyntaxError(f"{filename}:{elif_token['line']}:{elif_token['column']}: Expected '}}' to close ELIF block")
    pos += 1
    
    # Update position
    parser_state["pos"] = pos
    
    return {
        "condition": condition,
        "block": block
    }

# === helper functions ===

# === OOP compatibility layer ===
