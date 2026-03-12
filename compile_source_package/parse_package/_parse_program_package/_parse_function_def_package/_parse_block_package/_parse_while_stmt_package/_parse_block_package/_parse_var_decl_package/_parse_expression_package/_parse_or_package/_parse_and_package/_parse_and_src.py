# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._parse_comparison_package._parse_comparison_src import _parse_comparison
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
def _parse_and(parser_state: ParserState) -> Tuple[AST, ParserState]:
    """
    解析逻辑 AND 表达式（&&）。
    这是表达式优先级链中的中间层，位于 OR 之下、比较之上。
    支持左结合链式解析：a && b && c → 嵌套 BINARY_OP 结构。
    """
    # 1. 解析左侧操作数（比较表达式）
    left_ast, current_state = _parse_comparison(parser_state)
    
    # 2. 循环处理左结合的 AND 链
    while _is_current_token_and(current_state):
        # 记录 AND token 的位置信息
        and_token, current_state = _consume_token(current_state, "AND")
        op_line = and_token["line"]
        op_column = and_token["column"]
        
        # 3. 解析右侧操作数
        right_ast, current_state = _parse_comparison(current_state)
        
        # 4. 构建 BINARY_OP 节点
        left_ast = {
            "type": "BINARY_OP",
            "value": "&&",
            "children": [left_ast, right_ast],
            "line": op_line,
            "column": op_column
        }
    
    return left_ast, current_state


# === helper functions ===
def _is_current_token_and(parser_state: ParserState) -> bool:
    """
    检查当前位置的 token 是否为 AND 类型。
    如果已到达 token 列表末尾，返回 False。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        return False
    
    current_token = tokens[pos]
    return current_token["type"] == "AND"
