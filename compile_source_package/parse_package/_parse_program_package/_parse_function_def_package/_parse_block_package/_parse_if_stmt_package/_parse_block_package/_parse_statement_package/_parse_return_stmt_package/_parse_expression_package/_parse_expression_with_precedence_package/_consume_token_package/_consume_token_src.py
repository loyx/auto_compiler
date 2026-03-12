# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._current_token_package._current_token_src import _current_token

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
def _consume_token(parser_state: ParserState, expected_type: str | None = None) -> Token:
    """
    消费当前 token 并前进 pos 位置。
    
    资源读写说明：
    - 读：读取 parser_state["tokens"]、parser_state["pos"]、parser_state.get("filename")
    - 写：修改 parser_state["pos"] += 1（原地修改传入的 mutable 状态对象）
    
    Args:
        parser_state: 解析器状态字典，包含 tokens 列表和当前位置 pos
        expected_type: 可选的 token 类型约束，若不匹配则抛出 SyntaxError
    
    Returns:
        被消费的 token 对象
    
    Raises:
        SyntaxError: 当没有更多 token 或 token 类型不匹配时
    """
    token = _current_token(parser_state)
    
    if token is None:
        raise SyntaxError(f"No more tokens to consume in {parser_state.get('filename', 'unknown')}")
    
    if expected_type is not None and token.get("type") != expected_type:
        raise SyntaxError(
            f"Expected token type '{expected_type}', got '{token.get('type')}' "
            f"at line {token.get('line', '?')}, column {token.get('column', '?')} "
            f"in {parser_state.get('filename', 'unknown')}"
        )
    
    # 副作用：原地修改 parser_state 的 pos 字段
    parser_state["pos"] += 1
    return token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
