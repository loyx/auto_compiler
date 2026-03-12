# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expr_package._parse_expr_src import _parse_expr
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
    """Parse if statement. Grammar: IF expr COLON block (ELIF expr COLON block)* (ELSE COLON block)?"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. Consume IF token
    if_token = tokens[pos]
    pos += 1
    
    # 2. Parse condition expression
    condition_ast = _parse_expr(parser_state)
    pos = parser_state["pos"]
    
    # 3. Consume COLON token
    if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
        parser_state["error"] = f"Expected COLON after if condition at line {if_token['line']}"
        pos += 1
    else:
        pos += 1
    
    # 4. Parse if block
    then_block_ast = _parse_block(parser_state)
    pos = parser_state["pos"]
    
    # 5. Build children list
    children = [condition_ast, then_block_ast]
    
    # 6. Loop through ELIF branches
    while pos < len(tokens) and tokens[pos]["type"] == "ELIF":
        pos += 1  # consume ELIF
        parser_state["pos"] = pos
        
        elif_condition = _parse_expr(parser_state)
        pos = parser_state["pos"]
        
        # Consume COLON
        if pos < len(tokens) and tokens[pos]["type"] == "COLON":
            pos += 1
        else:
            parser_state["error"] = f"Expected COLON after elif condition at line {tokens[pos-1]['line']}"
        
        parser_state["pos"] = pos
        elif_block = _parse_block(parser_state)
        pos = parser_state["pos"]
        
        children.append(("ELIF", elif_condition, elif_block))
    
    # 7. Handle ELSE branch
    if pos < len(tokens) and tokens[pos]["type"] == "ELSE":
        pos += 1  # consume ELSE
        
        # Consume COLON
        if pos < len(tokens) and tokens[pos]["type"] == "COLON":
            pos += 1
        else:
            parser_state["error"] = f"Expected COLON after else at line {tokens[pos-1]['line']}"
        
        parser_state["pos"] = pos
        else_block = _parse_block(parser_state)
        pos = parser_state["pos"]
        
        children.append(("ELSE", else_block))
    
    parser_state["pos"] = pos
    
    return {
        "type": "IF_STMT",
        "line": if_token["line"],
        "column": if_token["column"],
        "children": children
    }

# === helper functions ===
# No helper functions needed - logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed - this is a parser sub-function, not a framework entry point
