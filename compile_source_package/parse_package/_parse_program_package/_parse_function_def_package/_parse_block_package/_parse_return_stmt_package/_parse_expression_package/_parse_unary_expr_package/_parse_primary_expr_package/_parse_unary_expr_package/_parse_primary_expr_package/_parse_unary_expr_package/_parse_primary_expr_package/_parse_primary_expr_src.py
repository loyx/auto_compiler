# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr

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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, PAREN_EXPR, ERROR, etc.)
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
    """Parse primary expressions (identifiers, literals, parenthesized expressions)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return _make_error_node(-1, -1)
    
    token = tokens[pos]
    token_type = token["type"]
    
    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "children": [],
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    elif token_type in ("NUMBER", "STRING", "BOOLEAN", "NULL"):
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "children": [],
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    elif token_type == "LPAREN":
        parser_state["pos"] += 1
        inner_expr = _parse_unary_expr(parser_state)
        
        if parser_state.get("error"):
            return inner_expr
        
        if parser_state["pos"] >= len(tokens):
            parser_state["error"] = "Expected closing parenthesis"
            return _make_error_node(token["line"], token["column"])
        
        closing_token = tokens[parser_state["pos"]]
        if closing_token["type"] != "RPAREN":
            parser_state["error"] = f"Expected RPAREN, got {closing_token['type']}"
            return _make_error_node(token["line"], token["column"])
        
        parser_state["pos"] += 1
        return inner_expr
    
    else:
        parser_state["error"] = f"Unexpected token: {token_type}"
        return _make_error_node(token["line"], token["column"])

# === helper functions ===
def _make_error_node(line: int, column: int) -> AST:
    """Create an ERROR type AST node."""
    return {
        "type": "ERROR",
        "children": [],
        "value": None,
        "line": line,
        "column": column
    }

# === OOP compatibility layer ===
# Not needed for this parser function node
