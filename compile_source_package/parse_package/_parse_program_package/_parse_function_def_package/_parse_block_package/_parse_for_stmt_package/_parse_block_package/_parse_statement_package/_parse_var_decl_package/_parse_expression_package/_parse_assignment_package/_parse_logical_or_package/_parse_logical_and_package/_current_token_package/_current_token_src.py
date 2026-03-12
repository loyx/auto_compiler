# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# 无子函数调用

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
def _current_token(parser_state: ParserState) -> Optional[Token]:
    """
    获取当前位置的 token。
    
    从 parser_state["tokens"] 中根据 parser_state["pos"] 获取当前 token。
    如果 pos 超出 tokens 范围，返回 None。
    不修改 parser_state，无副作用。
    
    Args:
        parser_state: 解析器状态字典，包含 tokens（token 列表）、pos（当前位置）、filename（源文件名）
        
    Returns:
        Token: 当前 token 字典，若越界则返回 None
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 检查 pos 是否在有效范围内
    if 0 <= pos < len(tokens):
        return tokens[pos]
    else:
        return None

# === helper functions ===
# 无 helper 函数

# === OOP compatibility layer ===
# 不需要 OOP wrapper，纯函数节点