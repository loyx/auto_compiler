# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_expr_package._parse_multiplicative_expr_src import _parse_multiplicative_expr

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
def _parse_additive_expr(parser_state: ParserState) -> AST:
    """解析加减法层级表达式（PLUS, MINUS）。"""
    left = _parse_multiplicative_expr(parser_state)
    
    while _current_token_is_operator(parser_state):
        op_token = _consume_current_token(parser_state)
        operator = _map_operator_type(op_token["type"])
        right = _parse_multiplicative_expr(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "operator": operator,
            "left": left,
            "right": right,
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
def _current_token_is_operator(parser_state: ParserState) -> bool:
    """检查当前 token 是否为加减运算符。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        return False
    token_type = tokens[pos]["type"]
    return token_type in ("PLUS", "MINUS")

def _consume_current_token(parser_state: ParserState) -> Token:
    """消费当前 token 并返回，原地修改 pos。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', 'unknown')}")
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token

def _map_operator_type(token_type: str) -> str:
    """将 token 类型映射为运算符字符串。"""
    if token_type == "PLUS":
        return "+"
    elif token_type == "MINUS":
        return "-"
    else:
        raise SyntaxError(f"Unknown operator type: {token_type}")

# === OOP compatibility layer ===
# Not required for this parser function node
