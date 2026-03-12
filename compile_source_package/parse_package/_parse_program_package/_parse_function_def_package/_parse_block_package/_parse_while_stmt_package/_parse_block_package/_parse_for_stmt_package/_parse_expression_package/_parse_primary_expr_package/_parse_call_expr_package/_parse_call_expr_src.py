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
def _parse_call_expr(parser_state: ParserState, func_name_token: Token) -> AST:
    """解析函数调用表达式：IDENTIFIER LPAREN arg1, arg2, ... RPAREN"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 消费 LPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "LPAREN":
        parser_state["error"] = "Expected '(' after function name"
        return {
            "type": "ERROR",
            "value": "Expected '('",
            "line": func_name_token["line"],
            "column": func_name_token["column"],
            "children": []
        }
    pos += 1
    
    args = []
    
    # 检查是否为空参数列表
    if pos < len(tokens) and tokens[pos]["type"] == "RPAREN":
        # 空参数列表 ()
        pos += 1
    else:
        # 解析参数列表
        while True:
            if pos >= len(tokens):
                parser_state["error"] = "Unexpected end of input in function call"
                return {
                    "type": "ERROR",
                    "value": "Unexpected EOF",
                    "line": func_name_token["line"],
                    "column": func_name_token["column"],
                    "children": args
                }
            
            # 解析参数表达式
            arg_ast = _parse_expression(parser_state)
            if parser_state["error"]:
                return arg_ast
            
            args.append(arg_ast)
            pos = parser_state["pos"]
            
            if pos >= len(tokens):
                parser_state["error"] = "Unexpected end of input, expected ')' or ','"
                return {
                    "type": "ERROR",
                    "value": "Unexpected EOF",
                    "line": func_name_token["line"],
                    "column": func_name_token["column"],
                    "children": args
                }
            
            next_token = tokens[pos]
            
            if next_token["type"] == "RPAREN":
                pos += 1
                break
            elif next_token["type"] == "COMMA":
                pos += 1
                # 继续循环解析下一个参数
            else:
                parser_state["error"] = f"Expected ')' or ',' but got '{next_token['value']}'"
                return {
                    "type": "ERROR",
                    "value": "Syntax error in function call",
                    "line": next_token["line"],
                    "column": next_token["column"],
                    "children": args
                }
    
    parser_state["pos"] = pos
    
    return {
        "type": "CALL",
        "value": func_name_token["value"],
        "line": func_name_token["line"],
        "column": func_name_token["column"],
        "children": args
    }

# === helper functions ===

# === OOP compatibility layer ===
