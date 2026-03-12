# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_package._parse_comparison_src import _parse_comparison
from ._expect_token_package._expect_token_src import _expect_token

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (PLUS, MINUS, STAR, SLASH, PERCENT, EQ, NE, LT, GT, LE, GE, AND, OR, BANG, IDENTIFIER, INTEGER, STRING, LPAREN, RPAREN)
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL)
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
def _parse_logical_and(parser_state: ParserState) -> AST:
    """
    解析逻辑 AND 表达式（&& 运算符）。
    优先级高于 OR，低于比较运算符。
    左结合：((a && b) && c)
    """
    # 解析左侧操作数（比较表达式）
    left = _parse_comparison(parser_state)
    
    # 循环处理 && 运算符（左结合）
    while _current_token_is_and(parser_state):
        # 记录 && token 位置用于错误报告
        and_token = _get_current_token(parser_state)
        
        # 消耗 AND token
        _expect_token(parser_state, "AND")
        
        # 解析右侧操作数
        right = _parse_comparison(parser_state)
        
        # 构建 BINARY_OP 节点
        left = {
            "type": "BINARY_OP",
            "value": "&&",
            "children": [left, right],
            "line": and_token["line"],
            "column": and_token["column"]
        }
    
    return left

# === helper functions ===
def _current_token_is_and(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 AND (&&)。"""
    token = _get_current_token(parser_state)
    return token is not None and token["type"] == "AND"

def _get_current_token(parser_state: ParserState) -> Token:
    """获取当前 token，如果已到达末尾则返回 None。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos < len(tokens):
        return tokens[pos]
    return None

# === OOP compatibility layer ===
# Not required for this parser function node
