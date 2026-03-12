# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
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
def _expect_token(parser_state: ParserState, token_type: str) -> Token:
    """
    期望当前 token 为指定类型。
    
    检查 parser_state["tokens"][parser_state["pos"]] 的 type 是否等于 token_type。
    如果匹配：消耗该 token（pos += 1）并返回该 token 字典。
    如果不匹配或已超出 tokens 范围：抛出 SyntaxError。
    
    副作用：更新 parser_state["pos"]。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否越界
    if pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of input, expected {token_type}"
        )
    
    current_token = tokens[pos]
    
    # 检查 token 类型是否匹配
    if current_token["type"] != token_type:
        raise SyntaxError(
            f"Expected {token_type}, got {current_token['type']} "
            f"at line {current_token['line']}, column {current_token['column']}"
        )
    
    # 消耗 token
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions

# === OOP compatibility layer ===
# No OOP wrapper needed for this utility function
