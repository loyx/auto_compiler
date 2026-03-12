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
#   "tokens": list,          # Token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 文件名
#   "error": str             # 错误信息
# }

# === main function ===
def _expect_token(parser_state: ParserState, token_type: str) -> Token:
    """
    验证并消耗期望类型的 token。
    
    从 parser_state 中获取当前位置的 token，检查其类型是否匹配期望值。
    若匹配则消耗该 token（pos += 1）并返回；若不匹配则抛出 SyntaxError。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 边界检查：是否已超出 token 列表
    if pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of input: expected token type '{token_type}', but no token found"
        )
    
    current_token = tokens[pos]
    
    # 检查 token 类型是否匹配
    if current_token["type"] != token_type:
        raise SyntaxError(
            f"Expected token type '{token_type}', got '{current_token['type']}' "
            f"at line {current_token.get('line', '?')}, column {current_token.get('column', '?')}"
        )
    
    # 消耗 token：更新位置
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
