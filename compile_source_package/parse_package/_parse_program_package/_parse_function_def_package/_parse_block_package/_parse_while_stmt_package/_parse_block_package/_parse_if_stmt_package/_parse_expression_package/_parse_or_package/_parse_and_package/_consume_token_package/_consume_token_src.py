# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# 无子函数依赖

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
def _consume_token(parser_state: ParserState, token_type: str) -> Token:
    """
    消耗指定类型的 token。
    
    参数:
        parser_state: 解析器状态字典，包含 tokens、pos、filename、error
        token_type: 期望的 token 类型字符串（区分大小写）
    
    返回:
        成功时返回 token 字典，失败时返回空字典 {}
    
    副作用:
        - 匹配成功时：parser_state["pos"] += 1
        - 失败时：设置 parser_state["error"] 错误信息
        - pos 仅在匹配成功时前进，失败时保持不变
    
    调用方通过检查 parser_state.get("error") 判断失败，不检查返回值。
    """
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    
    # 边界检查：tokens 耗尽
    if pos >= len(tokens):
        parser_state["error"] = f"Unexpected end of file, expected {token_type}"
        return {}
    
    current_token = tokens[pos]
    actual_type = current_token.get("type")
    
    # 类型检查
    if actual_type != token_type:
        parser_state["error"] = f"Expected token type {token_type}, got {actual_type}"
        return {}
    
    # 匹配成功，pos 前进
    parser_state["pos"] = pos + 1
    return current_token

# === helper functions ===
# 无 helper 函数

# === OOP compatibility layer ===
# 普通函数节点，无需 OOP wrapper