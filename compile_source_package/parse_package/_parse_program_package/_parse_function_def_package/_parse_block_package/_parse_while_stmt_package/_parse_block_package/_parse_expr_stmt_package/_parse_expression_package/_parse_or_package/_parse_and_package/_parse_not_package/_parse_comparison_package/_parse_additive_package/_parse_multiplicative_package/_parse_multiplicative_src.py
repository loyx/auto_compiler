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
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_multiplicative(parser_state: ParserState) -> AST:
    """
    解析乘除表达式（*, /），优先级高于加减运算符，低于一元运算符。
    
    处理行为：
    1. 调用 _parse_unary 解析左操作数
    2. 检查当前 token 是否为乘除运算符（ARITH_OP 类型，值为 * 或 /）
    3. 如果是：记录位置，消费运算符，解析右操作数，构建 BINARY_OP AST
    4. 如果不是：直接返回左操作数 AST
    5. 返回 AST 节点
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 解析左操作数（下一优先级：一元表达式）
    left = _parse_unary(parser_state)
    
    # 检查当前 token 是否为乘除运算符
    if pos < len(tokens):
        current_token = tokens[pos]
        if current_token.get("type") == "ARITH_OP" and current_token.get("value") in ("*", "/"):
            op_value = current_token["value"]
            line = current_token.get("line", 0)
            column = current_token.get("column", 0)
            
            # 消费运算符 token
            parser_state["pos"] = pos + 1
            
            # 解析右操作数
            right = _parse_unary(parser_state)
            
            # 构建 BINARY_OP AST
            return {
                "type": "BINARY_OP",
                "operator": op_value,
                "children": [left, right],
                "line": line,
                "column": column
            }
    
    # 没有乘除运算符，返回左操作数
    return left

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function