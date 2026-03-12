# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_expression_package._parse_expression_src import _parse_expression

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
#   "error": str | None
# }

# === main function ===
def _parse_assignment(parser_state: ParserState) -> AST:
    """
    解析 ASSIGNMENT 语句并返回 ASSIGNMENT AST 节点。
    
    输入：parser_state 当前指向 IDENTIFIER token（赋值目标）
    输出：{"type": "ASSIGNMENT", "target": str, "value": AST, "line": int, "column": int}
    """
    # 消费 IDENTIFIER token 获取 target 变量名
    id_token = _consume_token(parser_state, "IDENTIFIER")
    
    # 消费 ASSIGN token ('=')
    _consume_token(parser_state, "ASSIGN")
    
    # 解析表达式作为 value
    value_ast = _parse_expression(parser_state)
    
    # 构建并返回 ASSIGNMENT AST 节点
    return {
        "type": "ASSIGNMENT",
        "target": id_token["value"],
        "value": value_ast,
        "line": id_token["line"],
        "column": id_token["column"]
    }

# === helper functions ===
# No helper functions needed; all logic delegated to subfunctions.

# === OOP compatibility layer ===
# Not required for this function node.
