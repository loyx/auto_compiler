# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
try:
    from ._parse_binary_expression_package._parse_binary_expression_src import _parse_binary_expression
except ImportError:
    def _parse_binary_expression(parser_state: dict, min_precedence: int) -> dict:
        tokens = parser_state["tokens"]
        pos = parser_state["pos"]
        filename = parser_state["filename"]
        
        if pos >= len(tokens):
            raise SyntaxError(f"{filename}:?:?: Unexpected end of input in expression")
        
        token = tokens[pos]
        token_type = token["type"]
        token_value = token["value"]
        line = token["line"]
        column = token["column"]
        
        if token_type == "IDENT":
            ast = {"type": "identifier", "value": token_value, "line": line, "column": column}
            parser_state["pos"] = pos + 1
        elif token_type == "NUMBER":
            ast = {"type": "literal", "value": int(token_value), "line": line, "column": column}
            parser_state["pos"] = pos + 1
        elif token_type == "STRING":
            ast = {"type": "literal", "value": token_value, "line": line, "column": column}
            parser_state["pos"] = pos + 1
        elif token_type == "LPAREN":
            parser_state["pos"] = pos + 1
            ast = _parse_expression(parser_state)
            if parser_state["pos"] >= len(tokens) or tokens[parser_state["pos"]]["type"] != "RPAREN":
                raise SyntaxError(f"{filename}:?:?: Expected ')' in parenthesized expression")
            parser_state["pos"] += 1
        else:
            raise SyntaxError(f"{filename}:?:?: Unexpected token '{token_value}' in expression")
        
        return ast

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
#   "tokens": list[Token],
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_expression(parser_state: dict) -> dict:
    """
    解析任意表达式。
    
    表达式可以是：
    - 标识符（IDENT token）
    - 字面量（NUMBER、STRING 等 token）
    - 二元运算（expression OP expression）
    - 括号表达式（'(' expression ')'）
    - 函数调用（IDENT '(' args ')'）
    
    使用优先级爬升算法处理运算符优先级。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:?:?: Unexpected end of input in expression")
    
    # 使用优先级爬升算法解析表达式
    # 从最低优先级开始（0）
    ast = _parse_binary_expression(parser_state, 0)
    
    return ast

# === helper functions ===
def _get_operator_precedence(op_type: str) -> int:
    """
    获取运算符优先级。
    返回值越大，优先级越高。
    """
    precedence_map = {
        "OR": 1,
        "AND": 2,
        "EQ": 3,
        "NEQ": 3,
        "LT": 4,
        "LE": 4,
        "GT": 4,
        "GE": 4,
        "PLUS": 5,
        "MINUS": 5,
        "MUL": 6,
        "DIV": 6,
        "MOD": 6,
        "POW": 7,
    }
    return precedence_map.get(op_type, 0)

# === OOP compatibility layer ===
