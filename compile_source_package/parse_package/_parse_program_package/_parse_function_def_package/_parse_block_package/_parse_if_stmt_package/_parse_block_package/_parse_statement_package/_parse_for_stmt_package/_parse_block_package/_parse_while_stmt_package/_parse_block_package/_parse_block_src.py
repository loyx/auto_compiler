# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_statement_package._parse_statement_src import _parse_statement

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
def _parse_block(parser_state: ParserState) -> AST:
    """解析代码块。输入：parser_state（pos 指向 LBRACE）。输出：BLOCK AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]

    # 消费 LBRACE
    if pos >= len(tokens) or tokens[pos]["type"] != "LBRACE":
        raise SyntaxError(f"{filename}:0:0: expected '{{' to start block")

    lbrace_token = tokens[pos]
    parser_state["pos"] = pos + 1

    statements = []

    # 解析语句序列，直到遇到 RBRACE
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]

        # 检查是否到达块结束
        if current_token["type"] == "RBRACE":
            parser_state["pos"] += 1
            break

        # 解析语句
        stmt_ast = _parse_statement(parser_state)
        statements.append(stmt_ast)

        # 检查并消费 SEMICOLON
        if parser_state["pos"] < len(tokens):
            next_token = tokens[parser_state["pos"]]
            if next_token["type"] == "SEMICOLON":
                parser_state["pos"] += 1
            elif next_token["type"] != "RBRACE":
                # 非 RBRACE 且非 SEMICOLON，说明语句未正确结束
                raise SyntaxError(
                    f"{filename}:{next_token['line']}:{next_token['column']}: "
                    f"expected ';' after statement"
                )

    # 检查是否缺少 RBRACE
    if parser_state["pos"] <= pos + 1 or (
        parser_state["pos"] > 0 and tokens[parser_state["pos"] - 1]["type"] != "RBRACE"
    ):
        # 如果循环正常退出但最后一个 token 不是 RBRACE
        if parser_state["pos"] >= len(tokens) or tokens[parser_state["pos"] - 1]["type"] != "RBRACE":
            raise SyntaxError(
                f"{filename}:{lbrace_token['line']}:{lbrace_token['column']}: "
                f"expected '}}' at end of block"
            )

    return {
        "type": "BLOCK",
        "statements": statements,
        "line": lbrace_token["line"],
        "column": lbrace_token["column"]
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
