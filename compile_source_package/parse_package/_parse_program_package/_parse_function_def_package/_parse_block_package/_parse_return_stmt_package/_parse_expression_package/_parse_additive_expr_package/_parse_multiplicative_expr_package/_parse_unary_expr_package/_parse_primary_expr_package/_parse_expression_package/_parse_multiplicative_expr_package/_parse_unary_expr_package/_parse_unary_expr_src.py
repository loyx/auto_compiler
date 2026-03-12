# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this parsing logic

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
#   "operator": str,         # 运算符 (仅 BINARY_OP/UNARY_OP)
#   "left": AST,             # 左操作数 (仅 BINARY_OP)
#   "right": AST,            # 右操作数 (仅 BINARY_OP)
#   "operand": AST,          # 操作数 (仅 UNARY_OP)
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
    """解析一元表达式（最高优先级的操作数）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing unary expression")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    token_line = current_token["line"]
    token_column = current_token["column"]
    
    # Check for unary operators
    unary_op_map = {
        "PLUS": "+",
        "MINUS": "-",
        "NOT": "not",
        "TILDE": "~"
    }
    
    if token_type in unary_op_map:
        operator = unary_op_map[token_type]
        # Consume the operator token
        parser_state["pos"] += 1
        # Recursively parse the operand
        operand = _parse_unary_expr(parser_state)
        return {
            "type": "UNARY_OP",
            "operator": operator,
            "operand": operand,
            "line": token_line,
            "column": token_column
        }
    
    # Check for parenthesized expression
    elif token_type == "LPAREN":
        parser_state["pos"] += 1  # Consume LPAREN
        # Parse the inner expression (use binary expr for full precedence)
        inner_expr = _parse_binary_expr(parser_state)
        # Expect RPAREN
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError("Missing closing parenthesis")
        closing_token = tokens[parser_state["pos"]]
        if closing_token["type"] != "RPAREN":
            raise SyntaxError(f"Expected RPAREN, got {closing_token['type']}")
        parser_state["pos"] += 1  # Consume RPAREN
        return inner_expr
    
    # Check for identifier
    elif token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "value": current_token["value"],
            "line": token_line,
            "column": token_column
        }
    
    # Check for literal
    elif token_type == "LITERAL":
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "value": current_token["value"],
            "line": token_line,
            "column": token_column
        }
    
    else:
        raise SyntaxError(f"Unexpected token '{token_type}' at line {token_line}, column {token_column}")

# === helper functions ===
def _parse_binary_expr(parser_state: ParserState) -> AST:
    """
    解析二元表达式（用于括号内的完整表达式）。
    此函数为简化版本，实际应由专门的 binary expression parser 处理。
    这里作为占位实现，递归调用 _parse_unary_expr 作为基础。
    """
    # For now, delegate to unary expr (simplified implementation)
    # A full binary expression parser would handle operator precedence
    return _parse_unary_expr(parser_state)

# === OOP compatibility layer ===
# Not needed for this parser function
