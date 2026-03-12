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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_block(parser_state: ParserState) -> AST:
    """解析语句块。输入：parser_state（pos 指向 LBRACE token）。返回：BLOCK AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 检查 LBRACE
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:?:?: Unexpected end of input, expected '{{'")
    
    current_token = tokens[pos]
    if current_token["type"] != "LBRACE":
        raise SyntaxError(f"{filename}:{current_token['line']}:{current_token['column']}: Expected '{{', got {current_token['type']}")
    
    # 记录 LBRACE 位置
    block_line = current_token["line"]
    block_column = current_token["column"]
    
    # 消费 LBRACE
    parser_state["pos"] = pos + 1
    
    # 解析语句列表
    statements = []
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        # 检查 RBRACE
        if current_token["type"] == "RBRACE":
            # 消费 RBRACE
            parser_state["pos"] += 1
            break
        
        # 解析语句
        statement = _parse_statement(parser_state)
        statements.append(statement)
    
    # 检查是否正确闭合
    if parser_state["pos"] > 0 and tokens[parser_state["pos"] - 1]["type"] != "RBRACE":
        last_token = tokens[parser_state["pos"] - 1] if parser_state["pos"] > 0 else current_token
        raise SyntaxError(f"{filename}:{last_token['line']}:{last_token['column']}: Unclosed block, expected '}}'")
    
    # 构建 BLOCK AST 节点
    return {
        "type": "BLOCK",
        "statements": statements,
        "line": block_line,
        "column": block_column
    }

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes
