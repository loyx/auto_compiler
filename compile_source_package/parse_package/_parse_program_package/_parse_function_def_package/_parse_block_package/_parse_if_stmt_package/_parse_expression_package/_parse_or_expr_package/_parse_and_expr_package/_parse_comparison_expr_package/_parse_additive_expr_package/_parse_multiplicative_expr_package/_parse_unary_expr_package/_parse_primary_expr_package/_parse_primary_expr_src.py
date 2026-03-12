# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions to import at module level
# _parse_unary_expr is imported inside the function to avoid circular import

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
#   "value": Any,
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
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
def _parse_primary_expr(parser_state: ParserState) -> AST:
    """
    解析主表达式（数字字面量、标识符、括号表达式等最低优先级表达式）。
    
    输入 parser_state 字典，当前位置指向表达式起始 token。
    返回 AST 节点字典。若解析失败则抛出 SyntaxError。
    """
    # 在函数内部 import，避免模块级循环依赖
    from .._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr
    
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input in primary expression")
    
    current_token = tokens[pos]
    token_type = current_token.get("type")
    line = current_token.get("line", 0)
    column = current_token.get("column", 0)
    
    if token_type == "NUMBER":
        # 消费 NUMBER token
        parser_state["pos"] += 1
        return {
            "type": "NUMBER",
            "value": current_token["value"],
            "line": line,
            "column": column
        }
    
    elif token_type == "IDENTIFIER":
        # 消费 IDENTIFIER token
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "value": current_token["value"],
            "line": line,
            "column": column
        }
    
    elif token_type == "LPAREN":
        # 消费 '(' token
        parser_state["pos"] += 1
        
        # 递归调用一元表达式解析括号内内容
        expr = _parse_unary_expr(parser_state)
        
        # 期待 ')'
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens):
            raise SyntaxError("Missing closing parenthesis")
        
        closing_token = tokens[new_pos]
        if closing_token.get("type") != "RPAREN":
            raise SyntaxError("Missing closing parenthesis")
        
        # 消费 ')' token
        parser_state["pos"] += 1
        
        return expr
    
    else:
        raise SyntaxError(
            f"Unexpected token '{current_token.get('value', '')}' "
            f"at line {line}, column {column} in primary expression"
        )

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
