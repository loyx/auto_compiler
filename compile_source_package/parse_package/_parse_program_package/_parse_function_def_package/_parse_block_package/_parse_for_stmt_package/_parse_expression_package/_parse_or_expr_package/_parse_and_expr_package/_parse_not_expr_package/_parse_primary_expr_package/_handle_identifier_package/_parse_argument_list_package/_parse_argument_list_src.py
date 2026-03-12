# === std / third-party imports ===
from typing import Any, Dict, List

# === ADT defines ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


# === main function ===
def _parse_argument_list(parser_state: dict) -> list:
    """
    解析函数调用的参数列表。
    输入：parser_state（pos 指向 LPAREN 之后的第一个 token）。
    输出：参数 AST 列表。
    会更新 parser_state['pos'] 越过 RPAREN。
    """
    arguments = []
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 空参数列表：直接遇到 RPAREN
    if pos >= len(tokens):
        parser_state["error"] = "unexpected end of input in argument list"
        return arguments
    
    current_token = tokens[pos]
    
    # 如果第一个 token 就是 RPAREN，说明是空参数列表
    if current_token["type"] == "RPAREN":
        parser_state["pos"] += 1
        return arguments
    
    # 解析参数列表
    while pos < len(tokens):
        current_token = tokens[pos]
        
        # 遇到 RPAREN，结束参数列表
        if current_token["type"] == "RPAREN":
            parser_state["pos"] += 1
            break
        
        # 解析表达式作为参数
        from .._parse_expression_package._parse_expression_src import _parse_expression
        arg = _parse_expression(parser_state)
        
        if parser_state.get("error"):
            return arguments
        
        arguments.append(arg)
        
        # 检查下一个 token
        pos = parser_state["pos"]
        if pos >= len(tokens):
            parser_state["error"] = "unexpected end of input in argument list"
            break
        
        next_token = tokens[pos]
        
        # 如果是逗号，继续解析下一个参数
        if next_token["type"] == "COMMA":
            parser_state["pos"] += 1
            pos = parser_state["pos"]
        # 如果不是逗号也不是 RPAREN，可能是错误
        elif next_token["type"] != "RPAREN":
            parser_state["error"] = f"expected ',' or ')' but got {next_token['type']}"
            break
    
    return arguments


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this parser function node.
