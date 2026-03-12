# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ..expression_package._parse_expression_src import _parse_expression

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
def _parse_assign_statement(parser_state: ParserState) -> AST:
    """解析赋值语句。输入：parser_state（pos 指向 IDENT token）。输出：ASSIGN_STMT AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 前置条件验证：必须是 IDENT token
    if pos >= len(tokens) or tokens[pos]["type"] != "IDENT":
        token = tokens[pos] if pos < len(tokens) else {"type": "EOF", "line": 0, "column": 0}
        raise SyntaxError(f"Expected identifier at {filename}:{token['line']}:{token['column']}, got {token['type']}")
    
    # 记录起始位置
    start_line = tokens[pos]["line"]
    start_column = tokens[pos]["column"]
    
    # 消费标识符
    ident_token = tokens[pos]
    parser_state["pos"] += 1
    pos = parser_state["pos"]
    
    # 消费赋值运算符（EQ 或复合赋值符）
    if pos >= len(tokens):
        raise SyntaxError(f"Expected assignment operator at {filename}:{start_line}:{start_column}")
    
    valid_operators = ("EQ", "PLUS_EQ", "MINUS_EQ", "STAR_EQ", "SLASH_EQ",
                       "PERCENT_EQ", "AMP_EQ", "PIPE_EQ", "CARET_EQ",
                       "LT_LT_EQ", "GT_GT_EQ")
    
    op_token = tokens[pos]
    if op_token["type"] not in valid_operators:
        raise SyntaxError(f"Expected assignment operator at {filename}:{op_token['line']}:{op_token['column']}, got {op_token['type']}")
    
    parser_state["pos"] += 1
    
    # 解析右侧表达式
    expr_ast = _parse_expression(parser_state)
    
    # 消费结束分号
    pos = parser_state["pos"]
    if pos >= len(tokens) or tokens[pos]["type"] != "SEMICOLON":
        raise SyntaxError(f"Expected semicolon at {filename}:{start_line}:{start_column}")
    parser_state["pos"] += 1
    
    # 构建 AST
    return {
        "type": "ASSIGN_STMT",
        "line": start_line,
        "column": start_column,
        "children": [
            {"type": "IDENT", "value": ident_token["value"], "line": ident_token["line"], "column": ident_token["column"]},
            {"type": op_token["type"], "value": op_token["value"]},
            {"type": "VALUE", "value": expr_ast}
        ]
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function
