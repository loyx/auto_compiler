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

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
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
def _parse_continue_stmt(parser_state: ParserState) -> AST:
    """
    解析 continue 语句。
    语法：continue ;
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]

    # 步骤 1: 检查当前 token 是否为 CONTINUE
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: unexpected end of input, expected 'continue'")

    current_token = tokens[pos]
    if current_token["type"] != "CONTINUE":
        raise SyntaxError(
            f"{filename}:{current_token['line']}:{current_token['column']}: "
            f"expected 'continue', found '{current_token['value']}'"
        )

    continue_line = current_token["line"]
    continue_column = current_token["column"]

    # 步骤 2: 消耗 CONTINUE token
    pos += 1

    # 步骤 3: 检查下一个 token 是否为 SEMICOLON
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{continue_line}:{continue_column}: expected ';' after 'continue'")

    next_token = tokens[pos]
    if next_token["type"] != "SEMICOLON":
        raise SyntaxError(
            f"{filename}:{next_token['line']}:{next_token['column']}: "
            f"expected ';', found '{next_token['value']}'"
        )

    # 步骤 4: 消耗 SEMICOLON token
    pos += 1

    # 原地更新 parser_state 的 pos
    parser_state["pos"] = pos

    # 步骤 5: 返回 CONTINUE_STMT AST 节点
    ast_node: AST = {
        "type": "CONTINUE_STMT",
        "children": [],
        "line": continue_line,
        "column": continue_column
    }

    return ast_node


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function
