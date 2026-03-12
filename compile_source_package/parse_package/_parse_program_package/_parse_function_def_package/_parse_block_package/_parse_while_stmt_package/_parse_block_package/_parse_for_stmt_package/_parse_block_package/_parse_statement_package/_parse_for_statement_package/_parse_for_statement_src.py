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
def _parse_for_statement(parser_state: ParserState) -> AST:
    """Parse for-loop statement from token stream."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Step 1: Consume FOR token
    if pos >= len(tokens) or tokens[pos]["type"] != "FOR":
        raise SyntaxError(f"Expected 'for' keyword at {filename}:{tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    for_token = tokens[pos]
    pos += 1
    
    # Step 2: Parse loop variable (IDENT token)
    if pos >= len(tokens) or tokens[pos]["type"] != "IDENT":
        raise SyntaxError(f"Expected loop variable after 'for' at {filename}:{tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    loop_var_token = tokens[pos]
    pos += 1
    
    # Step 3: Consume IN token
    if pos >= len(tokens) or tokens[pos]["type"] != "IN":
        raise SyntaxError(f"Expected 'in' after loop variable at {filename}:{tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    pos += 1
    
    # Step 4: Parse iterable expression (delegate to expression parser)
    parser_state["pos"] = pos
    iter_expr_ast = _parse_expression(parser_state)
    pos = parser_state["pos"]
    
    # Step 5: Consume COLON token
    if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
        raise SyntaxError(f"Expected ':' after for loop header at {filename}:{tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    pos += 1
    
    # Step 6: Parse loop body block (delegate to block parser)
    parser_state["pos"] = pos
    body_ast = _parse_block(parser_state)
    pos = parser_state["pos"]
    
    # Step 7: Consume SEMICOLON token
    if pos >= len(tokens) or tokens[pos]["type"] != "SEMICOLON":
        raise SyntaxError(f"Expected ';' after for loop at {filename}:{tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    pos += 1
    
    # Update parser state
    parser_state["pos"] = pos
    
    # Build FOR_STMT AST node
    return {
        "type": "FOR_STMT",
        "line": for_token["line"],
        "column": for_token["column"],
        "children": [
            {"type": "LOOP_VAR", "value": loop_var_token["value"], "line": loop_var_token["line"], "column": loop_var_token["column"]},
            {"type": "ITER_EXPR", **iter_expr_ast},
            {"type": "BODY", **body_ast}
        ]
    }

# === helper functions ===
def _expect_token(parser_state: ParserState, token_type: str, error_msg: str) -> Token:
    """Helper to expect and consume a token of specific type."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos >= len(tokens) or tokens[pos]["type"] != token_type:
        raise SyntaxError(f"{error_msg} at {filename}:{tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token

# === OOP compatibility layer ===
# Not required for this parser function node
