# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions for this helper utility

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
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
def _consume_token(parser_state: ParserState, expected_type: str) -> ParserState:
    """
    消费期望类型的 token。
    
    验证当前 token 类型是否匹配 expected_type，如果匹配则 pos + 1。
    如果不匹配或已到达末尾，raise SyntaxError。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    filename = parser_state.get("filename", "unknown")
    
    # 检查是否到达 token 末尾
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: 期望 '{expected_type}'，但遇到 'EOF'")
    
    current_token = tokens[pos]
    actual_type = current_token.get("type", "UNKNOWN")
    
    # 验证 token 类型是否匹配
    if actual_type != expected_type:
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        raise SyntaxError(f"{filename}:{line}:{column}: 期望 '{expected_type}'，但遇到 '{actual_type}'")
    
    # 原地修改 pos + 1
    parser_state["pos"] = pos + 1
    
    return parser_state

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
