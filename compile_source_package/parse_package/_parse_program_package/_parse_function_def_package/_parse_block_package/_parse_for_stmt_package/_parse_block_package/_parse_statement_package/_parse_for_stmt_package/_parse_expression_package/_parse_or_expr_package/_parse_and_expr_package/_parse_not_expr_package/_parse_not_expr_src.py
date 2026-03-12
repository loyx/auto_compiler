# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._current_token_package._current_token_src import _current_token
from ._advance_package._advance_src import _advance

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
def _parse_not_expr(parser_state: ParserState) -> AST:
    """
    解析 not 一元表达式。
    
    若当前 token 为 'not' 关键字，则消耗该 token 并递归解析 not 表达式，
    构建 UNARY_OP 节点。否则直接解析 primary 表达式。
    
    输入：parser_state（pos 指向 not 表达式起始位置）
    输出：AST 节点（UNARY_OP 或 primary 节点）
    副作用：原地更新 parser_state["pos"]
    """
    current = _current_token(parser_state)
    
    # 检查当前 token 是否为 "not" 运算符
    if current is not None and current.get("type") == "KEYWORD" and current.get("value") == "not":
        # 记录 not 关键字的位置信息
        not_line = current.get("line", 0)
        not_column = current.get("column", 0)
        
        # 消耗 'not' token
        _advance(parser_state)
        
        # 递归解析 not 表达式（支持嵌套 not）
        operand = _parse_not_expr(parser_state)
        
        # 构建 UNARY_OP 节点
        return {
            "type": "UNARY_OP",
            "value": "not",
            "children": [operand],
            "line": not_line,
            "column": not_column
        }
    else:
        # 不是 not 表达式，解析 primary 表达式
        return _parse_primary(parser_state)


# === helper functions ===
# No helper functions needed for this module


# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
