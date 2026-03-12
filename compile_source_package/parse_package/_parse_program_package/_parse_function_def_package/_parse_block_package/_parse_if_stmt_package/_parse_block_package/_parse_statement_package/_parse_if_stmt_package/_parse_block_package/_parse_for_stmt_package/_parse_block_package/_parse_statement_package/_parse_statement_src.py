# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_block_package._parse_block_src import _parse_block
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_if_statement_package._parse_if_statement_src import _parse_if_statement
from ._parse_while_statement_package._parse_while_statement_src import _parse_while_statement
from ._parse_for_statement_package._parse_for_statement_src import _parse_for_statement
from ._parse_return_statement_package._parse_return_statement_src import _parse_return_statement
from ._parse_var_declaration_package._parse_var_declaration_src import _parse_var_declaration

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
    解析单个语句。根据当前 token 类型分发到相应的专用解析函数。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # 根据 token 类型分发到相应的解析函数
    if token_type == "LBRACE":
        return _parse_block(parser_state)
    elif token_type == "IF":
        return _parse_if_statement(parser_state)
    elif token_type == "WHILE":
        return _parse_while_statement(parser_state)
    elif token_type == "FOR":
        return _parse_for_statement(parser_state)
    elif token_type == "RETURN":
        return _parse_return_statement(parser_state)
    elif token_type in ("VAR", "LET", "CONST"):
        return _parse_var_declaration(parser_state)
    else:
        # 默认作为表达式语句处理
        return _parse_expression(parser_state)

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
