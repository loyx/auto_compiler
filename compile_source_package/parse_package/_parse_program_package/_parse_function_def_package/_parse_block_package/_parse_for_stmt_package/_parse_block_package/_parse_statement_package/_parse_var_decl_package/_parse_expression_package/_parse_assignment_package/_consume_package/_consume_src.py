# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions delegated

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
    消耗当前 token 并前进位置。
    
    获取当前 token，验证类型匹配，pos++，返回 token。
    类型不匹配或越界时抛出 SyntaxError。
    副作用：原地修改 parser_state['pos']。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否越界
    if pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of input at {parser_state.get('filename', 'unknown')}"
        )
    
    current_token = tokens[pos]
    
    # 检查类型是否匹配
    if current_token.get("type") != expected_type:
        raise SyntaxError(
            f"Expected token type '{expected_type}', got '{current_token.get('type')}' "
            f"at line {current_token.get('line', '?')}, column {current_token.get('column', '?')}"
        )
    
    # 前进位置
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function