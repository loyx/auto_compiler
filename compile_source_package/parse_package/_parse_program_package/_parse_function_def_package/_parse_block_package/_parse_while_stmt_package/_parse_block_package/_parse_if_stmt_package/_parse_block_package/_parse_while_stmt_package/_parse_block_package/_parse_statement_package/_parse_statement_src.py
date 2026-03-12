# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
from ._parse_break_stmt_package._parse_break_stmt_src import _parse_break_stmt
from ._parse_continue_stmt_package._parse_continue_stmt_src import _parse_continue_stmt
from ._parse_assignment_package._parse_assignment_src import _parse_assignment
from ._parse_expression_stmt_package._parse_expression_stmt_src import _parse_expression_stmt

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_statement(parser_state: ParserState) -> AST:
    """
    解析单条语句并分发到具体语句解析器。
    根据当前 token 类型调用相应的语句解析函数。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return {"type": "error", "value": "Unexpected end of input"}
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # 根据 token 类型分发到相应的语句解析器
    if token_type == "IF":
        return _parse_if_stmt(parser_state)
    elif token_type == "WHILE":
        return _parse_while_stmt(parser_state)
    elif token_type == "FOR":
        return _parse_for_stmt(parser_state)
    elif token_type == "RETURN":
        return _parse_return_stmt(parser_state)
    elif token_type == "BREAK":
        return _parse_break_stmt(parser_state)
    elif token_type == "CONTINUE":
        return _parse_continue_stmt(parser_state)
    elif token_type == "IDENT":
        # 可能是赋值语句或表达式语句
        return _parse_assignment(parser_state)
    else:
        # 其他情况尝试作为表达式语句解析
        return _parse_expression_stmt(parser_state)

# === helper functions ===
# No helper functions needed - all logic delegated to child functions

# === OOP compatibility layer ===
# Not needed for this parser function node
