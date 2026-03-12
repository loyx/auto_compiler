# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple validation function

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
def _expect_token(parser_state: ParserState, expected_type: str) -> None:
    """验证并消耗期望类型的 token。
    
    处理逻辑：
    1. 获取 parser_state["tokens"][parser_state["pos"]] 当前 token
    2. 校验当前 token 的 type 字段是否等于 expected_type
    3. 若匹配：parser_state["pos"] 加 1（消耗 token），静默返回 None
    4. 若不匹配：抛出 SyntaxError 异常，错误信息应包含期望类型、实际类型、位置信息
    
    Args:
        parser_state: 解析器状态字典，包含 tokens（list）、pos（int，指向当前 token）、filename（str）等字段
        expected_type: 期望的 token 类型字符串（如 "BREAK"、"SEMICOLON"、"IF" 等）
    
    Returns:
        None（无返回值）
    
    Raises:
        SyntaxError: token 类型不匹配时抛出
    """
    # 获取当前 token
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否越界（由调用方保证，但添加防御性检查）
    if pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of input while expecting '{expected_type}' "
            f"at {parser_state.get('filename', '<unknown>')}"
        )
    
    current_token = tokens[pos]
    
    # 验证 token 类型
    if current_token.get("type") != expected_type:
        # 构造详细的错误信息
        actual_type = current_token.get("type", "UNKNOWN")
        line = current_token.get("line", -1)
        column = current_token.get("column", -1)
        filename = parser_state.get("filename", "<unknown>")
        
        raise SyntaxError(
            f"Expected token type '{expected_type}' but got '{actual_type}' "
            f"at line {line}, column {column} in {filename}"
        )
    
    # 消耗 token：pos 加 1
    parser_state["pos"] = pos + 1

# === helper functions ===
# No helper functions needed for this simple function

# === OOP compatibility layer ===
# No OOP wrapper needed for this pure function