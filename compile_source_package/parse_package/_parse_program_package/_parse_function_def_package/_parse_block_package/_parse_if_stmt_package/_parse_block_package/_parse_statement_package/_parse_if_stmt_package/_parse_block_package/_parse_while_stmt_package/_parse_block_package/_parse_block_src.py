# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_statement_package._parse_statement_src import _parse_statement
from ._get_current_token_package._get_current_token_src import _get_current_token
from ._consume_token_package._consume_token_src import _consume_token

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
    """
    解析代码块。代码块由 LBRACE 和 RBRACE 包围的语句序列组成。
    输入：parser_state（pos 指向 LBRACE token）。
    输出：BLOCK AST 节点。
    副作用：parser_state["pos"] 指向 RBRACE 之后的下一个 token。
    """
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    # 验证并消费 LBRACE
    current_token = _get_current_token(parser_state)
    if current_token["type"] != "LBRACE":
        raise SyntaxError(
            f"{filename}:{current_token['line']}:{current_token['column']}: "
            f"Expected LBRACE, got {current_token['type']}"
        )
    
    brace_line = current_token["line"]
    brace_column = current_token["column"]
    _consume_token(parser_state)
    
    # 解析块内语句
    statements = []
    while True:
        current_token = _get_current_token(parser_state)
        
        # 检查是否到达块结尾
        if current_token["type"] == "RBRACE":
            break
        
        # 检查是否意外到达文件末尾
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(
                f"{filename}:{brace_line}:{brace_column}: "
                f"Unexpected end of file, expected RBRACE"
            )
        
        # 解析单条语句
        stmt = _parse_statement(parser_state)
        statements.append(stmt)
    
    # 消费 RBRACE
    _consume_token(parser_state)
    
    # 构建并返回 BLOCK AST 节点
    return {
        "type": "BLOCK",
        "statements": statements,
        "line": brace_line,
        "column": brace_column
    }

# === helper functions ===
# No helper functions needed; logic is delegated to sub-functions.

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node.
