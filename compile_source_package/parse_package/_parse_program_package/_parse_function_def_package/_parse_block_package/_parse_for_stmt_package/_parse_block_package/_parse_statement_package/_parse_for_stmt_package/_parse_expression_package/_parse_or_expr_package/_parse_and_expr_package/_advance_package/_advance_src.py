# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub-functions needed for this simple operation

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
def _advance(parser_state: ParserState) -> Token:
    """
    前进到下一个 token 并返回当前 token。
    
    获取当前 token，将 parser_state["pos"] 加 1，返回更新前的当前 token。
    若 pos 已超出 tokens 范围，返回 EOF token。
    
    Args:
        parser_state: 解析器状态字典，包含 tokens 列表和 pos 当前位置
        
    Returns:
        更新前的当前 Token，若已到达末尾则返回 EOF token
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否已到达末尾
    if pos >= len(tokens):
        return {
            "type": "EOF",
            "value": "",
            "line": 0,
            "column": 0
        }
    
    # 获取当前 token（更新前的）
    current_token = tokens[pos]
    
    # 原地更新 pos
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
