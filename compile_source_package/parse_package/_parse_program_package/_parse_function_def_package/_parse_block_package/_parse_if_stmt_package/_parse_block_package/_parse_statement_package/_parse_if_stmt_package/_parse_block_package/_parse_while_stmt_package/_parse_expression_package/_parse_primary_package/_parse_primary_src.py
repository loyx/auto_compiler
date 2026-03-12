# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
from ._parse_paren_expression_package._parse_paren_expression_src import _parse_paren_expression

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
#   "error": Optional[str]
# }

# === main function ===
def _parse_primary(parser_state: ParserState) -> Optional[AST]:
    """
    解析基本表达式单元（primary expression）。
    
    支持：标识符、整数字面量、浮点数字面量、字符串字面量、
         括号表达式、布尔字面量、None 字面量。
    
    输入：parser_state（pos 指向当前 token）
    输出：AST 节点或 None（如果不是 primary）
    副作用：成功解析时修改 parser_state["pos"] 到 primary 结束位置
    异常：语法错误时抛出 SyntaxError
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        return None
    
    token = tokens[pos]
    token_type = token.get("type", "")
    token_value = token.get("value", "")
    line = token.get("line", 0)
    column = token.get("column", 0)
    
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {"type": "identifier", "value": token_value, "line": line, "column": column}
    elif token_type == "INTEGER":
        parser_state["pos"] = pos + 1
        return {"type": "integer", "value": int(token_value), "line": line, "column": column}
    elif token_type == "FLOAT":
        parser_state["pos"] = pos + 1
        return {"type": "float", "value": float(token_value), "line": line, "column": column}
    elif token_type == "STRING":
        parser_state["pos"] = pos + 1
        if len(token_value) >= 2 and ((token_value[0] == '"' and token_value[-1] == '"') or (token_value[0] == "'" and token_value[-1] == "'")):
            token_value = token_value[1:-1]
        return {"type": "string", "value": token_value, "line": line, "column": column}
    elif token_type == "TRUE":
        parser_state["pos"] = pos + 1
        return {"type": "boolean", "value": True, "line": line, "column": column}
    elif token_type == "FALSE":
        parser_state["pos"] = pos + 1
        return {"type": "boolean", "value": False, "line": line, "column": column}
    elif token_type == "NONE":
        parser_state["pos"] = pos + 1
        return {"type": "none", "value": None, "line": line, "column": column}
    elif token_type == "LPAREN":
        return _parse_paren_expression(parser_state, token)
    else:
        return None

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this parser function
