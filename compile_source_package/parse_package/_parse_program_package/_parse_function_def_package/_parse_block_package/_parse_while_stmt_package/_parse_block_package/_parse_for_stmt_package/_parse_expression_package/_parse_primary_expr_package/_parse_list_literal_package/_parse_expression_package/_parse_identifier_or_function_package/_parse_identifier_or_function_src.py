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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_identifier_or_function(parser_state: ParserState) -> AST:
    """解析标识符（变量）或函数调用。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    
    # 检查是否越界
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return {"type": "ERROR", "value": "Unexpected end of input", "line": 0, "column": 0, "children": []}
    
    token = tokens[pos]
    
    # 验证当前 token 是 IDENTIFIER
    if token["type"] != "IDENTIFIER":
        parser_state["error"] = f"Expected IDENTIFIER, got {token['type']}"
        return {"type": "ERROR", "value": f"Expected IDENTIFIER", "line": token["line"], "column": token["column"], "children": []}
    
    identifier_name = token["value"]
    identifier_line = token["line"]
    identifier_column = token["column"]
    
    # 移动到标识符之后
    parser_state["pos"] = pos + 1
    
    # 检查下一个 token 是否为 '('
    if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] == "LPAREN":
        # 函数调用
        parser_state["pos"] += 1  # 跳过 '('
        
        # 解析参数列表
        args = []
        if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] != "RPAREN":
            # 解析第一个参数
            args.append(_parse_expression(parser_state))
            
            # 解析剩余参数（逗号分隔）
            while (parser_state["pos"] < len(tokens) and 
                   tokens[parser_state["pos"]]["type"] == "COMMA"):
                parser_state["pos"] += 1  # 跳过逗号
                args.append(_parse_expression(parser_state))
        
        # 期望 ')'
        if parser_state["pos"] >= len(tokens) or tokens[parser_state["pos"]]["type"] != "RPAREN":
            parser_state["error"] = "Expected ')'"
            return {"type": "ERROR", "value": "Expected ')'", "line": identifier_line, "column": identifier_column, "children": []}
        
        parser_state["pos"] += 1  # 跳过 ')'
        
        return {
            "type": "FUNCTION_CALL",
            "value": identifier_name,
            "line": identifier_line,
            "column": identifier_column,
            "children": args
        }
    else:
        # 变量引用
        return {
            "type": "VARIABLE",
            "value": identifier_name,
            "line": identifier_line,
            "column": identifier_column,
            "children": []
        }

# === helper functions ===

# === OOP compatibility layer ===
