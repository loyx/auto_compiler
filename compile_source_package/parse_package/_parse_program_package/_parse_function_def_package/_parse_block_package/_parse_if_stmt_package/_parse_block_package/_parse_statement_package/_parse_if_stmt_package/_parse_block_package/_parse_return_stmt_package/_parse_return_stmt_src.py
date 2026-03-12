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
def _parse_return_stmt(parser_state: ParserState) -> AST:
    """
    解析 return 语句。
    语法：RETURN [expression] SEMICOLON
    返回：RETURN AST 节点
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 记录 RETURN token 的位置
    return_token = tokens[pos]
    line = return_token["line"]
    column = return_token["column"]
    
    # 消费 RETURN token
    parser_state["pos"] += 1
    pos = parser_state["pos"]
    
    # 检查下一个 token
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{line}:{column}: unexpected end of file, expected ';' or expression")
    
    next_token = tokens[pos]
    
    # 解析返回值或分号
    if next_token["type"] == "SEMICOLON":
        # return; 没有返回值
        value_ast = None
        parser_state["pos"] += 1
    else:
        # 解析表达式
        value_ast = _parse_expression(parser_state)
        
        # 消费 SEMICOLON
        pos = parser_state["pos"]
        if pos >= len(tokens) or tokens[pos]["type"] != "SEMICOLON":
            raise SyntaxError(f"{filename}:{line}:{column}: expected ';' after return expression")
        parser_state["pos"] += 1
    
    # 构建 RETURN AST 节点
    return {
        "type": "RETURN",
        "value": value_ast,
        "line": line,
        "column": column
    }

# === helper functions ===

# === OOP compatibility layer ===
