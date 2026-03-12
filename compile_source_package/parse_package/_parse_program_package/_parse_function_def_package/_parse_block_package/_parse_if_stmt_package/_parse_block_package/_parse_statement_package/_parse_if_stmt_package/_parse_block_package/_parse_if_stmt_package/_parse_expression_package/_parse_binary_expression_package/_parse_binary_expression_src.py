# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

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
def _parse_binary_expression(parser_state: dict, min_precedence: int) -> dict:
    """
    使用优先级爬升算法解析二元表达式。
    输入：parser_state（pos 指向左操作数起始）、min_precedence（最小优先级阈值）。
    输出：AST 节点。
    副作用：更新 parser_state["pos"] 到表达式结束位置。
    异常：语法错误时抛出 SyntaxError。
    """
    # Step 1: Parse left operand
    left = _parse_primary(parser_state)
    
    # Step 2: Loop to handle binary operators
    while True:
        tokens = parser_state["tokens"]
        pos = parser_state["pos"]
        
        # Check if we have more tokens
        if pos >= len(tokens):
            break
        
        current_token = tokens[pos]
        op_type = current_token.get("type")
        
        # Get operator precedence
        prec = _get_operator_precedence(op_type)
        if prec is None or prec < min_precedence:
            break
        
        # Step 3: Consume operator token
        op_line = current_token.get("line", 0)
        op_column = current_token.get("column", 0)
        parser_state["pos"] += 1
        
        # Step 4: Determine right precedence (handle right-associativity for POW)
        if op_type == "POW":
            next_prec = prec  # Right-associative
        else:
            next_prec = prec + 1  # Left-associative
        
        # Step 5: Parse right operand
        right = _parse_binary_expression(parser_state, next_prec)
        
        # Step 6: Build BINOP AST node
        left = {
            "type": "BINOP",
            "op": op_type,
            "left": left,
            "right": right,
            "line": op_line,
            "column": op_column
        }
    
    return left

# === helper functions ===
def _get_operator_precedence(op_type: str) -> int:
    """
    获取运算符优先级。返回优先级值（1-7），非运算符返回 None。
    优先级从低到高：OR(1), AND(2), EQ/NEQ(3), LT/LE/GT/GE(4), PLUS/MINUS(5), MUL/DIV/MOD(6), POW(7)
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
        "POW": 7
    }
    return precedence_map.get(op_type)

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function
