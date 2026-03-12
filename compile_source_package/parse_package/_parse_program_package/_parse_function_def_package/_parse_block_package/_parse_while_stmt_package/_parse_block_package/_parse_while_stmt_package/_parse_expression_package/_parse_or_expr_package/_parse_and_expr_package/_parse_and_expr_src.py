# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._peek_token_package._peek_token_src import _peek_token
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_comparison_package._parse_comparison_src import _parse_comparison

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
def _parse_and_expr(parser_state: ParserState) -> Tuple[AST, ParserState]:
    """
    解析 'and' 表达式链（比 'or' 高一级优先级，比 comparison 低一级）。
    
    输入：parser_state 字典，包含 tokens、pos、filename、error
    输出：(AST 节点, 更新后的 parser_state)
    处理：循环解析 and 表达式，构建 BINARY_OP 节点
    """
    # 首先解析左侧 comparison 表达式
    left_ast, parser_state = _parse_comparison(parser_state)
    
    # 循环检查是否有 "AND" token
    while True:
        current_token = _peek_token(parser_state)
        
        # 检查当前 token 是否为 AND
        if current_token is None or current_token.get("type") != "AND":
            break
        
        # 记录 AND token 的位置信息
        and_line = current_token.get("line", 0)
        and_column = current_token.get("column", 0)
        
        # 消费 AND token
        parser_state = _consume_token(parser_state)
        
        # 解析右侧 comparison 表达式
        right_ast, parser_state = _parse_comparison(parser_state)
        
        # 构建 BINARY_OP AST 节点
        left_ast = {
            "type": "BINARY_OP",
            "operator": "and",
            "children": [left_ast, right_ast],
            "value": None,
            "line": and_line,
            "column": and_column
        }
    
    return (left_ast, parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
