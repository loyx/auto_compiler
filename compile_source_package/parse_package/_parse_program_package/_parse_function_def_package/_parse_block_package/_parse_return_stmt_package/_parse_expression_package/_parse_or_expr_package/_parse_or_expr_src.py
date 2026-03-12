# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_expr_package._parse_and_expr_src import _parse_and_expr

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
def _parse_or_expr(parser_state: ParserState) -> AST:
    """
    解析 OR 表达式（|| 运算符，左结合）。
    
    算法：
    1. 调用 _parse_and_expr 获取左操作数
    2. 循环检查当前 token 是否为 "OR" 类型
    3. 如果是，消费 token，构建 BINARY_OP 节点
    4. 继续循环直到没有更多 ||
    5. 返回最终 AST 节点
    """
    # 解析左操作数
    left = _parse_and_expr(parser_state)
    
    # 循环处理 || 运算符
    while _is_current_token_or(parser_state):
        # 记录运算符位置
        op_token = _get_current_token(parser_state)
        line = op_token.get("line", 0)
        column = op_token.get("column", 0)
        
        # 消费 OR token
        _consume_token(parser_state)
        
        # 解析右操作数
        right = _parse_and_expr(parser_state)
        
        # 构建 BINARY_OP 节点
        left = {
            "type": "BINARY_OP",
            "value": "||",
            "children": [left, right],
            "line": line,
            "column": column
        }
    
    return left

# === helper functions ===
def _is_current_token_or(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 OR 类型。"""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    if pos >= len(tokens):
        return False
    token = tokens[pos]
    return token.get("type") == "OR"

def _get_current_token(parser_state: ParserState) -> Token:
    """获取当前 token。"""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    if pos >= len(tokens):
        return {"type": "EOF", "value": "", "line": 0, "column": 0}
    return tokens[pos]

def _consume_token(parser_state: ParserState) -> None:
    """消费当前 token（前进 pos）。"""
    parser_state["pos"] = parser_state.get("pos", 0) + 1

# === OOP compatibility layer ===
# Not required for this parser function node
