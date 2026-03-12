# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_not_expr_package._parse_not_expr_src import _parse_not_expr

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
def _parse_and_expr(parser_state: ParserState) -> AST:
    """
    解析 'and' 表达式（中等优先级）。
    
    语法：not_expr ('and' not_expr)*
    左结合构建 AST。
    """
    # 1. 解析左侧操作数
    left = _parse_not_expr(parser_state)
    
    # 2. 循环检查 'and' token
    while _is_current_token_and(parser_state):
        # 3. 消费 'and' token
        and_token = _consume_token(parser_state)
        
        # 4. 解析右侧操作数
        right = _parse_not_expr(parser_state)
        
        # 5. 构建 BINARY_OP 节点（左结合）
        left = _build_binary_op_node("and", left, right, and_token)
    
    # 6. 返回最终 AST 节点
    return left

# === helper functions ===
def _is_current_token_and(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 'AND' 类型。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos >= len(tokens):
        return False
    token = tokens[pos]
    return token.get("type") == "AND"

def _consume_token(parser_state: ParserState) -> Token:
    """消费当前 token 并返回，同时更新 pos。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token

def _build_binary_op_node(op: str, left: AST, right: AST, op_token: Token) -> AST:
    """构建二元操作 AST 节点。"""
    return {
        "type": "BINARY_OP",
        "value": op,
        "children": [left, right],
        "line": op_token.get("line", left.get("line", 0)),
        "column": op_token.get("column", left.get("column", 0))
    }

# === OOP compatibility layer ===
# Not required for this parser function node
