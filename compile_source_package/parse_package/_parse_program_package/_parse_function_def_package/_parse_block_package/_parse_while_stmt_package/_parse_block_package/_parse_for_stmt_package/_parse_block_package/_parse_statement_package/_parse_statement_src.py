# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_for_statement_package._parse_for_statement_src import _parse_for_statement
from ._parse_while_statement_package._parse_while_statement_src import _parse_while_statement
from ._parse_if_statement_package._parse_if_statement_src import _parse_if_statement
from ._parse_return_statement_package._parse_return_statement_src import _parse_return_statement
from ._parse_break_statement_package._parse_break_statement_src import _parse_break_statement
from ._parse_continue_statement_package._parse_continue_statement_src import _parse_continue_statement
from ._parse_pass_statement_package._parse_pass_statement_src import _parse_pass_statement
from ._parse_assign_statement_package._parse_assign_statement_src import _parse_assign_statement
from ._parse_import_statement_package._parse_import_statement_src import _parse_import_statement
from ._parse_def_statement_package._parse_def_statement_src import _parse_def_statement
from ._parse_class_statement_package._parse_class_statement_src import _parse_class_statement
from ._parse_expression_statement_package._parse_expression_statement_src import _parse_expression_statement

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
def _parse_statement(parser_state: ParserState) -> AST:
    """
    语句解析分发器。根据当前 token 类型分发到具体语句解析函数。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 跳过前导分号（空语句）
    while pos < len(tokens) and tokens[pos]["type"] == "SEMICOLON":
        parser_state["pos"] += 1
        pos = parser_state["pos"]
    
    # 检查是否到达文件末尾
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of file at {filename}")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # 分发到具体解析器
    if token_type == "FOR":
        return _parse_for_statement(parser_state)
    elif token_type == "WHILE":
        return _parse_while_statement(parser_state)
    elif token_type == "IF":
        return _parse_if_statement(parser_state)
    elif token_type == "RETURN":
        return _parse_return_statement(parser_state)
    elif token_type == "BREAK":
        return _parse_break_statement(parser_state)
    elif token_type == "CONTINUE":
        return _parse_continue_statement(parser_state)
    elif token_type == "PASS":
        return _parse_pass_statement(parser_state)
    elif token_type == "IMPORT":
        return _parse_import_statement(parser_state)
    elif token_type == "DEF":
        return _parse_def_statement(parser_state)
    elif token_type == "CLASS":
        return _parse_class_statement(parser_state)
    elif token_type == "IDENT":
        return _parse_assign_statement(parser_state)
    else:
        # 其他情况作为表达式语句处理
        return _parse_expression_statement(parser_state)

# === helper functions ===
# No helper functions needed - all logic delegated to child functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a parser function node