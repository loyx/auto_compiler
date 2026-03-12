# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

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
def _parse_primary_expr(parser_state: ParserState) -> AST:
    """解析主表达式（标识符、字面量、括号表达式等）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查边界
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing primary expression")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # 标识符
    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "value": current_token["value"],
            "line": current_token["line"],
            "column": current_token["column"]
        }
    
    # 字面量
    elif token_type in ("NUMBER", "STRING", "BOOLEAN", "NULL"):
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "value": current_token["value"],
            "line": current_token["line"],
            "column": current_token["column"]
        }
    
    # 括号表达式
    elif token_type == "LEFT_PAREN":
        parser_state["pos"] += 1  # 消费左括号
        expr = _parse_expression(parser_state)  # 解析内部表达式
        
        # 检查右括号
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError("Missing closing parenthesis")
        
        right_paren = tokens[parser_state["pos"]]
        if right_paren["type"] != "RIGHT_PAREN":
            raise SyntaxError(
                f"Missing closing parenthesis at line {right_paren['line']}, column {right_paren['column']}"
            )
        
        parser_state["pos"] += 1  # 消费右括号
        return expr
    
    # 未知 token
    else:
        raise SyntaxError(
            f"Unexpected token '{token_type}' at line {current_token['line']}, column {current_token['column']}"
        )

# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
