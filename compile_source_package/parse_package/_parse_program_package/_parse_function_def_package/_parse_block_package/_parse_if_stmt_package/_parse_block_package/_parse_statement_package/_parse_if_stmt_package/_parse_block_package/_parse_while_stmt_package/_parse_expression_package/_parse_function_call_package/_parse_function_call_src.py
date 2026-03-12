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
def _parse_function_call(parser_state: dict, func_ast: dict) -> dict:
    """解析函数调用语法：primary '(' [arguments] ')'"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. 验证并消耗 LPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "LPAREN":
        raise SyntaxError(f"Expected '(' after function name")
    pos += 1
    
    # 2. 初始化参数列表
    args = []
    
    # 3. 如果有参数，解析它们
    if pos < len(tokens) and tokens[pos]["type"] != "RPAREN":
        while True:
            # 解析参数表达式
            arg_ast = _parse_expression(parser_state)
            args.append(arg_ast)
            
            pos = parser_state["pos"]
            if pos >= len(tokens):
                raise SyntaxError("Unexpected end of input, expected ')' or ','")
            
            # 检查是 COMMA 还是 RPAREN
            if tokens[pos]["type"] == "COMMA":
                pos += 1
                parser_state["pos"] = pos
                if pos >= len(tokens):
                    raise SyntaxError("Unexpected end of input after ','")
            elif tokens[pos]["type"] == "RPAREN":
                break
            else:
                raise SyntaxError(f"Expected ',' or ')', got {tokens[pos]['type']}")
    
    # 4. 验证并消耗 RPAREN
    pos = parser_state["pos"]
    if pos >= len(tokens) or tokens[pos]["type"] != "RPAREN":
        raise SyntaxError("Expected ')' to close function call")
    pos += 1
    parser_state["pos"] = pos
    
    # 5. 构建并返回函数调用 AST
    return {
        "type": "function_call",
        "func": func_ast,
        "args": args,
        "line": func_ast.get("line", 0),
        "column": func_ast.get("column", 0)
    }

# === helper functions ===

# === OOP compatibility layer ===
