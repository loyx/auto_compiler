# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

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
def _parse_unary(parser_state: ParserState) -> AST:
    """
    解析一元表达式（如负号、正号、逻辑非等）。
    优先级高于乘除法运算符，右结合。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否还有 token
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input while parsing unary expression"
        return {"type": "ERROR", "value": None, "line": -1, "column": -1}
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    
    # 一元运算符集合
    unary_operators = {"MINUS", "PLUS", "NOT", "BITWISE_NOT"}
    
    if token_type in unary_operators:
        # 记录运算符并前进
        operator = current_token.get("value", "")
        line = current_token.get("line", -1)
        column = current_token.get("column", -1)
        
        parser_state["pos"] = pos + 1
        
        # 递归解析后续表达式（右结合）
        operand = _parse_unary(parser_state)
        
        # 检查是否有错误
        if parser_state.get("error"):
            return operand
        
        # 构建 UNARY_OP 节点
        return {
            "type": "UNARY_OP",
            "operator": operator,
            "children": [operand],
            "line": line,
            "column": column
        }
    else:
        # 不是一元运算符，调用更低优先级解析函数
        return _parse_primary(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this parser function node