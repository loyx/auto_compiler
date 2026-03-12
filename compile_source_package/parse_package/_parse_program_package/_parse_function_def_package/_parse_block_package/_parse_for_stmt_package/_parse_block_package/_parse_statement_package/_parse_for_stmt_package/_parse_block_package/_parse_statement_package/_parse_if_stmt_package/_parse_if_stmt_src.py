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
def _parse_if_stmt(parser_state: ParserState) -> AST:
    """Parse if statement: if (condition) { ... } [else { ... }]"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Get IF token for line/column info
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input, expected 'if'")
    
    if_token = tokens[pos]
    start_line = if_token["line"]
    start_column = if_token["column"]
    
    # 1. Consume IF token
    if if_token["type"] != "IF":
        raise SyntaxError(f"{filename}:{if_token['line']}:{if_token['column']}: Expected 'if' keyword")
    pos += 1
    
    # 2. Expect and consume LPAREN
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{start_line}:{start_column}: Unexpected end of input, expected '('")
    if tokens[pos]["type"] != "LPAREN":
        raise SyntaxError(f"{filename}:{tokens[pos]['line']}:{tokens[pos]['column']}: Expected '(' after 'if'")
    pos += 1
    
    # 3. Parse condition expression
    parser_state["pos"] = pos
    condition_ast = _parse_expression(parser_state)
    pos = parser_state["pos"]
    
    # 4. Expect and consume RPAREN
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{start_line}:{start_column}: Unexpected end of input, expected ')'")
    if tokens[pos]["type"] != "RPAREN":
        raise SyntaxError(f"{filename}:{tokens[pos]['line']}:{tokens[pos]['column']}: Expected ')' after condition")
    pos += 1
    
    # 5. Parse then block
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{start_line}:{start_column}: Unexpected end of input, expected '{{'")
    if tokens[pos]["type"] != "LBRACE":
        raise SyntaxError(f"{filename}:{tokens[pos]['line']}:{tokens[pos]['column']}: Expected '{{' after if condition")
    
    parser_state["pos"] = pos
    then_block_ast = _parse_block(parser_state)
    pos = parser_state["pos"]
    
    # 6. Check for ELSE
    else_block_ast = None
    if pos < len(tokens) and tokens[pos]["type"] == "ELSE":
        pos += 1
        # Expect LBRACE for else block
        if pos >= len(tokens):
            raise SyntaxError(f"{filename}:{start_line}:{start_column}: Unexpected end of input, expected '{{' after 'else'")
        if tokens[pos]["type"] != "LBRACE":
            raise SyntaxError(f"{filename}:{tokens[pos]['line']}:{tokens[pos]['column']}: Expected '{{' after 'else'")
        
        parser_state["pos"] = pos
        else_block_ast = _parse_block(parser_state)
        pos = parser_state["pos"]
    
    # 7. Return IF_STMT AST node
    parser_state["pos"] = pos
    
    return {
        "type": "IF_STMT",
        "condition": condition_ast,
        "then_block": then_block_ast,
        "else_block": else_block_ast,
        "line": start_line,
        "column": start_column
    }

# === helper functions ===

# === OOP compatibility layer ===
