# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _parse_unary_expr(parser_state: ParserState) -> AST:
    """Parse unary expression (supports unary +/- operators, parenthesized expressions, primary expressions).
    
    Resource IO:
    - Reads parser_state['tokens'], parser_state['pos']
    - Writes parser_state['pos'], parser_state['error']
    """
    tokens = parser_state['tokens']
    pos = parser_state['pos']
    
    # Check if we're at the end of tokens
    if pos >= len(tokens):
        parser_state['error'] = "Unexpected end of input in unary expression"
        return _create_error_node(-1, -1)
    
    current_token = tokens[pos]
    
    # Check for unary operators (PLUS, MINUS)
    if current_token['type'] in ('PLUS', 'MINUS'):
        op_token = current_token
        parser_state['pos'] += 1  # consume operator token
        
        # Recursively parse the operand as unary expression
        operand = _parse_unary_expr(parser_state)
        
        # Check if operand parsing failed
        if parser_state.get('error'):
            return operand
        
        return {
            "type": "UNARY_OP",
            "children": [operand],
            "value": op_token['value'],
            "line": op_token['line'],
            "column": op_token['column']
        }
    else:
        # Not a unary operator, parse as primary expression
        return _parse_primary_expr(parser_state)

# === helper functions ===
def _create_error_node(line: int, column: int) -> AST:
    """Create an error AST node."""
    return {
        "type": "ERROR",
        "children": [],
        "value": None,
        "line": line,
        "column": column
    }

# === OOP compatibility layer ===
# Not required for this parser function node
