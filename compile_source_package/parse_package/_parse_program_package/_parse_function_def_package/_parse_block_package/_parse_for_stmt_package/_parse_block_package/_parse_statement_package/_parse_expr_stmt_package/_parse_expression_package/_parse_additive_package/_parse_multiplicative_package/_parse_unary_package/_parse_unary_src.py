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
def _parse_unary(parser_state: ParserState) -> AST:
    """解析一元表达式（前缀运算符、括号、原子值）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否还有 token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    token = tokens[pos]
    token_type = token["type"]
    
    # 1. 处理前缀运算符
    if token_type in ("OP_POS", "OP_NEG", "OP_NOT"):
        op_token = token
        parser_state["pos"] += 1  # 消费运算符
        operand = _parse_unary(parser_state)  # 递归解析操作数
        return {
            "type": "UNARY_OP",
            "children": [operand],
            "value": op_token["value"],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    # 2. 处理括号表达式
    if token_type == "LPAREN":
        parser_state["pos"] += 1  # 消费左括号
        expr_ast = _parse_expression(parser_state)  # 解析括号内表达式
        
        # 检查并消费右括号
        pos = parser_state["pos"]
        if pos >= len(tokens) or tokens[pos]["type"] != "RPAREN":
            raise SyntaxError("Expected ')'")
        parser_state["pos"] += 1  # 消费右括号
        
        return expr_ast
    
    # 3. 处理原子值
    return _parse_atom(parser_state)

# === helper functions ===
def _parse_atom(parser_state: ParserState) -> AST:
    """解析原子值（NUMBER、STRING、IDENT、BOOL、NULL）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    token = tokens[pos]
    token_type = token["type"]
    
    # 原子值类型集合
    atom_types = {"NUMBER", "STRING", "IDENT", "BOOL", "NULL"}
    
    if token_type not in atom_types:
        raise SyntaxError(f"Unexpected token: {token_type}")
    
    # 消费原子值 token
    parser_state["pos"] += 1
    
    return {
        "type": token_type,
        "children": [],
        "value": token["value"],
        "line": token["line"],
        "column": token["column"]
    }

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node.
