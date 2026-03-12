# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary

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
def _parse_multiplicative(parser_state: ParserState) -> AST:
    """
    解析乘除表达式。处理 *、/、% 运算符，左右操作数调用 _parse_unary。
    输入 parser_state，输出 AST 节点，原地更新 pos。错误时抛出 SyntaxError。
    """
    # Step 1: Parse left operand using _parse_unary
    left = _parse_unary(parser_state)
    
    # Step 2: Loop while encountering multiplicative operators
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    while pos < len(tokens):
        token = tokens[pos]
        if token["type"] != "OPERATOR" or token["value"] not in ("*", "/", "%"):
            break
        
        # Record operator position
        op_line = token["line"]
        op_column = token["column"]
        op_value = token["value"]
        
        # Advance pos
        parser_state["pos"] = pos + 1
        pos = parser_state["pos"]
        
        # Parse right operand
        right = _parse_unary(parser_state)
        
        # Build BINARY_OP node
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": op_value,
            "line": op_line,
            "column": op_column
        }
        
        # Update pos for next iteration
        pos = parser_state["pos"]
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node
