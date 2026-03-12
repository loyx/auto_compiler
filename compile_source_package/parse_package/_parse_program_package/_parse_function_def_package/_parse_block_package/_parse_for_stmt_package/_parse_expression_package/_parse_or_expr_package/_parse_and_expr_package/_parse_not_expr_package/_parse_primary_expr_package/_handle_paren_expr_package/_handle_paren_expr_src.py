# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._build_error_node_package._build_error_node_src import _build_error_node

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (大写字符串)
#   "value": str,            # token 值 (原始字符串)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (IDENTIFIER, LITERAL, CALL, ERROR, etc.)
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
def _handle_paren_expr(parser_state: ParserState, lparen_token: Token) -> AST:
    """
    处理括号表达式：( expression )
    
    1. 消费 LPAREN token
    2. 递归解析内部表达式
    3. 验证并消费 RPAREN
    4. 返回内部表达式的 AST 节点或 ERROR 节点
    """
    tokens = parser_state["tokens"]
    
    # 1. 消费 LPAREN token
    parser_state["pos"] += 1
    
    # 2. 检查是否到达 token 末尾
    if parser_state["pos"] >= len(tokens):
        return _build_error_node(
            parser_state,
            "unexpected end of input inside parentheses",
            lparen_token["line"],
            lparen_token["column"]
        )
    
    # 3. 递归解析括号内的完整表达式
    inner_ast = _parse_expression(parser_state)
    
    # 4. 检查是否还有 token 用于匹配 RPAREN
    if parser_state["pos"] >= len(tokens):
        return _build_error_node(
            parser_state,
            "expected ')' but found end of input",
            lparen_token["line"],
            lparen_token["column"]
        )
    
    # 5. 检查当前 token 是否为 RPAREN
    current_token = tokens[parser_state["pos"]]
    if current_token["type"] != "RPAREN":
        return _build_error_node(
            parser_state,
            f"expected ')' but found '{current_token['value']}'",
            current_token["line"],
            current_token["column"]
        )
    
    # 6. 消费 RPAREN token
    parser_state["pos"] += 1
    
    # 7. 返回内部表达式的 AST 节点
    return inner_ast

# === helper functions ===

# === OOP compatibility layer ===
