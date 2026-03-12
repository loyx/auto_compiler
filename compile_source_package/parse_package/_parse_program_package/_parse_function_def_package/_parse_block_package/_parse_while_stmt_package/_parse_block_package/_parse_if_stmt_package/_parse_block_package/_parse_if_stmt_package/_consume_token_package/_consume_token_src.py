# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this utility function

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
def _consume_token(parser_state: ParserState, expected_type: str = None) -> Token:
    """
    消费当前 token 并推进解析器位置。
    
    检查当前 token 类型是否匹配 expected_type，不匹配则抛出 SyntaxError。
    返回被消费的 token 字典，原地修改 parser_state['pos']。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否越界
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    # 获取当前 token
    current_token = tokens[pos]
    
    # 检查类型匹配
    if expected_type is not None and current_token["type"] != expected_type:
        raise SyntaxError(f"Expected '{expected_type}', got {current_token['type']}")
    
    # 原地修改 pos
    parser_state["pos"] += 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function