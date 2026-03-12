# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple parser

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,         # "STRING" | "NUMBER" | "BOOLEAN" | "NULL" | ...
#   "value": str,        # token 原始值
#   "line": int,         # 行号
#   "column": int        # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,         # 节点类型，如 "Literal"
#   "value": Any,        # 节点值
#   "line": int,         # 行号
#   "column": int,       # 列号
#   "children": list     # 子节点列表
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,      # Token 列表
#   "pos": int,          # 当前位置
#   "filename": str,     # 源文件名
#   "error": str         # 错误信息（可选）
# }


# === main function ===
def _parse_literal(parser_state: ParserState) -> AST:
    """
    解析字面量值。
    输入：parser_state（当前位置在 STRING/NUMBER/BOOLEAN/NULL token）
    输出：字面量 AST 节点
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "unknown")

    # 检查 pos 越界
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {filename}")

    current_token = tokens[pos]
    token_type = current_token["type"]
    token_value = current_token["value"]
    line = current_token["line"]
    column = current_token["column"]

    # 根据 token 类型解析值
    if token_type == "STRING":
        parsed_value = token_value  # 已解码，不含引号
    elif token_type == "NUMBER":
        parsed_value = _parse_number(token_value, line, column, filename)
    elif token_type == "BOOLEAN":
        parsed_value = _parse_boolean(token_value, line, column, filename)
    elif token_type == "NULL":
        parsed_value = None
    else:
        raise SyntaxError(
            f"Expected literal token (STRING/NUMBER/BOOLEAN/NULL), "
            f"got {token_type} at line {line}, column {column} in {filename}"
        )

    # 消耗当前 token
    parser_state["pos"] = pos + 1

    # 返回 AST 节点
    return {
        "type": "Literal",
        "value": parsed_value,
        "line": line,
        "column": column,
        "children": []
    }


# === helper functions ===
def _parse_number(value: str, line: int, column: int, filename: str) -> Any:
    """
    将数字字符串转换为 int 或 float。
    尝试 int()，失败则 float()。
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            raise SyntaxError(
                f"Invalid number format '{value}' at line {line}, "
                f"column {column} in {filename}"
            )


def _parse_boolean(value: str, line: int, column: int, filename: str) -> bool:
    """
    将布尔字符串转换为 Python bool。
    "true" -> True, "false" -> False
    """
    if value == "true":
        return True
    elif value == "false":
        return False
    else:
        raise SyntaxError(
            f"Invalid boolean value '{value}' at line {line}, "
            f"column {column} in {filename}. Expected 'true' or 'false'"
        )


# === OOP compatibility layer ===
# No OOP wrapper needed for this parser helper function
