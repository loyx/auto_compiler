# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_logical_and_package._parse_logical_and_src import _parse_logical_and

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
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "name": str,
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
def _parse_logical_or(parser_state: ParserState) -> AST:
    """
    解析逻辑或表达式（|| 运算符）。
    这是最低优先级的二元运算符。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. 解析左侧操作数（更高优先级的 && 表达式）
    left_ast = _parse_logical_and(parser_state)
    
    # 2. 循环处理 || 运算符
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        if current_token.get("value") == "||" and current_token.get("type") == "OPERATOR":
            # 3. 消耗 || token
            op_token = current_token
            parser_state["pos"] += 1
            
            # 4. 解析右侧操作数
            right_ast = _parse_logical_and(parser_state)
            
            # 5. 构建 BINARY_OP 节点
            left_ast = {
                "type": "BINARY_OP",
                "operator": "||",
                "left": left_ast,
                "right": right_ast,
                "line": op_token.get("line", 0),
                "column": op_token.get("column", 0)
            }
        else:
            break
    
    return left_ast

# === helper functions ===
def _check_current_token(parser_state: ParserState, expected_value: str) -> bool:
    """检查当前 token 是否为期望值。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        return False
    return tokens[pos].get("value") == expected_value

# === OOP compatibility layer ===
