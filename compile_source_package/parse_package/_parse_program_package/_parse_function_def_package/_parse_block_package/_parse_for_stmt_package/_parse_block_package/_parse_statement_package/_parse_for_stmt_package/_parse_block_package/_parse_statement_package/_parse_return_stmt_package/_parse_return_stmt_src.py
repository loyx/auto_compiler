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
def _parse_return_stmt(parser_state: dict) -> dict:
    """
    解析 return 语句，语法：return [expression];
    
    返回 RETURN_STMT AST 节点，原地更新 parser_state["pos"]。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 获取 RETURN token 的位置信息
    return_token = tokens[pos]
    line = return_token.get("line", 0)
    column = return_token.get("column", 0)
    
    # 1. 消耗 RETURN token
    pos += 1
    
    # 2. 检查下一个 token 是否为 SEMICOLON 或语句结束
    if pos >= len(tokens):
        # 语句结束，无返回值
        parser_state["pos"] = pos
        return {
            "type": "RETURN_STMT",
            "value": None,
            "line": line,
            "column": column
        }
    
    next_token = tokens[pos]
    
    # 3. 如果是 SEMICOLON，直接消耗并返回无值的 return 语句
    if next_token.get("type") == "SEMICOLON":
        pos += 1
        parser_state["pos"] = pos
        return {
            "type": "RETURN_STMT",
            "value": None,
            "line": line,
            "column": column
        }
    
    # 4. 否则解析返回值表达式
    try:
        expr_ast = _parse_expression(parser_state)
    except SyntaxError as e:
        raise SyntaxError(f"{filename}:{line}:{column}: {str(e)}")
    
    # 5. 检查并消耗 SEMICOLON
    pos = parser_state["pos"]
    if pos < len(tokens) and tokens[pos].get("type") == "SEMICOLON":
        pos += 1
        parser_state["pos"] = pos
    # 注意：如果没有 SEMICOLON，也允许（某些语言风格）
    
    return {
        "type": "RETURN_STMT",
        "value": expr_ast,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node
