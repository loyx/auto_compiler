# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (IDENTIFIER, NUMBER, STRING, LPAREN, RPAREN, OPERATOR, etc.)
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (UNARY_OP, IDENTIFIER, LITERAL, ERROR, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值（operator 符号或字面量值）
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息
# }

# === main function ===
def _parse_unary_expr(parser_state: ParserState) -> AST:
    """解析一元表达式（unary expression）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 如果 token 已到末尾，解析基本表达式
    if pos >= len(tokens):
        return _parse_primary_expr(parser_state)
    
    current_token = tokens[pos]
    
    # 检查是否为一元运算符
    if current_token["type"] == "OPERATOR" and current_token["value"] in ("-", "+", "!", "~"):
        # 消费运算符 token
        parser_state["pos"] += 1
        op_token = current_token
        
        # 递归解析后面的表达式（支持连续一元运算符）
        operand_ast = _parse_unary_expr(parser_state)
        
        # 创建 UNARY_OP 节点
        return {
            "type": "UNARY_OP",
            "children": [operand_ast],
            "value": op_token["value"],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    # 否则解析基本表达式
    return _parse_primary_expr(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
