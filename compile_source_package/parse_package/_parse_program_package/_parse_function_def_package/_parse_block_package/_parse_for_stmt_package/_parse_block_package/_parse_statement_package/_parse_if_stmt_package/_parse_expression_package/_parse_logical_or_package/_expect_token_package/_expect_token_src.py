# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this leaf node

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (PLUS, MINUS, STAR, SLASH, PERCENT, EQ, NE, LT, GT, LE, GE, AND, OR, BANG, IDENTIFIER, INTEGER, STRING, LPAREN, RPAREN)
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
def _expect_token(parser_state: ParserState, expected_type: str) -> Token:
    """
    验证当前 token 类型并推进位置。
    
    如果当前 token 类型匹配 expected_type，推进 pos 并返回该 token。
    如果 token 类型不匹配或已无 token，抛出 SyntaxError。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # 检查是否还有 token
    if pos >= len(tokens):
        # 获取最后一个 token 的位置信息用于错误报告
        if tokens:
            last_token = tokens[-1]
            line = last_token["line"]
            column = last_token["column"]
        else:
            line = 1
            column = 1
        raise SyntaxError(f"{filename}:{line}:{column}: Unexpected end of input, expected '{expected_type}'")
    
    current_token = tokens[pos]
    current_type = current_token["type"]
    
    # 检查 token 类型是否匹配
    if current_type != expected_type:
        line = current_token["line"]
        column = current_token["column"]
        raise SyntaxError(f"{filename}:{line}:{column}: Expected token '{expected_type}' but got '{current_type}'")
    
    # 推进位置
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node