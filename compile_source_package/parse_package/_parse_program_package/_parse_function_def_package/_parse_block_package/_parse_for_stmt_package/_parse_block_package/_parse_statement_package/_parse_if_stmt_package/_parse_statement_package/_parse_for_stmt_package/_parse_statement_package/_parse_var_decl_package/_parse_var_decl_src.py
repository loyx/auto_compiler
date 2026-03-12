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
#   "value": str,
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
def _parse_var_decl(parser_state: ParserState) -> AST:
    """
    解析变量声明语句（VAR/LET/CONST）。
    语法：var/let/const identifier [= initializer] ;
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Step 1: Consume VAR/LET/CONST keyword
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected variable declaration keyword")
    
    keyword_token = tokens[pos]
    if keyword_token["type"] not in ("VAR", "LET", "CONST"):
        raise SyntaxError(f"Expected VAR/LET/CONST, got {keyword_token['type']}")
    
    keyword_value = keyword_token["value"]
    keyword_line = keyword_token["line"]
    keyword_column = keyword_token["column"]
    pos += 1
    
    # Step 2: Expect and consume identifier
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected identifier")
    
    ident_token = tokens[pos]
    if ident_token["type"] != "IDENT":
        raise SyntaxError(f"Expected identifier, got {ident_token['type']}")
    
    var_name = ident_token["value"]
    pos += 1
    
    # Step 3: Check for initializer (= expression)
    children = []
    if pos < len(tokens) and tokens[pos]["type"] == "ASSIGN":
        pos += 1  # consume '='
        initializer_ast = _parse_expression(parser_state)
        children.append(initializer_ast)
        pos = parser_state["pos"]  # update pos after expression parsing
    
    # Step 4: Expect and consume semicolon
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected ';'")
    
    semicolon_token = tokens[pos]
    if semicolon_token["type"] != "SEMI":
        raise SyntaxError(f"Expected ';', got {semicolon_token['type']}")
    
    pos += 1
    
    # Update parser state
    parser_state["pos"] = pos
    
    # Build and return AST node
    return {
        "type": "VAR_DECL",
        "children": children,
        "value": var_name,
        "line": keyword_line,
        "column": keyword_column,
        "keyword": keyword_value
    }

# === helper functions ===
def _expect_token(parser_state: ParserState, token_type: str) -> Token:
    """
    期望当前 token 为指定类型，若是则消耗并返回，否则抛出异常。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input, expected {token_type}")
    
    token = tokens[pos]
    if token["type"] != token_type:
        raise SyntaxError(f"Expected {token_type}, got {token['type']}")
    
    parser_state["pos"] = pos + 1
    return token

# === OOP compatibility layer ===
