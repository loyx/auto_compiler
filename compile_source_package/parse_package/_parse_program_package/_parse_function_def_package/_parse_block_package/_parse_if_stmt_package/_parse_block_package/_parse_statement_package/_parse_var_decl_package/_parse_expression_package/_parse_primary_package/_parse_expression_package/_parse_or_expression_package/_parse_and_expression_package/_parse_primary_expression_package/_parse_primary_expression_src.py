# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_or_expression_package._parse_or_expression_src import _parse_or_expression

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
#   "column": int,
#   "operator": str,
#   "left": AST,
#   "right": AST
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
def _parse_primary_expression(parser_state: ParserState) -> AST:
    """解析 primary 表达式（最高优先级）。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 检查是否越界
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return {"type": "error", "value": "Unexpected end of input", "line": 0, "column": 0}
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    token_value = current_token.get("value", "")
    token_line = current_token.get("line", 0)
    token_column = current_token.get("column", 0)
    
    if token_type == "IDENT":
        _consume_token(parser_state, "IDENT")
        return {"type": "identifier", "value": token_value, "line": token_line, "column": token_column}
    
    elif token_type == "STRING":
        _consume_token(parser_state, "STRING")
        return {"type": "string_literal", "value": token_value, "line": token_line, "column": token_column}
    
    elif token_type == "NUMBER":
        _consume_token(parser_state, "NUMBER")
        # 优先尝试 int，若包含小数点或转换失败则使用 float
        if "." in token_value:
            ast_value = float(token_value)
        else:
            try:
                ast_value = int(token_value)
            except ValueError:
                ast_value = float(token_value)
        return {"type": "number_literal", "value": ast_value, "line": token_line, "column": token_column}
    
    elif token_type == "TRUE":
        _consume_token(parser_state, "TRUE")
        return {"type": "boolean_literal", "value": True, "line": token_line, "column": token_column}
    
    elif token_type == "FALSE":
        _consume_token(parser_state, "FALSE")
        return {"type": "boolean_literal", "value": False, "line": token_line, "column": token_column}
    
    elif token_type == "LPAREN":
        _consume_token(parser_state, "LPAREN")
        # 解析括号内的表达式
        inner_ast = _parse_or_expression(parser_state)
        
        # 检查是否有错误
        if parser_state.get("error"):
            return inner_ast
        
        # 必须消费 RPAREN
        if parser_state.get("pos", 0) >= len(tokens):
            parser_state["error"] = f"Expected ')' at end of input"
            return {"type": "error", "value": parser_state["error"], "line": token_line, "column": token_column}
        
        next_token = tokens[parser_state.get("pos", 0)]
        if next_token.get("type") != "RPAREN":
            rp_line = next_token.get("line", 0)
            rp_column = next_token.get("column", 0)
            rp_type = next_token.get("type", "UNKNOWN")
            parser_state["error"] = f"Expected ')' at line {rp_line}, column {rp_column}, found {rp_type}"
            return {"type": "error", "value": parser_state["error"], "line": rp_line, "column": rp_column}
        
        _consume_token(parser_state, "RPAREN")
        return inner_ast
    
    elif token_type == "EOF":
        parser_state["error"] = "Unexpected end of input"
        return {"type": "error", "value": "Unexpected end of input", "line": token_line, "column": token_column}
    
    else:
        parser_state["error"] = f"Unexpected token: {token_type}"
        return {"type": "error", "value": parser_state["error"], "line": token_line, "column": token_column}


# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
