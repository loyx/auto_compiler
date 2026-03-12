# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_expr_package._parse_additive_expr_src import _parse_additive_expr

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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
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
def _parse_comparison_expr(parser_state: ParserState) -> AST:
    """解析比较表达式（==, !=, <, >, <=, >=），左结合。"""
    # 1. 解析左操作数
    left = _parse_additive_expr(parser_state)
    
    # 2. 检查当前 token 是否为比较运算符
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    comparison_ops = {"EQ", "NE", "LT", "GT", "LE", "GE"}
    
    if pos < len(tokens) and tokens[pos]["type"] in comparison_ops:
        # 3. 消费运算符 token
        op_token = tokens[pos]
        parser_state["pos"] = pos + 1
        
        operator_str = op_token["value"]
        line = op_token["line"]
        column = op_token["column"]
        
        # 4. 解析右操作数
        right = _parse_additive_expr(parser_state)
        
        # 5. 构建 BINARY_OP 节点
        return {
            "type": "BINARY_OP",
            "value": operator_str,
            "children": [left, right],
            "line": line,
            "column": column
        }
    
    # 无比较运算符，返回左操作数
    return left

# === helper functions ===
# (none needed - logic is inline)

# === OOP compatibility layer ===
# (not needed for parser helper function)
