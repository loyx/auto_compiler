# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No sub functions needed for this utility function

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
def _consume_token(parser_state: ParserState) -> Optional[Token]:
    """
    消费当前 token 并返回它，更新 parser_state['pos'] += 1。
    
    输入：parser_state - 解析器状态字典
    输出：被消费的 token 字典，若 pos 超出 tokens 范围则返回 None
    副作用：修改 parser_state['pos']
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 检查是否超出范围
    if pos >= len(tokens):
        return None
    
    # 获取当前 token
    token = tokens[pos]
    
    # 更新位置（副作用）
    parser_state["pos"] = pos + 1
    
    return token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
