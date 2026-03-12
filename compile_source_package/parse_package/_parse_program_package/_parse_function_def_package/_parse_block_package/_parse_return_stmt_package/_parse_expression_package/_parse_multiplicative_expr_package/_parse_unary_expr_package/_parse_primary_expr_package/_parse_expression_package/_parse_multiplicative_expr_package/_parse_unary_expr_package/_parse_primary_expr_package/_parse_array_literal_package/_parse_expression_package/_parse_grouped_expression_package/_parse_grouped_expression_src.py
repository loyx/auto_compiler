# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ..._parse_expression_package._parse_expression_src import _parse_expression

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
def _parse_grouped_expression(parser_state: ParserState) -> AST:
    """
    解析括号表达式 (...)。
    
    入口假设：parser_state["pos"] 已指向 LEFT_PAREN token
    出口保证：消费完 RIGHT_PAREN 后返回，pos 指向下一个待处理 token
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 边界检查：确保当前位置有效
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing grouped expression")
    
    left_paren_token = tokens[pos]
    line = left_paren_token["line"]
    column = left_paren_token["column"]
    
    # 步骤 1: 消耗 LEFT_PAREN token
    parser_state["pos"] += 1
    
    # 步骤 2: 检查空括号情况
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError("Empty parentheses are not allowed")
    
    current_token = tokens[parser_state["pos"]]
    if current_token["type"] == "RIGHT_PAREN":
        raise SyntaxError("Empty parentheses are not allowed")
    
    # 步骤 3: 解析括号内的表达式（递归调用 _parse_expression）
    inner_ast = _parse_expression(parser_state)
    
    # 步骤 4: 检查并消耗 RIGHT_PAREN
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"Expected ')' but found end of input at line {line}, column {column}")
    
    current_token = tokens[parser_state["pos"]]
    if current_token["type"] != "RIGHT_PAREN":
        raise SyntaxError(f"Expected ')' but found '{current_token['type']}' at line {current_token['line']}, column {current_token['column']}")
    
    # 消耗 RIGHT_PAREN
    parser_state["pos"] += 1
    
    # 步骤 5: 返回包装后的 AST 节点
    return {
        "type": "GROUPED_EXPRESSION",
        "children": [inner_ast],
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed for this simple parsing logic

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function