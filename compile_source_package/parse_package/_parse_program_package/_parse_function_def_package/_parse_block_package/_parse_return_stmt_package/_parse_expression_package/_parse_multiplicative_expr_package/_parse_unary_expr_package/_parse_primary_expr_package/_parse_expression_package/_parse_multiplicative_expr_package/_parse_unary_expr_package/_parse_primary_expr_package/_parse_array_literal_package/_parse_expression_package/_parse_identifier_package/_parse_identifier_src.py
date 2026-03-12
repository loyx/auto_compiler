# === std / third-party imports ===
from typing import Any, Dict, List

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
def _parse_identifier(parser_state: ParserState) -> AST:
    """解析标识符或函数调用。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 边界检查
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return {"type": "Error", "value": "Unexpected EOF", "line": 0, "column": 0, "children": []}
    
    current_token = tokens[pos]
    identifier_name = current_token["value"]
    line = current_token["line"]
    column = current_token["column"]
    
    # 消耗 IDENTIFIER token
    parser_state["pos"] = pos + 1
    
    # 检查下一个 token 是否为 LEFT_PAREN
    next_pos = parser_state["pos"]
    if next_pos < len(tokens) and tokens[next_pos]["type"] == "LEFT_PAREN":
        # 解析函数调用
        return _parse_function_call(parser_state, identifier_name, line, column)
    else:
        # 解析简单标识符
        return {"type": "Identifier", "value": identifier_name, "line": line, "column": column, "children": []}

# === helper functions ===
def _parse_function_call(parser_state: ParserState, func_name: str, line: int, column: int) -> AST:
    """解析函数调用表达式。"""
    tokens = parser_state["tokens"]
    
    # 消耗 LEFT_PAREN token
    parser_state["pos"] += 1
    
    args: List[AST] = []
    
    # 检查是否为空参数列表
    if parser_state["pos"] < len(tokens):
        current = tokens[parser_state["pos"]]
        if current["type"] != "RIGHT_PAREN":
            # 解析参数列表
            while True:
                arg = _parse_expression(parser_state)
                args.append(arg)
                
                # 检查下一个 token
                if parser_state["pos"] >= len(tokens):
                    parser_state["error"] = "Unexpected end of input in function call"
                    break
                
                next_token = tokens[parser_state["pos"]]
                if next_token["type"] == "COMMA":
                    # 消耗 COMMA，继续解析下一个参数
                    parser_state["pos"] += 1
                elif next_token["type"] == "RIGHT_PAREN":
                    # 参数列表结束
                    break
                else:
                    parser_state["error"] = f"Expected COMMA or RIGHT_PAREN, got {next_token['type']}"
                    break
    
    # 消耗 RIGHT_PAREN token
    if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] == "RIGHT_PAREN":
        parser_state["pos"] += 1
    else:
        parser_state["error"] = "Expected RIGHT_PAREN in function call"
    
    return {
        "type": "CallExpression",
        "value": func_name,
        "line": line,
        "column": column,
        "children": args
    }

# === OOP compatibility layer ===