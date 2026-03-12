# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._build_error_node_package._build_error_node_src import _build_error_node
from ._parse_argument_list_package._parse_argument_list_src import _parse_argument_list

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (大写字符串)
#   "value": str,            # token 值 (原始字符串)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (IDENTIFIER, LITERAL, CALL, ERROR, etc.)
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
def _handle_identifier(parser_state: dict, token: dict) -> dict:
    """
    Handle IDENTIFIER token: determine if it's a variable reference or function call.
    Mutates parser_state["pos"] directly.
    Returns: IDENTIFIER node, CALL node, or ERROR node.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Build IDENTIFIER node (used for both variable and function call)
    identifier_node = {
        "type": "IDENTIFIER",
        "value": token["value"],
        "line": token["line"],
        "column": token["column"]
    }
    
    # Consume the IDENTIFIER token
    parser_state["pos"] += 1
    
    # Check if next token is LPAREN (function call)
    if parser_state["pos"] < len(tokens):
        next_token = tokens[parser_state["pos"]]
        if next_token["type"] == "LPAREN":
            # This is a function call
            # Consume LPAREN
            parser_state["pos"] += 1
            
            # Parse argument list
            arguments = _parse_argument_list(parser_state)
            
            # Check if parser encountered an error
            if parser_state.get("error"):
                return _build_error_node(
                    parser_state,
                    "函数调用参数解析失败",
                    token["line"],
                    token["column"]
                )
            
            # Build CALL node
            return {
                "type": "CALL",
                "function": identifier_node,
                "arguments": arguments,
                "line": token["line"],
                "column": token["column"]
            }
    
    # Not a function call, return IDENTIFIER node
    return identifier_node

# === helper functions ===
# No helper functions needed; all logic is in main function.

# === OOP compatibility layer ===
# Not needed for this parser function node.
