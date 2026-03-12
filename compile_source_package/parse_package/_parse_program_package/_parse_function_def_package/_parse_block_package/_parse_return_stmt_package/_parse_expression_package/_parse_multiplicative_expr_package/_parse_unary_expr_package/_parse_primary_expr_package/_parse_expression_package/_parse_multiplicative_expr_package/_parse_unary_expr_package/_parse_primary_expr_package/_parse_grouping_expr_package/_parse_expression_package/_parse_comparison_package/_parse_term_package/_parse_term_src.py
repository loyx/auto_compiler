# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_factor_package._parse_factor_src import _parse_factor

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
#   "column": int,
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST
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
def _parse_term(parser_state: ParserState) -> AST:
    """
    解析加减类（term）表达式。
    优先级高于 factor，低于 comparison。
    """
    # 1. 解析左侧操作数
    left_ast = _parse_factor(parser_state)
    
    # 2. 循环处理 +、- 运算符
    while True:
        # 检查是否越界
        if parser_state["pos"] >= len(parser_state["tokens"]):
            break
        
        current_token = parser_state["tokens"][parser_state["pos"]]
        
        # 检查是否为加减运算符
        if current_token["value"] not in ("+", "-"):
            break
        
        # 3. 消费运算符 token，记录位置
        op_token = current_token
        parser_state["pos"] += 1
        
        # 4. 解析右侧操作数
        right_ast = _parse_factor(parser_state)
        
        # 5. 构建 BINARY AST 节点
        left_ast = {
            "type": "BINARY",
            "operator": op_token["value"],
            "left": left_ast,
            "right": right_ast,
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    # 7. 返回最终 AST
    return left_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function