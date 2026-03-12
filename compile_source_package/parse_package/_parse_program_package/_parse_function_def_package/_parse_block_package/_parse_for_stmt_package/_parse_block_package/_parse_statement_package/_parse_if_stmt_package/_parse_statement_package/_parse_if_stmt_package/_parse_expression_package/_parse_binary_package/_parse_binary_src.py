# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary
from ._get_precedence_package._get_precedence_src import _get_precedence

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
#   "type": str,             # BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL 等
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
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
def _parse_binary(parser_state: ParserState, min_precedence: int) -> AST:
    """
    解析二元表达式（带优先级处理）。
    使用 Pratt Parsing 算法解析二元运算符。
    """
    # 步骤 1: 解析左侧操作数
    left = _parse_unary(parser_state)
    
    # 步骤 2: 循环检查后续 token 是否为二元运算符
    tokens = parser_state["tokens"]
    
    while parser_state["pos"] < len(tokens):
        token = tokens[parser_state["pos"]]
        token_type = token["type"]
        
        # 获取当前运算符优先级
        precedence = _get_precedence(token_type)
        
        # 步骤 3: 如果运算符优先级 < min_precedence，停止解析
        if precedence < min_precedence:
            break
        
        # 检查是否为二元运算符（优先级 > 0 表示是运算符）
        if precedence == 0:
            break
        
        # 消耗运算符 token
        op_token = token
        parser_state["pos"] += 1
        
        # 步骤 4: 解析右侧操作数
        # 对于左结合运算符，右侧使用 precedence + 1；右结合使用 precedence
        # 这里简化处理，统一使用 precedence + 1（左结合）
        right = _parse_binary(parser_state, precedence + 1)
        
        # 构建 BINARY_OP AST 节点
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": op_token["value"],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    # 步骤 5: 返回最终的 AST 节点
    return left

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
