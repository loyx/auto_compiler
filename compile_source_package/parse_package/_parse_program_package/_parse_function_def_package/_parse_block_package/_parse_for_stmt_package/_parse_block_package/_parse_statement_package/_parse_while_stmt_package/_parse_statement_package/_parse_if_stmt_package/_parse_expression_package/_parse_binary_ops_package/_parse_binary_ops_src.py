# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

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

# === main function ===
def _parse_binary_ops(parser_state: ParserState, left: AST, filename: str) -> AST:
    """
    解析二元运算符并构建 AST。
    支持比较运算符 (==, !=, <, >, <=, >=) 和逻辑运算符 (&&, ||)。
    处理左结合性，原地更新 parser_state["pos"]。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 定义支持的二元运算符
    BINARY_OPS = {"==", "!=", "<", ">", "<=", ">=", "&&", "||"}
    
    # 循环处理左结合的连续二元运算符
    result = left
    while pos < len(tokens):
        token = tokens[pos]
        
        # 检查是否为二元运算符
        if token.get("type") != "OPERATOR" or token.get("value") not in BINARY_OPS:
            break
        
        # 消耗运算符 token
        op_token = token
        pos += 1
        
        # 解析右操作数
        parser_state["pos"] = pos
        right = _parse_primary(parser_state, filename)
        pos = parser_state.get("pos", pos)
        
        # 构建 BINOP 节点
        result = {
            "type": "BINOP",
            "children": [result, right],
            "value": op_token["value"],
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0)
        }
    
    # 最终更新 pos
    parser_state["pos"] = pos
    return result

# === helper functions ===
def _is_binary_op(token: Token) -> bool:
    """检查 token 是否为支持的二元运算符。"""
    BINARY_OPS = {"==", "!=", "<", ">", "<=", ">=", "&&", "||"}
    return token.get("type") == "OPERATOR" and token.get("value") in BINARY_OPS

# === OOP compatibility layer ===
# 不需要 OOP wrapper，此为普通函数节点
