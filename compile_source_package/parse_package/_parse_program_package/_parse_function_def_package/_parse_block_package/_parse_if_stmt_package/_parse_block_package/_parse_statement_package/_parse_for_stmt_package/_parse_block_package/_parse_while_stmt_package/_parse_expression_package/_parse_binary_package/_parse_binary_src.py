# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary
from ._get_token_package._get_token_src import _get_token
from ._advance_package._advance_src import _advance

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

# 运算符优先级映射
OPERATOR_PRECEDENCE = {
    "or": 1,
    "and": 2,
    "==": 3, "!=": 3,
    "<": 4, ">": 4, "<=": 4, ">=": 4,
    "+": 5, "-": 5,
    "*": 6, "/": 6,
}

BINARY_OPERATORS = set(OPERATOR_PRECEDENCE.keys())

# === main function ===
def _parse_binary(parser_state: dict, min_prec: int) -> dict:
    """
    使用优先级爬升算法解析二元运算符表达式。
    
    算法步骤：
    1. 解析左操作数（调用 _parse_unary）
    2. 循环检查后续 token 是否为二元运算符
    3. 如果运算符优先级 >= min_prec，则解析右操作数并构建 AST
    4. 返回最终的 AST 节点
    """
    # 步骤 1: 解析左操作数
    left_ast = _parse_unary(parser_state)
    
    # 步骤 2: 循环处理二元运算符
    while True:
        token = _get_token(parser_state)
        if token is None:
            break
        
        token_value = token.get("value", "")
        if token_value not in BINARY_OPERATORS:
            break
        
        # 检查运算符优先级
        op_prec = OPERATOR_PRECEDENCE[token_value]
        if op_prec < min_prec:
            break
        
        # 记录运算符信息
        op_token = token
        _advance(parser_state)
        
        # 步骤 3: 计算右操作数的最小优先级（左结合：op_prec + 1）
        right_min_prec = op_prec + 1
        
        # 递归解析右操作数
        right_ast = _parse_binary(parser_state, right_min_prec)
        
        # 步骤 4: 构建二元运算符 AST 节点
        left_ast = {
            "type": "binary_op",
            "value": op_token.get("value"),
            "children": [left_ast, right_ast],
            "line": op_token.get("line"),
            "column": op_token.get("column"),
        }
    
    return left_ast

# === helper functions ===
# Helper functions are delegated to child modules

# === OOP compatibility layer ===
# Not required for this parser function node
