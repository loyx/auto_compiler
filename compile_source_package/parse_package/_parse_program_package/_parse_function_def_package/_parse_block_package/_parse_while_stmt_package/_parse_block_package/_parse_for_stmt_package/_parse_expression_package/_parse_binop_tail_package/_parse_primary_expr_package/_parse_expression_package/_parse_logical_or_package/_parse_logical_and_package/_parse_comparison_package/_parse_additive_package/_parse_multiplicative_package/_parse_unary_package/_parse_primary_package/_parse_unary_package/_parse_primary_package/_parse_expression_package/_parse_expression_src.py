# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary

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
#   "operator": str,
#   "operand": Any,
#   "name": str,
#   "message": str,
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

# === main function ===
def _parse_expression(parser_state: ParserState) -> AST:
    """
    解析完整表达式（包括运算符优先级）。
    输入：parser_state（解析器状态，会被修改 pos）
    输出：AST 节点
    """
    # 首先解析左侧操作数（处理一元运算符）
    left = _parse_unary(parser_state)
    
    # 如果左侧解析出错，直接返回
    if left.get("type") == "ERROR":
        return left
    
    # 使用优先级爬升算法处理二元运算符
    return _parse_binary_op(parser_state, left, 0)

# === helper functions ===
def _parse_binary_op(parser_state: ParserState, left: AST, min_precedence: int) -> AST:
    """
    处理二元运算符（优先级爬升算法）。
    left: 已经解析好的左侧操作数 AST
    min_precedence: 最小优先级阈值
    """
    tokens = parser_state["tokens"]
    
    while True:
        pos = parser_state["pos"]
        if pos >= len(tokens):
            break
        
        token = tokens[pos]
        token_type = token["type"]
        
        # 获取当前 token 的运算符优先级
        precedence = _get_operator_precedence(token_type)
        
        # 如果优先级低于阈值，停止处理
        if precedence < min_precedence:
            break
        
        # 消费运算符 token
        parser_state["pos"] = pos + 1
        
        # 解析右侧操作数（优先级 +1 保证右结合性）
        right = _parse_unary(parser_state)
        if right.get("type") == "ERROR":
            return right
        
        # 处理右结合运算符（如幂运算），这里假设所有运算符都是左结合
        # 继续处理更高优先级的运算符
        right = _parse_binary_op(parser_state, right, precedence + 1)
        if right.get("type") == "ERROR":
            return right
        
        # 构建二元运算 AST 节点
        left = {
            "type": "BINARY",
            "operator": token["value"],
            "children": [left, right],
            "line": token["line"],
            "column": token["column"]
        }
    
    return left

def _get_operator_precedence(token_type: str) -> int:
    """
    获取运算符优先级（数字越大优先级越高）。
    """
    precedence_map = {
        "OR": 1,
        "AND": 2,
        "EQUAL": 3,
        "NOT_EQUAL": 3,
        "LESS": 4,
        "GREATER": 4,
        "LESS_EQUAL": 4,
        "GREATER_EQUAL": 4,
        "PLUS": 5,
        "MINUS": 5,
        "STAR": 6,
        "SLASH": 6,
    }
    return precedence_map.get(token_type, 0)

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes
