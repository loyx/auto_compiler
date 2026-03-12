# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_equality_package._parse_equality_src import _parse_equality
from ._current_token_package._current_token_src import _current_token
from ._consume_package._consume_src import _consume

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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, CALL, BLOCK)
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
    解析逻辑与表达式（&& 运算符）。
    语法：equality ('&&' equality)*
    返回左结合的 BINARY_OP 树或单个操作数节点。
    """
    # 解析左侧操作数
    left = _parse_equality(parser_state)
    
    # 循环处理 && 运算符
    while True:
        token = _current_token(parser_state)
        if token is None or token.get("type") != "OPERATOR" or token.get("value") != "&&":
            break
        
        # 消耗 && 运算符
        _consume(parser_state, "OPERATOR", "&&")
        
        # 解析右侧操作数
        right = _parse_equality(parser_state)
        
        # 构建 BINARY_OP 节点（左结合）
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": "&&",
            "line": token.get("line", left.get("line")),
            "column": token.get("column", left.get("column"))
        }
    
    return left

# === helper functions ===
# No additional helpers needed; all logic is in main function

# === OOP compatibility layer ===
# Not needed for parser internal function
