# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary
from ._consume_token_package._consume_token_src import _consume_token

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
def _parse_multiplicative(parser_state: ParserState) -> Tuple[AST, ParserState]:
    """
    解析乘除表达式（* / % 运算符）。
    这是表达式优先级链中位于 _parse_unary 之下、_parse_additive 之上的层级。
    支持左结合性，返回 (AST 节点，更新后的 parser_state)。
    """
    # 1. 解析左侧操作数
    left_ast, state = _parse_unary(parser_state)
    
    # 2. 循环处理连续的乘除运算符（左结合性）
    while _is_multiplicative_operator(state):
        # 获取当前运算符 token
        op_token = _get_current_token(state)
        op_type = op_token["type"]
        
        # 3. 消费运算符 token
        _, state = _consume_token(state, op_type)
        
        # 4. 解析右侧操作数
        right_ast, state = _parse_unary(state)
        
        # 5. 构建 BINARY_OP 节点
        left_ast = {
            "type": "BINARY_OP",
            "value": op_token["value"],
            "children": [left_ast, right_ast],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left_ast, state

# === helper functions ===
def _is_multiplicative_operator(state: ParserState) -> bool:
    """检查当前 token 是否为乘除运算符 (* / %)。"""
    token = _get_current_token(state)
    return token is not None and token["type"] in ("STAR", "SLASH", "PERCENT")

def _get_current_token(state: ParserState) -> Token:
    """获取当前位置的 token，如果超出范围则返回 None。"""
    tokens = state["tokens"]
    pos = state["pos"]
    if pos < len(tokens):
        return tokens[pos]
    return {"type": "EOF", "value": "", "line": 0, "column": 0}

# === OOP compatibility layer ===
