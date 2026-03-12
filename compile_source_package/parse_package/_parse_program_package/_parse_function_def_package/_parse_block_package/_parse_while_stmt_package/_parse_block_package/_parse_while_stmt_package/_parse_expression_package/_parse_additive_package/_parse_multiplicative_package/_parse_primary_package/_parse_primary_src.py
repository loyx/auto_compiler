# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._peek_token_package._peek_token_src import _peek_token
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_additive_package._parse_additive_src import _parse_additive

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
def _parse_primary(parser_state: ParserState) -> Tuple[AST, ParserState]:
    """
    解析基本表达式（primary expression）。
    处理 NUMBER、IDENTIFIER、LPAREN 等 token 类型。
    返回 (AST 节点，更新后的 parser_state)。
    """
    current_token = _peek_token(parser_state)
    
    if current_token is None:
        raise SyntaxError(
            f"Unexpected end of input in {parser_state.get('filename', 'unknown')}"
        )
    
    token_type = current_token.get("type")
    
    if token_type == "NUMBER":
        token, parser_state = _consume_token(parser_state, "NUMBER")
        ast_node = {
            "type": "NUMBER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
        return ast_node, parser_state
    
    elif token_type == "IDENTIFIER":
        token, parser_state = _consume_token(parser_state, "IDENTIFIER")
        ast_node = {
            "type": "IDENTIFIER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
        return ast_node, parser_state
    
    elif token_type == "LPAREN":
        # 消费左括号
        _consume_token(parser_state, "LPAREN")
        
        # 递归解析括号内表达式
        ast_node, parser_state = _parse_additive(parser_state)
        
        # 期望并消费右括号
        closing_token = _peek_token(parser_state)
        if closing_token is None or closing_token.get("type") != "RPAREN":
            raise SyntaxError(
                f"Expected ')' at line {closing_token.get('line', '?')}, "
                f"column {closing_token.get('column', '?')} "
                f"in {parser_state.get('filename', 'unknown')}"
            )
        _consume_token(parser_state, "RPAREN")
        
        return ast_node, parser_state
    
    else:
        raise SyntaxError(
            f"Expected NUMBER, IDENTIFIER, or '(' at line {current_token.get('line', '?')}, "
            f"column {current_token.get('column', '?')} "
            f"in {parser_state.get('filename', 'unknown')}. "
            f"Got '{token_type}' instead."
        )

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for this parser function node
