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
def _consume_token(parser_state: ParserState) -> Token:
    """
    消费当前 token 并推进解析器位置。
    
    算法：
    1. 获取当前 token：tokens[parser_state["pos"]]
    2. 将 parser_state["pos"] 加 1（in place 修改）
    3. 返回被消费的 token
    
    边界情况：
    - 如果 pos 已超出 tokens 列表长度，返回 EOF token
    
    约束：
    - 必须 in place 修改 parser_state["pos"]
    - 不抛出异常，超出范围时返回 EOF token
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否已到达 token 列表末尾
    if pos >= len(tokens):
        # 返回 EOF token
        return {"type": "EOF", "value": "", "line": 0, "column": 0}
    
    # 获取当前 token
    current_token = tokens[pos]
    
    # in place 修改 pos
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
