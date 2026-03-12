# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub-functions needed for this utility function

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
def _consume_token(parser_state: ParserState) -> ParserState:
    """
    消费当前 token 并推进解析器位置指针。
    
    输入：parser_state（pos 指向待消费 token）
    输出：更新后的 parser_state（pos 已 +1）
    
    处理规则：
    1. 检查 pos 是否超出 tokens 范围
    2. 若未超出，将 pos 加 1
    3. 返回更新后的 parser_state
    
    约束：
    - 不修改 tokens 列表
    - 若 pos 已超出范围，保持 pos 不变
    - 纯内存操作，无副作用
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 检查 pos 是否超出 tokens 范围
    if pos < len(tokens):
        # 若未超出，将 pos 加 1
        parser_state["pos"] = pos + 1
    
    # 返回更新后的 parser_state
    return parser_state

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
