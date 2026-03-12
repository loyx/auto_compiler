# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_block_package._parse_block_src import _parse_block
from ._parse_param_list_package._parse_param_list_src import _parse_param_list

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
def _parse_def_stmt(parser_state: ParserState) -> AST:
    """解析 def 语句（函数定义）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "unknown")

    # 1. 消费 DEF token
    if pos >= len(tokens) or tokens[pos]["type"] != "DEF":
        raise SyntaxError(f"Expected DEF at {filename}:{_get_loc(tokens, pos)}")
    def_token = tokens[pos]
    pos += 1

    # 2. 解析函数名
    if pos >= len(tokens) or tokens[pos]["type"] != "IDENTIFIER":
        raise SyntaxError(f"Expected function name at {filename}:{_get_loc(tokens, pos)}")
    name_token = tokens[pos]
    pos += 1

    # 3. 消费 LPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "LPAREN":
        raise SyntaxError(f"Expected '(' at {filename}:{_get_loc(tokens, pos)}")
    pos += 1

    # 4. 解析参数列表
    params_ast, pos = _parse_param_list(parser_state, pos)
    parser_state["pos"] = pos

    # 5. 消费 RPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "RPAREN":
        raise SyntaxError(f"Expected ')' at {filename}:{_get_loc(tokens, pos)}")
    pos += 1

    # 6. 消费 COLON
    if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
        raise SyntaxError(f"Expected ':' at {filename}:{_get_loc(tokens, pos)}")
    pos += 1

    parser_state["pos"] = pos

    # 7. 解析函数体
    block_ast = _parse_block(parser_state)

    return {
        "type": "DEF",
        "value": name_token["value"],
        "children": [params_ast, block_ast],
        "line": def_token["line"],
        "column": def_token["column"]
    }

# === helper functions ===
def _get_loc(tokens: list, pos: int) -> str:
    """获取位置字符串 'line:column'。"""
    if pos >= len(tokens):
        return "EOF:0"
    return f"{tokens[pos]['line']}:{tokens[pos]['column']}"

# === OOP compatibility layer ===
