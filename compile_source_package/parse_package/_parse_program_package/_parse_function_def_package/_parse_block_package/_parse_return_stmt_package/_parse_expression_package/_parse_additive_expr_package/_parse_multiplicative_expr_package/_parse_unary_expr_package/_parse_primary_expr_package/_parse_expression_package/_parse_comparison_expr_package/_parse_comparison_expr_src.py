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
def _parse_comparison_expr(parser_state: ParserState) -> AST:
    """解析比较运算符层级表达式（EQ, NE, LT, LE, GT, GE）。"""
    # 解析左侧表达式
    left = _parse_additive_expr(parser_state)
    
    # 比较运算符映射
    comparison_ops = {"EQ": "==", "NE": "!=", "LT": "<", "LE": "<=", "GT": ">", "GE": ">="}
    
    # 当当前 token 是比较运算符时，循环处理
    while parser_state["pos"] < len(parser_state["tokens"]):
        token = parser_state["tokens"][parser_state["pos"]]
        if token["type"] not in comparison_ops:
            break
        
        # 记录运算符位置
        line = token["line"]
        column = token["column"]
        operator = comparison_ops[token["type"]]
        
        # 消费运算符 token
        parser_state["pos"] += 1
        
        # 解析右侧表达式
        right = _parse_additive_expr(parser_state)
        
        # 构建 BINARY_OP AST 节点
        left = {
            "type": "BINARY_OP",
            "operator": operator,
            "left": left,
            "right": right,
            "line": line,
            "column": column
        }
    
    return left

# === helper functions ===

# === OOP compatibility layer ===
