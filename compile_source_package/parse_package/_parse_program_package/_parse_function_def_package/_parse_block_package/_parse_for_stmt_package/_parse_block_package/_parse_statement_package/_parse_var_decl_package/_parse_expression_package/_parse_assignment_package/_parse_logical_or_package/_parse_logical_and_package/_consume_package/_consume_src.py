# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this simple token consumption logic

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
def _consume(parser_state: ParserState, expected_type: str, expected_value: str = None) -> Token:
    """
    消耗期望的 token。
    
    验证当前 token 是否匹配期望的类型和值，匹配则前进位置并返回 token，
    不匹配则设置错误信息并抛出异常。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否已到达 token 列表末尾
    if pos >= len(tokens):
        error_msg = f"Unexpected end of input at {parser_state.get('filename', 'unknown')}: expected {expected_type}"
        parser_state["error"] = error_msg
        raise ValueError(error_msg)
    
    current_token = tokens[pos]
    
    # 验证 token 类型
    if current_token.get("type") != expected_type:
        error_msg = (
            f"Token type mismatch at line {current_token.get('line', '?')}, "
            f"column {current_token.get('column', '?')}: "
            f"expected {expected_type}, got {current_token.get('type')}"
        )
        parser_state["error"] = error_msg
        raise ValueError(error_msg)
    
    # 如果提供了期望值，验证 token 值
    if expected_value is not None and current_token.get("value") != expected_value:
        error_msg = (
            f"Token value mismatch at line {current_token.get('line', '?')}, "
            f"column {current_token.get('column', '?')}: "
            f"expected '{expected_value}', got '{current_token.get('value')}'"
        )
        parser_state["error"] = error_msg
        raise ValueError(error_msg)
    
    # 匹配成功，前进位置
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
