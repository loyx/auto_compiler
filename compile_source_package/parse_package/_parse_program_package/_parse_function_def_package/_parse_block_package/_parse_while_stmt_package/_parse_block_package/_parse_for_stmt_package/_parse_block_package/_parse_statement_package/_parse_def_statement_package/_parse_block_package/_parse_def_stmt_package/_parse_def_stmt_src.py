# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_param_list_package._parse_param_list_src import _parse_param_list

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
def _parse_def_stmt(parser_state: ParserState) -> AST:
    """Parse def statement (function definition with nesting support)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. Consume DEF keyword
    if pos >= len(tokens) or tokens[pos]["type"] != "DEF":
        raise SyntaxError(f"Expected DEF keyword at {parser_state.get('filename', 'unknown')}")
    def_token = tokens[pos]
    pos += 1
    
    # 2. Consume function name identifier
    if pos >= len(tokens) or tokens[pos]["type"] != "IDENTIFIER":
        raise SyntaxError(f"Expected function name after DEF at line {def_token['line']}")
    name_token = tokens[pos]
    pos += 1
    
    # 3. Consume LPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "LPAREN":
        raise SyntaxError(f"Expected '(' after function name at line {name_token['line']}")
    pos += 1
    
    # 4. Parse parameter list (if any)
    params_ast = []
    if pos < len(tokens) and tokens[pos]["type"] != "RPAREN":
        params_ast = _parse_param_list(parser_state)
        pos = parser_state["pos"]
    
    # 5. Consume RPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "RPAREN":
        raise SyntaxError(f"Expected ')' after parameters at line {def_token['line']}")
    pos += 1
    
    # 6. Consume COLON (block start marker)
    if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
        raise SyntaxError(f"Expected ':' after ')' at line {def_token['line']}")
    pos += 1
    parser_state["pos"] = pos
    
    # 7. Parse function body block (lazy import to avoid circular dependency)
    from ._parse_block_package._parse_block_src import _parse_block
    body_ast = _parse_block(parser_state)
    pos = parser_state["pos"]
    
    # 8. Build DEF AST node
    func_name_ast = {
        "type": "FUNC_NAME",
        "value": name_token["value"],
        "line": name_token["line"],
        "column": name_token["column"]
    }
    
    params_node = {
        "type": "PARAMS",
        "children": params_ast,
        "line": def_token["line"],
        "column": def_token["column"]
    }
    
    result = {
        "type": "DEF",
        "line": def_token["line"],
        "column": def_token["column"],
        "children": [func_name_ast, params_node, body_ast]
    }
    
    return result

# === helper functions ===

# === OOP compatibility layer ===
