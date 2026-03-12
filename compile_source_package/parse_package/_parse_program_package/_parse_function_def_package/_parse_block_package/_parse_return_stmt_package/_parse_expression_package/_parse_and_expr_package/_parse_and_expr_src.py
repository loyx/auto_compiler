# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_expr_package._parse_comparison_expr_src import _parse_comparison_expr

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
    解析 AND 表达式（处理 && 运算符，左结合）。
    
    算法：
    1. 调用 _parse_comparison_expr 获取左操作数
    2. 循环检查当前 token 是否为 "AND" 类型
    3. 如果是，消费 token，构建 BINARY_OP 节点
    4. 继续循环直到没有更多 &&
    5. 返回最终的 AST 节点
    """
    # 解析左操作数
    left = _parse_comparison_expr(parser_state)
    
    # 循环处理 && 运算符
    while _is_current_token_and(parser_state):
        # 记录运算符位置
        op_line = _get_current_token_line(parser_state)
        op_column = _get_current_token_column(parser_state)
        
        # 消费 AND token
        _consume_token(parser_state)
        
        # 解析右操作数
        right = _parse_comparison_expr(parser_state)
        
        # 构建 BINARY_OP 节点
        left = {
            "type": "BINARY_OP",
            "value": "&&",
            "children": [left, right],
            "line": op_line,
            "column": op_column
        }
    
    return left

# === helper functions ===
def _is_current_token_and(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 AND 类型。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos >= len(tokens):
        return False
    token = tokens[pos]
    return token.get("type") == "AND"

def _get_current_token_line(parser_state: ParserState) -> int:
    """获取当前 token 的行号。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos >= len(tokens):
        return 0
    return tokens[pos].get("line", 0)

def _get_current_token_column(parser_state: ParserState) -> int:
    """获取当前 token 的列号。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos >= len(tokens):
        return 0
    return tokens[pos].get("column", 0)

def _consume_token(parser_state: ParserState) -> None:
    """消费当前 token（更新 pos）。"""
    parser_state["pos"] = parser_state.get("pos", 0) + 1

# === OOP compatibility layer ===
# Not needed for this parser function node
