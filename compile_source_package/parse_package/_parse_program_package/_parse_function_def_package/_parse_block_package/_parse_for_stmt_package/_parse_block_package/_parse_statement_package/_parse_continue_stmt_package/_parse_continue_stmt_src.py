# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions delegated

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (PROGRAM, FUNCTION_DEF, PARAM, VAR_DECL, IF_STMT, WHILE_STMT, FOR_STMT, RETURN_STMT, BREAK_STMT, CONTINUE_STMT, EXPR_STMT, BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, BLOCK)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _parse_continue_stmt(parser_state: ParserState) -> AST:
    """
    Parse continue statement.
    
    Syntax: continue;
    
    Args:
        parser_state: Parser state with pos pointing to CONTINUE token.
                      This function mutates parser_state["pos"].
        
    Returns:
        AST node of type CONTINUE_STMT
        
    Raises:
        SyntaxError: If semicolon is missing or unexpected end of input
        
    Side Effects:
        - Mutates parser_state["pos"] to point after the semicolon token
    """
    # Read tokens from parser_state (GLOBAL_STATE read)
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Step 1: Consume CONTINUE token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected 'continue'")
    
    continue_token = tokens[pos]
    if continue_token["type"] != "CONTINUE":
        raise SyntaxError(f"Expected CONTINUE token, got {continue_token['type']}")
    
    continue_line = continue_token["line"]
    continue_column = continue_token["column"]
    pos += 1
    
    # Step 2: Consume semicolon token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected ';' after continue")
    
    semicolon_token = tokens[pos]
    if semicolon_token["type"] != "SEMICOLON":
        raise SyntaxError(f"Expected ';' after continue, got {semicolon_token['type']}")
    
    pos += 1
    
    # Write updated position to parser_state (GLOBAL_STATE write)
    parser_state["pos"] = pos
    
    # Step 3: Return CONTINUE_STMT AST node
    ast_node: AST = {
        "type": "CONTINUE_STMT",
        "children": [],
        "value": None,
        "line": continue_line,
        "column": continue_column
    }
    
    return ast_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function