# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_array_literal_package._parse_array_literal_src import _parse_array_literal
from ._parse_object_literal_package._parse_object_literal_src import _parse_object_literal
from ._parse_literal_package._parse_literal_src import _parse_literal
from ._parse_identifier_package._parse_identifier_src import _parse_identifier
from ._parse_grouped_expression_package._parse_grouped_expression_src import _parse_grouped_expression

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
def _parse_expression(parser_state: ParserState) -> AST:
    """
    解析通用表达式。这是表达式解析的入口函数，
    负责识别并分发到具体的表达式类型解析器。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 边界检查：pos 越界
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', 'unknown')}")
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    
    # 根据 token 类型分发到相应的解析器
    if token_type == "LEFT_BRACKET":
        return _parse_array_literal(parser_state)
    elif token_type == "LEFT_BRACE":
        return _parse_object_literal(parser_state)
    elif token_type in ("STRING", "NUMBER", "BOOLEAN", "NULL"):
        return _parse_literal(parser_state)
    elif token_type == "IDENTIFIER":
        return _parse_identifier(parser_state)
    elif token_type == "LEFT_PAREN":
        return _parse_grouped_expression(parser_state)
    else:
        raise SyntaxError(
            f"Unexpected token '{token_type}' at line {current_token.get('line', '?')}, "
            f"column {current_token.get('column', '?')} in {parser_state.get('filename', 'unknown')}"
        )

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for parser internal function