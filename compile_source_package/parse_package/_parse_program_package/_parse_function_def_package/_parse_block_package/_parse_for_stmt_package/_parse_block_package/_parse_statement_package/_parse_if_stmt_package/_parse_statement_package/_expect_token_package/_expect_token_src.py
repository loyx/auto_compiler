# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this helper

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
#   "tokens": list[Token],
#   "pos": int,
#   "filename": str,
#   "error": str
# }


# === main function ===
def _expect_token(parser_state: ParserState, expected_type: str) -> None:
    """
    期望当前 token 为指定类型。
    
    若匹配则消耗 token（pos += 1）；若不匹配或到达输入末尾则抛出 SyntaxError。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否超出 tokens 范围
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    current_token = tokens[pos]
    current_type = current_token["type"]
    
    # 检查类型是否匹配
    if current_type != expected_type:
        raise SyntaxError(
            f"Unexpected token '{current_token['value']}' at line {current_token['line']}, "
            f"column {current_token['column']}; expected {expected_type}"
        )
    
    # 消耗 token
    parser_state["pos"] = pos + 1


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function