# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_and_package._parse_and_src import _parse_and

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
def _parse_or(parser_state: ParserState) -> AST:
    """
    解析逻辑或表达式（|| 运算符）。
    这是最低优先级的二元运算符，实现左结合。
    """
    # 解析左侧操作数（更高优先级的 AND 表达式）
    left = _parse_and(parser_state)
    
    # 循环处理左结合的 || 运算符
    while _current_token_is_or(parser_state):
        # 消耗 OR token
        or_token = _consume_token(parser_state, "OR")
        
        # 解析右侧操作数（递归调用实现左结合）
        right = _parse_or(parser_state)
        
        # 构建 BINARY_OP 节点
        left = _build_binary_op_node(left, right, or_token)
    
    return left

# === helper functions ===
def _current_token_is_or(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 OR 类型。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos >= len(tokens):
        return False
    token = tokens[pos]
    return token.get("type") == "OR"

def _build_binary_op_node(left: AST, right: AST, or_token: Token) -> AST:
    """构建二元运算符 AST 节点。"""
    return {
        "type": "BINARY_OP",
        "children": [left, right],
        "value": "||",
        "line": or_token.get("line", 0),
        "column": or_token.get("column", 0)
    }

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
