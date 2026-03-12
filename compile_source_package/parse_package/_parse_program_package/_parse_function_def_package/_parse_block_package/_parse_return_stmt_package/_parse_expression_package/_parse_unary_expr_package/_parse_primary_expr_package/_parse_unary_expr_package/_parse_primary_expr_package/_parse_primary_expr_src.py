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
    """解析基本表达式（标识符、字面量、括号表达式）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否超出范围
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return _create_error_node("Unexpected end of input", parser_state)
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    token_value = current_token["value"]
    token_line = current_token["line"]
    token_column = current_token["column"]
    
    # 根据 token 类型处理
    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "children": [],
            "value": token_value,
            "line": token_line,
            "column": token_column
        }
    
    elif token_type in ("NUMBER", "STRING", "BOOLEAN", "NULL"):
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "children": [],
            "value": token_value,
            "line": token_line,
            "column": token_column
        }
    
    elif token_type == "LPAREN":
        parser_state["pos"] += 1
        # 调用 _parse_unary_expr 解析括号内表达式
        inner_expr = _parse_unary_expr(parser_state)
        
        # 检查是否有错误
        if parser_state.get("error"):
            return inner_expr
        
        # 检查并消费匹配的 RPAREN
        if parser_state["pos"] >= len(tokens):
            parser_state["error"] = "Missing closing parenthesis"
            return _create_error_node("Missing closing parenthesis", parser_state)
        
        closing_token = tokens[parser_state["pos"]]
        if closing_token["type"] != "RPAREN":
            parser_state["error"] = f"Expected RPAREN, got {closing_token['type']}"
            return _create_error_node(f"Expected RPAREN, got {closing_token['type']}", parser_state)
        
        parser_state["pos"] += 1
        
        return {
            "type": "PAREN_EXPR",
            "children": [inner_expr],
            "value": None,
            "line": token_line,
            "column": token_column
        }
    
    else:
        parser_state["error"] = f"Unexpected token: {token_type}"
        return _create_error_node(f"Unexpected token: {token_type}", parser_state)

# === helper functions ===
def _create_error_node(message: str, parser_state: ParserState) -> AST:
    """创建错误类型的 AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos < len(tokens):
        token = tokens[pos]
        line = token["line"]
        column = token["column"]
    else:
        line = 0
        column = 0
    
    return {
        "type": "ERROR",
        "children": [],
        "value": message,
        "line": line,
        "column": column
    }

# === OOP compatibility layer ===
# No OOP wrapper needed for parser helper function
