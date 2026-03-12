# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._current_token_package._current_token_src import _current_token
from ._consume_package._consume_src import _consume

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
#   "name": str,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str
# }


# === main function ===
def _parse_primary(parser_state: ParserState) -> AST:
    """解析基础表达式单元：标识符、字面量、括号表达式、函数调用。"""
    token = _current_token(parser_state)
    
    if token is None:
        raise SyntaxError(f"Unexpected end of file at {parser_state.get('filename', '<unknown>')}")
    
    # 标识符（可能是函数调用）
    if token["type"] == "IDENT":
        _consume(parser_state, "IDENT")
        next_token = _current_token(parser_state)
        if next_token and next_token["type"] == "LPAREN":
            return _parse_function_call(parser_state, token["value"], token["line"], token["column"])
        else:
            return {"type": "IDENT", "value": token["value"], "line": token["line"], "column": token["column"]}
    
    # 字面量
    elif token["type"] in ("NUMBER", "STRING"):
        _consume(parser_state)
        return {"type": token["type"], "value": token["value"], "line": token["line"], "column": token["column"]}
    
    # 括号表达式
    elif token["type"] == "LPAREN":
        _consume(parser_state, "LPAREN")
        expr = _parse_expression(parser_state)
        _consume(parser_state, "RPAREN")
        return expr
    
    else:
        raise SyntaxError(f"Unexpected token {token['type']} at {parser_state.get('filename', '<unknown>')}:{token['line']}:{token['column']}")


# === helper functions ===
def _parse_function_call(parser_state: ParserState, name: str, line: int, column: int) -> AST:
    """解析函数调用：消耗 LPAREN、参数列表、RPAREN。"""
    _consume(parser_state, "LPAREN")
    args = []
    
    next_token = _current_token(parser_state)
    if next_token and next_token["type"] != "RPAREN":
        args.append(_parse_expression(parser_state))
        while True:
            next_token = _current_token(parser_state)
            if not next_token:
                raise SyntaxError(f"Unexpected end of file at {parser_state.get('filename', '<unknown>')}")
            if next_token["type"] == "RPAREN":
                break
            elif next_token["type"] == "COMMA":
                _consume(parser_state, "COMMA")
                args.append(_parse_expression(parser_state))
            else:
                raise SyntaxError(f"Expected COMMA or RPAREN but got {next_token['type']} at {parser_state.get('filename', '<unknown>')}:{next_token['line']}:{next_token['column']}")
    
    _consume(parser_state, "RPAREN")
    return {"type": "CALL", "name": name, "children": args, "line": line, "column": column}


# === OOP compatibility layer ===
