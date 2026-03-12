# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_relational_package._parse_relational_src import _parse_relational
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
def _parse_equality(parser_state: ParserState) -> AST:
    """
    解析相等性表达式（== 和 != 运算符）。
    语法：relational (('==' | '!=') relational)*
    返回左结合的 BINARY_OP 树或单个操作数节点。
    """
    # 1. 解析左侧操作数（关系表达式）
    left_node = _parse_relational(parser_state)
    
    # 2. 循环处理 == 和 != 运算符
    while True:
        token = _current_token(parser_state)
        if token is None:
            break
        
        if token["type"] not in ("EQ", "NE"):
            break
        
        # 3. 消耗运算符
        op_token = _consume(parser_state, token["type"])
        
        # 4. 解析右侧操作数
        right_node = _parse_relational(parser_state)
        
        # 5. 构建 BINARY_OP 节点（左结合）
        left_node = {
            "type": "BINARY_OP",
            "children": [left_node, right_node],
            "value": op_token["value"],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left_node

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for parser function nodes