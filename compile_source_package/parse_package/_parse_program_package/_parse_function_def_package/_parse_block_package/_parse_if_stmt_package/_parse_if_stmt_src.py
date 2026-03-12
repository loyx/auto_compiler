# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _parse_if_stmt(parser_state: dict) -> dict:
    """解析 if 语句，包括 if/elif/else 结构。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. 消费 IF token
    if pos >= len(tokens) or tokens[pos]["type"] != "IF":
        raise SyntaxError(f"Expected IF token at position {pos}")
    
    if_token = tokens[pos]
    pos += 1
    
    # 2. 解析条件表达式
    condition_node = _parse_expression(parser_state)
    
    # 3. 解析 if 主体块
    body_node = _parse_block(parser_state)
    
    # 构建 IF_STMT 节点
    if_node = {
        "type": "IF_STMT",
        "children": [condition_node, body_node],
        "line": if_token["line"],
        "column": if_token["column"]
    }
    
    # 4. 解析 elif 子句（多个）
    while parser_state["pos"] < len(tokens):
        if tokens[parser_state["pos"]]["type"] == "ELIF":
            elif_token = tokens[parser_state["pos"]]
            parser_state["pos"] += 1
            
            # 解析 elif 条件
            elif_condition = _parse_expression(parser_state)
            # 解析 elif 主体
            elif_body = _parse_block(parser_state)
            
            elif_node = {
                "type": "ELIF_STMT",
                "children": [elif_condition, elif_body],
                "line": elif_token["line"],
                "column": elif_token["column"]
            }
            if_node["children"].append(elif_node)
        else:
            break
    
    # 5. 解析 else 子句（可选）
    if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] == "ELSE":
        else_token = tokens[parser_state["pos"]]
        parser_state["pos"] += 1
        
        # 解析 else 主体
        else_body = _parse_block(parser_state)
        
        else_node = {
            "type": "ELSE_STMT",
            "children": [else_body],
            "line": else_token["line"],
            "column": else_token["column"]
        }
        if_node["children"].append(else_node)
    
    return if_node

# === helper functions ===
# No helper functions needed - logic is delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for this function node