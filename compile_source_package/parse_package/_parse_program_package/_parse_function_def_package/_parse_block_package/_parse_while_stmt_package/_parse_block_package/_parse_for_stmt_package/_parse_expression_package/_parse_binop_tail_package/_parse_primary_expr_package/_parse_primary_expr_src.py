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
#   "operator": str,
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
    """解析主表达式（原子表达式），包括数字、字符串、标识符、括号表达式等。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否越界
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input while parsing primary expression"
        return {"type": "ERROR", "value": None, "line": 0, "column": 0}
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    token_line = token.get("line", 0)
    token_column = token.get("column", 0)
    
    # 根据 token type 分类处理
    if token_type == "NUMBER":
        parser_state["pos"] += 1
        return {"type": "NUM_LITERAL", "value": token_value, "line": token_line, "column": token_column}
    
    elif token_type == "STRING":
        parser_state["pos"] += 1
        return {"type": "STR_LITERAL", "value": token_value, "line": token_line, "column": token_column}
    
    elif token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {"type": "IDENTIFIER", "value": token_value, "line": token_line, "column": token_column}
    
    elif token_type == "TRUE":
        parser_state["pos"] += 1
        return {"type": "BOOL_LITERAL", "value": True, "line": token_line, "column": token_column}
    
    elif token_type == "FALSE":
        parser_state["pos"] += 1
        return {"type": "BOOL_LITERAL", "value": False, "line": token_line, "column": token_column}
    
    elif token_type == "NONE":
        parser_state["pos"] += 1
        return {"type": "NONE_LITERAL", "value": None, "line": token_line, "column": token_column}
    
    elif token_type == "LPAREN":
        # 消耗 LPAREN
        parser_state["pos"] += 1
        
        # 解析内部表达式
        inner_expr = _parse_expression(parser_state)
        
        # 检查是否有错误
        if parser_state.get("error"):
            return inner_expr
        
        # 检查并消耗 RPAREN
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens):
            parser_state["error"] = "Unexpected end of input, expected ')'"
            return {"type": "ERROR", "value": None, "line": token_line, "column": token_column}
        
        next_token = tokens[new_pos]
        if next_token["type"] != "RPAREN":
            parser_state["error"] = f"Expected ')' but got '{next_token['type']}'"
            return {"type": "ERROR", "value": None, "line": next_token.get("line", 0), "column": next_token.get("column", 0)}
        
        parser_state["pos"] += 1
        return inner_expr
    
    else:
        # 无法识别的 token
        parser_state["error"] = f"Unexpected token '{token_type}' while parsing primary expression"
        return {"type": "ERROR", "value": None, "line": token_line, "column": token_column}

# === helper functions ===

# === OOP compatibility layer ===
