# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions - all parser functions are in the same file
# _parse_expression is a sibling function in the same module (forward reference)

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (AND, OR, NOT, IDENTIFIER, LITERAL, LPAREN, RPAREN, etc.)
#   "value": str,            # token 值（源代码中的实际字符）
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
#   "operator": str,         # 运算符 (仅 BINARY_OP/UNARY_OP)
#   "left": AST,             # 左操作数 (仅 BINARY_OP)
#   "right": AST,            # 右操作数 (仅 BINARY_OP)
#   "operand": AST,          # 操作数 (仅 UNARY_OP)
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
def _parse_primary_expr(parser_state: ParserState) -> AST:
    """
    Parse atomic expressions (identifiers, literals, parenthesized expressions).
    
    Args:
        parser_state: ParserState dict with tokens, pos, filename
        
    Returns:
        AST node dict
        
    Raises:
        SyntaxError: On unexpected token or parse failure
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if we've reached the end of tokens
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    line = current_token["line"]
    column = current_token["column"]
    
    # Handle IDENTIFIER
    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "value": current_token["value"],
            "line": line,
            "column": column
        }
    
    # Handle LITERAL (numbers, strings, etc.)
    if token_type == "LITERAL":
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "value": current_token["value"],
            "line": line,
            "column": column
        }
    
    # Handle LPAREN (parenthesized expression)
    if token_type == "LPAREN":
        parser_state["pos"] += 1  # consume '('
        # Call _parse_expression to parse inner expression (sibling function in same module)
        inner_expr = _parse_expression(parser_state)  # type: ignore
        # Check and consume RPAREN
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(f"Expected ')' at line {line}")
        closing_token = tokens[parser_state["pos"]]
        if closing_token["type"] != "RPAREN":
            raise SyntaxError(f"Expected ')' at line {closing_token['line']}, got '{closing_token['value']}'")
        parser_state["pos"] += 1  # consume ')'
        return inner_expr
    
    # Unexpected token
    raise SyntaxError(f"Unexpected token '{current_token['value']}' at line {line}, column {column}")


# === helper functions ===
# No helper functions needed - all logic is inline

# Forward reference stub for _parse_expression (will be implemented by sibling agent in same file)
def _parse_expression(parser_state: ParserState) -> AST:  # type: ignore
    """Stub - actual implementation provided by sibling function in same module."""
    raise NotImplementedError("This stub will be replaced by actual _parse_expression implementation")


# === OOP compatibility layer ===
# No OOP wrapper needed - this is a parser function, not a framework entry point
