# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple utility

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
    
    Args:
        parser_state: 解析器状态字典，包含 tokens、pos、filename、error
        expected_type: 可选的期望 token 类型，若为 None 则不检查类型
    
    Returns:
        被消费的 token 字典
    
    Raises:
        SyntaxError: 当 pos 越界或 token 类型不匹配时抛出
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Step 1: Check if pos is out of bounds
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    # Step 2: Get current token
    token = tokens[pos]
    
    # Step 3: Check expected_type if provided
    if expected_type is not None and token["type"] != expected_type:
        raise SyntaxError(f"Expected {expected_type}, got {token['type']}")
    
    # Step 4: In-place modify pos
    parser_state["pos"] += 1
    
    # Step 5: Return the consumed token
    return token


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
