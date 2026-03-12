# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._parse_additive_package._parse_additive_src import _parse_additive

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
def _parse_comparison(parser_state: ParserState) -> Tuple[AST, ParserState]:
    """解析比较运算符表达式（更高优先级）。"""
    # 1. 首先解析左侧操作数（更高优先级的加减运算）
    left_ast, state = _parse_additive(parser_state)
    
    # 2. 检查当前 token 是否为比较运算符
    tokens = state["tokens"]
    pos = state["pos"]
    
    if pos >= len(tokens):
        return (left_ast, state)
    
    current_token = tokens[pos]
    operator = current_token.get("value", "")
    
    # 3. 判断是否为比较运算符
    comparison_ops = ["==", "!=", "<", ">", "<=", ">="]
    
    if operator not in comparison_ops:
        return (left_ast, state)
    
    # 4. 消费比较运算符 token
    state = _consume_token(state)
    
    # 5. 解析右侧操作数
    right_ast, state = _parse_additive(state)
    
    # 6. 构建 BINARY_OP AST 节点
    binary_node = {
        "type": "BINARY_OP",
        "value": operator,
        "children": [left_ast, right_ast],
        "line": current_token.get("line", 0),
        "column": current_token.get("column", 0)
    }
    
    return (binary_node, state)

# === helper functions ===
def _consume_token(state: ParserState) -> ParserState:
    """消费当前 token，推进解析位置。"""
    new_state = dict(state)
    new_state["pos"] = state["pos"] + 1
    return new_state

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
