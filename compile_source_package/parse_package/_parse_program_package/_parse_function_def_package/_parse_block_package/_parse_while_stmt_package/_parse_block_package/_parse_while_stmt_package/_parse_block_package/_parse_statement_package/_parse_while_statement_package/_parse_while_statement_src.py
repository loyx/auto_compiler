# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block

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
def _parse_while_statement(parser_state: ParserState) -> AST:
    """
    解析 WHILE 语句。
    预期语法：WHILE LPAREN expression RPAREN block
    输入时 WHILE token 已被消费，pos 指向 LPAREN。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 记录 WHILE 关键字的位置
    while_line = tokens[pos - 1]["line"] if pos > 0 else 0
    while_column = tokens[pos - 1]["column"] if pos > 0 else 0
    
    # 1. 消费 LPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "LPAREN":
        parser_state["error"] = "Expected LPAREN after WHILE"
        return _error_ast(while_line, while_column)
    pos += 1
    
    # 2. 解析条件表达式
    parser_state["pos"] = pos
    condition = _parse_expression(parser_state)
    pos = parser_state["pos"]
    
    if parser_state.get("error"):
        return condition
    
    # 3. 消费 RPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "RPAREN":
        parser_state["error"] = "Expected RPAREN after condition"
        return _error_ast(while_line, while_column)
    pos += 1
    
    # 4. 解析循环体
    parser_state["pos"] = pos
    body = _parse_block(parser_state)
    
    if parser_state.get("error"):
        return body
    
    # 5. 返回 WHILE_STATEMENT AST
    return {
        "type": "WHILE_STATEMENT",
        "condition": condition,
        "body": body,
        "line": while_line,
        "column": while_column
    }

# === helper functions ===
def _error_ast(line: int, column: int) -> AST:
    """生成错误 AST 节点。"""
    return {
        "type": "ERROR",
        "line": line,
        "column": column
    }

# === OOP compatibility layer ===