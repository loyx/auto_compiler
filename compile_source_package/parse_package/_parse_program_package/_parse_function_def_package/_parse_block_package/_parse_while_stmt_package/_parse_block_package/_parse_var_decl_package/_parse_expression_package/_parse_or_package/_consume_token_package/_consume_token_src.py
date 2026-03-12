# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions for this utility

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
def _consume_token(parser_state: ParserState, token_type: str) -> Tuple[Token, ParserState]:
    """
    消费指定类型的 token。
    
    Args:
        parser_state: 解析器状态字典，包含 tokens、pos、filename
        token_type: 期望消费的 token 类型
    
    Returns:
        Tuple[Token, ParserState]: (被消费的 token, 更新后的 parser_state)
    
    Raises:
        SyntaxError: 当输入结束或 token 类型不匹配时
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否越界
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    # 获取当前 token
    current_token = tokens[pos]
    
    # 检查类型是否匹配
    if current_token["type"] != token_type:
        actual_type = current_token["type"]
        raise SyntaxError(f"Expected {token_type}, got {actual_type}")
    
    # 返回 token 和更新后的状态
    updated_state = {
        "tokens": tokens,
        "pos": pos + 1,
        "filename": parser_state.get("filename", ""),
        "error": parser_state.get("error", "")
    }
    
    return current_token, updated_state

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function