# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed

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
def _consume_token(parser_state: ParserState, token_type: str) -> bool:
    """
    消费指定类型的 token。
    
    行为：
    1. 检查 parser_state["pos"] 是否越界
    2. 如果越界，返回 False
    3. 获取当前 token：tokens[parser_state["pos"]]
    4. 如果当前 token 的 type 字段与 token_type 匹配：
       - parser_state["pos"] += 1
       - 返回 True
    5. 否则返回 False
    
    资源读写说明：
    - 读：parser_state["tokens"], parser_state["pos"]
    - 写：parser_state["pos"] (当 token 类型匹配时递增)
    - 副作用：直接修改传入的 parser_state 字典的 "pos" 字段
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 检查是否越界
    if pos >= len(tokens):
        return False
    
    # 获取当前 token
    current_token = tokens[pos]
    
    # 检查类型是否匹配
    if current_token.get("type") == token_type:
        parser_state["pos"] = pos + 1
        return True
    
    return False

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
