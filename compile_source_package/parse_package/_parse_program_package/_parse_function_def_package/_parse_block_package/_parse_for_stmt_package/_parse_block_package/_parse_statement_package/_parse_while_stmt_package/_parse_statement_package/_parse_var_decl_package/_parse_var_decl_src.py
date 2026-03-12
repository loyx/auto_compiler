# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_identifier_package._parse_identifier_src import _parse_identifier
from ._parse_expression_package._parse_expression_src import _parse_expression

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
def _parse_var_decl(parser_state: ParserState) -> AST:
    """Parse variable declaration statement: var identifier [: type] [= expression] ;"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Step 1: Current token must be VAR
    if pos >= len(tokens) or tokens[pos]["type"] != "VAR":
        line = tokens[pos]["line"] if pos < len(tokens) else 0
        column = tokens[pos]["column"] if pos < len(tokens) else 0
        raise SyntaxError(f"{filename}:{line}:{column}: expected 'var' keyword")
    
    var_token = tokens[pos]
    pos += 1
    
    # Step 2: Next token must be IDENTIFIER
    if pos >= len(tokens) or tokens[pos]["type"] != "IDENTIFIER":
        line = tokens[pos]["line"] if pos < len(tokens) else var_token["line"]
        column = tokens[pos]["column"] if pos < len(tokens) else var_token["column"]
        raise SyntaxError(f"{filename}:{line}:{column}: expected identifier after 'var'")
    
    # Step 3: Parse identifier
    identifier_ast = _parse_identifier(parser_state)
    pos = parser_state["pos"]
    
    # Step 4: Optional type annotation
    type_ast = None
    if pos < len(tokens) and tokens[pos]["type"] == "COLON":
        pos += 1
        if pos >= len(tokens) or tokens[pos]["type"] != "IDENTIFIER":
            line = tokens[pos]["line"] if pos < len(tokens) else tokens[pos - 1]["line"]
            column = tokens[pos]["column"] if pos < len(tokens) else tokens[pos - 1]["column"]
            raise SyntaxError(f"{filename}:{line}:{column}: expected type identifier after ':'")
        type_ast = _parse_identifier(parser_state)
        pos = parser_state["pos"]
    
    # Step 5: Optional initializer
    initializer_ast = None
    if pos < len(tokens) and tokens[pos]["type"] == "EQUALS":
        pos += 1
        initializer_ast = _parse_expression(parser_state)
        pos = parser_state["pos"]
    
    # Step 6: Must end with SEMICOLON
    if pos >= len(tokens) or tokens[pos]["type"] != "SEMICOLON":
        line = tokens[pos]["line"] if pos < len(tokens) else tokens[pos - 1]["line"]
        column = tokens[pos]["column"] if pos < len(tokens) else tokens[pos - 1]["column"]
        raise SyntaxError(f"{filename}:{line}:{column}: expected ';' at end of variable declaration")
    
    pos += 1
    parser_state["pos"] = pos
    
    # Step 7: Return VAR_DECL AST node
    children = [identifier_ast]
    if type_ast is not None:
        children.append(type_ast)
    else:
        children.append(None)
    if initializer_ast is not None:
        children.append(initializer_ast)
    else:
        children.append(None)
    
    return {
        "type": "VAR_DECL",
        "children": children,
        "line": var_token["line"],
        "column": var_token["column"]
    }

# === helper functions ===

# === OOP compatibility layer ===
