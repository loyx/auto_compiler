# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr

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
#   "value": Any,
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
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
def _parse_unary_expr(parser_state: ParserState) -> AST:
    """
    解析一元操作符表达式（如负号、正号）。
    输入 parser_state 字典，当前位置指向表达式起始 token。
    返回 AST 节点字典。若解析失败则抛出 SyntaxError。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否越界
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing unary expression")
    
    current_token = tokens[pos]
    
    # 检查当前 token 是否为一元操作符
    if current_token.get("type") == "OPERATOR" and current_token.get("value") in ("-", "+"):
        op = current_token["value"]
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        
        # 消费该 token
        parser_state["pos"] = pos + 1
        
        # 递归解析后续的一元操作符（支持连续一元操作符如 --x）
        operand = _parse_unary_expr(parser_state)
        
        # 构建 UNARY_OP 节点
        return {
            "type": "UNARY_OP",
            "operator": op,
            "operand": operand,
            "line": line,
            "column": column
        }
    else:
        # 不是一元操作符，解析主表达式（下一优先级）
        return _parse_primary_expr(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
