# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_statement_package._parse_statement_src import _parse_statement
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block
from ._expect_token_package._expect_token_src import _expect_token

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
#   "type": str,             # e.g., FOR_STMT, VAR_DECL, EXPR_STMT
#   "children": list,        # child AST nodes
#   "value": str,            # token value
#   "line": int,             # source line number
#   "column": int            # source column number
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # list of Token
#   "pos": int,              # current position in tokens
#   "filename": str,         # source filename
#   "error": str             # error message (if any)
# }

# === main function ===
def _parse_for_stmt(parser_state: dict) -> dict:
    """
    Parse a for statement.
    
    Grammar: for ( init_stmt ; condition_expr ; update_expr ) block
    
    Args:
        parser_state: Parser state with pos pointing to FOR token.
    
    Returns:
        FOR_STMT AST node with children: [init, condition, update, body]
    
    Side effects:
        Updates parser_state['pos'] to after the for statement.
    
    Raises:
        SyntaxError: If for statement syntax is invalid.
    """
    tokens = parser_state["tokens"]
    start_pos = parser_state["pos"]
    
    # Step 1: Consume FOR token
    if start_pos >= len(tokens) or tokens[start_pos]["type"] != "FOR":
        raise SyntaxError(f"Expected FOR token at {parser_state.get('filename', 'unknown')}")
    for_token = tokens[start_pos]
    parser_state["pos"] += 1
    
    # Step 2: Consume LPAREN token
    _expect_token(parser_state, "LPAREN")
    
    # Step 3: Parse initialization statement
    init_ast = _parse_statement(parser_state)
    
    # Step 4: Parse condition expression
    condition_ast = _parse_expression(parser_state)
    
    # Step 5: Parse update expression
    update_ast = _parse_expression(parser_state)
    
    # Step 6: Consume RPAREN token
    _expect_token(parser_state, "RPAREN")
    
    # Step 7: Parse body block
    body_ast = _parse_block(parser_state)
    
    # Step 8: Build FOR_STMT AST node
    for_stmt_ast = {
        "type": "FOR_STMT",
        "children": [init_ast, condition_ast, update_ast, body_ast],
        "value": "for",
        "line": for_token.get("line", 0),
        "column": for_token.get("column", 0)
    }
    
    return for_stmt_ast

# === helper functions ===
# No helper functions needed; all logic delegated to sub-functions.

# === OOP compatibility layer ===
# Not required for this parser function node.
