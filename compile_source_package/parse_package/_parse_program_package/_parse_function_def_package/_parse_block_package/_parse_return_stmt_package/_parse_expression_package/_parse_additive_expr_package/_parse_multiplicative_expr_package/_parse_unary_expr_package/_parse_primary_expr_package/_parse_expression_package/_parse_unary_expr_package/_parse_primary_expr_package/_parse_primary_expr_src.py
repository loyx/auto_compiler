# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr

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
def _parse_primary_expr(parser_state: ParserState) -> AST:
    """解析初级表达式（标识符、字面量、括号表达式等）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    line = current_token["line"]
    column = current_token["column"]
    value = current_token["value"]
    
    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {"type": "IDENTIFIER", "value": value, "line": line, "column": column}
    
    elif token_type == "NUMBER":
        parser_state["pos"] += 1
        # 判断转换为 int 还是 float
        if "." in value or "e" in value or "E" in value:
            num_value = float(value)
        else:
            num_value = int(value)
        return {"type": "LITERAL", "value": num_value, "line": line, "column": column}
    
    elif token_type == "STRING":
        parser_state["pos"] += 1
        return {"type": "LITERAL", "value": value, "line": line, "column": column}
    
    elif token_type == "BOOL":
        parser_state["pos"] += 1
        bool_value = (value == "true")
        return {"type": "LITERAL", "value": bool_value, "line": line, "column": column}
    
    elif token_type == "LPAREN":
        parser_state["pos"] += 1  # 消费左括号
        # 解析括号内的表达式
        expr_ast = _parse_unary_expr(parser_state)
        # 检查并消费右括号
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens):
            raise SyntaxError(f"Expected ')' but found end of input at line {line}, column {column}")
        next_token = tokens[new_pos]
        if next_token["type"] != "RPAREN":
            raise SyntaxError(f"Expected ')' but found '{next_token['value']}' at line {next_token['line']}, column {next_token['column']}")
        parser_state["pos"] += 1  # 消费右括号
        return expr_ast
    
    else:
        raise SyntaxError(f"Unexpected token '{token_type}' at line {line}, column {column}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
