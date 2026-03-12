# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# 无子函数调用

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
def _current_token(parser_state: ParserState) -> Optional[Token]:
    """获取当前 token 而不消费（不修改 pos）。
    
    行为：
    1. 从 parser_state 中获取 tokens 列表和 pos 位置
    2. 如果 pos >= len(tokens)，返回 None（表示已到达输入末尾）
    3. 否则返回 tokens[pos]
    
    返回值：
    - 当前 Token 字典，或 None
    
    无副作用：不修改 parser_state 的任何字段。
    """
    # 从 parser_state 中提取 tokens 和 pos
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 检查是否到达输入末尾
    if pos >= len(tokens):
        return None
    
    # 返回当前 token
    return tokens[pos]

# === helper functions ===
# 无辅助函数

# === OOP compatibility layer ===
# 普通函数节点，无需 OOP wrapper