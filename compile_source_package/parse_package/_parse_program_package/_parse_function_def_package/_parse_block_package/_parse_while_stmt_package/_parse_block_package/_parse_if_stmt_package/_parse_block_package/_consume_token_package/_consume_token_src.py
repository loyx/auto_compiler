# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions required for this utility function

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
    
    行为：
    1. 检查当前位置是否越界，如果越界抛出 SyntaxError("Unexpected end of file")
    2. 获取当前 token
    3. 如果指定了 expected_type 且当前 token 类型不匹配，抛出 SyntaxError
    4. 推进 parser_state['pos'] += 1
    5. 返回被消费的 token
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check bounds
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of file")
    
    # Get current token
    current_token = tokens[pos]
    
    # Validate expected type if specified
    if expected_type is not None and current_token["type"] != expected_type:
        raise SyntaxError(
            f"Expected token type '{expected_type}', got '{current_token['type']}'"
        )
    
    # Advance position
    parser_state["pos"] = pos + 1
    
    return current_token


# === helper functions ===
# No helper functions needed for this focused utility

# === OOP compatibility layer ===
# Not required - this is a utility function, not a framework entry point
