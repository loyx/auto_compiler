# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_for_binary_package._parse_primary_for_binary_src import _parse_primary_for_binary

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

# Operator precedence mapping (higher number = higher precedence)
OPERATOR_PRECEDENCE = {
    "EQUAL": 1,           # 赋值 - 最低优先级
    "OR": 2,              # 逻辑或
    "AND": 3,             # 逻辑与
    "EQUAL_EQUAL": 4,     # 比较 ==
    "BANG_EQUAL": 4,      # 比较 !=
    "LESS": 4,            # 比较 <
    "LESS_EQUAL": 4,      # 比较 <=
    "GREATER": 4,         # 比较 >
    "GREATER_EQUAL": 4,   # 比较 >=
    "PLUS": 5,            # 加法
    "MINUS": 5,           # 减法
    "STAR": 6,            # 乘法
    "SLASH": 6,           # 除法
}

# === main function ===
def _parse_binary_op(parser_state: ParserState, min_precedence: int, left: AST) -> AST:
    """
    使用运算符优先级爬升算法解析二元运算表达式。
    
    Args:
        parser_state: 解析器状态，包含 tokens 列表和当前位置 pos
        min_precedence: 最小优先级阈值，用于 precedence climbing
        left: 左侧表达式的 AST 节点（已解析完成）
    
    Returns:
        完整表达式的 AST 节点
    """
    result = left
    
    while True:
        tokens = parser_state["tokens"]
        pos = parser_state["pos"]
        
        if pos >= len(tokens):
            break
        
        current_token = tokens[pos]
        token_type = current_token["type"]
        
        if token_type not in OPERATOR_PRECEDENCE:
            break
        
        op_precedence = OPERATOR_PRECEDENCE[token_type]
        if op_precedence < min_precedence:
            break
        
        parser_state["pos"] += 1
        operator_token = current_token
        
        next_min_precedence = op_precedence + 1 if token_type != "EQUAL" else op_precedence
        
        right = _parse_primary_for_binary(parser_state)
        right = _parse_binary_op(parser_state, next_min_precedence, right)
        
        result = {
            "type": "BinaryOp",
            "operator": operator_token["value"],
            "operator_token": operator_token,
            "left": result,
            "right": right,
            "line": operator_token["line"],
            "column": operator_token["column"]
        }
    
    return result

# === helper functions ===
# No helper functions - all logic delegated to sub functions

# === OOP compatibility layer ===
# Not required for this function node
