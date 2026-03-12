# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

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
def _parse_factor(parser_state: ParserState) -> AST:
    """
    解析 factor 层级：factor := IDENT | NUMBER | LPAREN expression RPAREN
    输入：parser_state（pos 指向 factor 起始 token）
    输出：factor AST 节点
    副作用：更新 parser_state['pos'] 到 factor 之后的位置
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', '<unknown>')}")
    
    token = tokens[pos]
    token_type = token["type"]
    
    if token_type == "IDENT":
        parser_state["pos"] = pos + 1
        return {
            "type": "IDENT",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    elif token_type == "NUMBER":
        parser_state["pos"] = pos + 1
        return {
            "type": "NUMBER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    elif token_type == "LPAREN":
        parser_state["pos"] = pos + 1
        expr_ast = _parse_expression(parser_state)
        
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens) or tokens[new_pos]["type"] != "RPAREN":
            raise SyntaxError(
                f"Expected ')' but found {tokens[new_pos]['type'] if new_pos < len(tokens) else 'EOF'} "
                f"in {parser_state.get('filename', '<unknown>')} at line {token['line']}"
            )
        
        parser_state["pos"] = new_pos + 1
        return {
            "type": "PAREN",
            "children": [expr_ast],
            "line": token["line"],
            "column": token["column"]
        }
    
    else:
        raise SyntaxError(
            f"Unexpected token '{token_type}' at line {token['line']}, column {token['column']} "
            f"in {parser_state.get('filename', '<unknown>')}"
        )

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this parser function