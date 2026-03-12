# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this utility

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
def _consume(parser_state: ParserState, expected_type: str) -> Token:
    """
    消耗当前 token 并前进位置指针。
    
    Args:
        parser_state: 解析器状态字典，包含 tokens、pos、filename
        expected_type: 期望消耗的 token 类型字符串
        
    Returns:
        被消耗的 Token 字典
        
    Raises:
        ValueError: 当 token 不存在或类型不匹配时
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查当前 token 是否存在
    if pos >= len(tokens):
        raise ValueError(
            f"Unexpected end of input at {parser_state.get('filename', 'unknown')}: "
            f"expected token type '{expected_type}'"
        )
    
    current_token = tokens[pos]
    
    # 检查当前 token 的 type 是否等于 expected_type
    if current_token["type"] != expected_type:
        raise ValueError(
            f"Token type mismatch at line {current_token.get('line', '?')}, "
            f"column {current_token.get('column', '?')}: "
            f"expected '{expected_type}', got '{current_token['type']}'"
        )
    
    # 匹配：前进位置指针
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
