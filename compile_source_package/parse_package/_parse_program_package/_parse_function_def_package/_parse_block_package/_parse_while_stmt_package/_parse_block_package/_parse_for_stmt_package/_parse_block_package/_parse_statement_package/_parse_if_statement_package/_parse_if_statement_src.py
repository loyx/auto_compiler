# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block
from ._parse_elif_branch_package._parse_elif_branch_src import _parse_elif_branch
from ._parse_else_branch_package._parse_else_branch_src import _parse_else_branch

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
def _parse_if_statement(parser_state: ParserState) -> AST:
    """Parse if-elif-else conditional statement."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "unknown")
    
    # Verify and consume IF token
    if pos >= len(tokens) or tokens[pos]["type"] != "IF":
        raise SyntaxError(f"Expected IF keyword at {filename}")
    if_token = tokens[pos]
    parser_state["pos"] += 1
    
    # Parse IF(...) structure
    _consume_token(parser_state, "LPAREN", "after IF")
    condition_ast = _parse_expression(parser_state)
    _consume_token(parser_state, "RPAREN", "after condition")
    _consume_token(parser_state, "COLON", "after condition")
    
    # Parse then block
    _consume_token(parser_state, "LBRACE", "after ':'")
    then_block = _parse_block(parser_state)
    _consume_token(parser_state, "RBRACE", "after block")
    
    # Process ELIF branches
    elif_branches = []
    while parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] == "ELIF":
        elif_branches.append(_parse_elif_branch(parser_state, if_token))
    
    # Process optional ELSE branch
    else_block = None
    if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] == "ELSE":
        else_block = _parse_else_branch(parser_state, if_token)
    
    # Consume SEMICOLON
    _consume_token(parser_state, "SEMICOLON", "after if statement")
    
    # Build AST node
    return {
        "type": "IF_STMT",
        "line": if_token["line"],
        "column": if_token["column"],
        "children": {
            "condition": condition_ast,
            "then_block": then_block,
            "elif_branches": elif_branches,
            "else_block": else_block
        }
    }

# === helper functions ===
def _consume_token(parser_state: ParserState, expected_type: str, context: str) -> None:
    """Consume expected token type or raise SyntaxError."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "unknown")
    
    if pos >= len(tokens) or tokens[pos]["type"] != expected_type:
        token_info = tokens[pos] if pos < len(tokens) else {"line": "?", "column": "?"}
        raise SyntaxError(f"Expected '{expected_type}' {context} at {filename}:{token_info.get('line', '?')}:{token_info.get('column', '?')}")
    parser_state["pos"] += 1

# === OOP compatibility layer ===
# Not required for parser function nodes
