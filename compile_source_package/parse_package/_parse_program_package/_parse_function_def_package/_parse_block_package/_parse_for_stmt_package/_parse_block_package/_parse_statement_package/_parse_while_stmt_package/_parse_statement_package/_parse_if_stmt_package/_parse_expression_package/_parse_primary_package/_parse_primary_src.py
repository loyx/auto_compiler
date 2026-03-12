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
def _parse_primary(parser_state: ParserState) -> AST:
    """
    解析主表达式（primary expression）。
    支持：一元 !、括号 (...)、标识符、整数字面量、字符串字面量。
    原地更新 parser_state["pos"]。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: 意外的文件结尾，期望主表达式")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    token_line = token["line"]
    token_column = token["column"]
    
    # 1. 一元运算符 !
    if token_type == "BANG":
        parser_state["pos"] += 1
        operand_ast = _parse_primary(parser_state)
        return {
            "type": "UNOP",
            "children": [operand_ast],
            "value": "!",
            "line": token_line,
            "column": token_column
        }
    
    # 2. 括号表达式 (...)
    if token_type == "LPAREN":
        parser_state["pos"] += 1
        expr_ast = _parse_expression(parser_state)
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(f"{filename}:{token_line}:{token_column}: 未匹配的左括号")
        rparen_token = tokens[parser_state["pos"]]
        if rparen_token["type"] != "RPAREN":
            raise SyntaxError(f"{filename}:{rparen_token['line']}:{rparen_token['column']}: 期望 ')'，得到 '{rparen_token['value']}'")
        parser_state["pos"] += 1
        return expr_ast
    
    # 3. 标识符 IDENT
    if token_type == "IDENT":
        parser_state["pos"] += 1
        return {
            "type": "IDENT",
            "value": token_value,
            "line": token_line,
            "column": token_column
        }
    
    # 4. 整数字面量 INT
    if token_type == "INT":
        parser_state["pos"] += 1
        return {
            "type": "INT_LITERAL",
            "value": token_value,
            "line": token_line,
            "column": token_column
        }
    
    # 5. 字符串字面量 STRING
    if token_type == "STRING":
        parser_state["pos"] += 1
        return {
            "type": "STRING_LITERAL",
            "value": token_value,
            "line": token_line,
            "column": token_column
        }
    
    # 未知 token 类型
    raise SyntaxError(f"{filename}:{token_line}:{token_column}: 意外的 token '{token_value}'，期望主表达式")


# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# Not needed for parser function nodes
