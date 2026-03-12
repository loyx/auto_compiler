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
    """
    解析代码块。
    
    输入：parser_state，pos 指向 COLON 之后的 token（通常是 INDENT）
    输出：BLOCK AST 节点
    副作用：消费从 INDENT 到 DEDENT 的全部 token，更新 pos 到 DEDENT 之后
    错误：缺少 INDENT/DEDENT、空 block、缩进不一致时抛 SyntaxError
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # 检查是否以 INDENT 开始
    if pos >= len(tokens):
        raise SyntaxError(f"Expected INDENT after ':' at {filename}:{tokens[-1]['line'] if tokens else 0}")
    
    if tokens[pos]["type"] != "INDENT":
        raise SyntaxError(f"Expected INDENT after ':' at {filename}:{tokens[pos]['line']}")
    
    # 消费 INDENT
    pos += 1
    block_start_line = tokens[pos]["line"] if pos < len(tokens) else tokens[pos - 1]["line"]
    block_start_column = tokens[pos]["column"] if pos < len(tokens) else tokens[pos - 1]["column"]
    
    children = []
    
    # 循环解析语句直到 DEDENT
    while pos < len(tokens) and tokens[pos]["type"] != "DEDENT":
        # 记录语句起始位置
        stmt_line = tokens[pos]["line"]
        stmt_column = tokens[pos]["column"]
        
        # 解析单个语句
        statement_ast = _parse_statement(parser_state)
        children.append(statement_ast)
        
        # 更新 pos（_parse_statement 已更新 parser_state["pos"]）
        pos = parser_state["pos"]
    
    # 检查空 block
    if len(children) == 0:
        raise SyntaxError(f"Empty block not allowed at {filename}:{block_start_line}")
    
    # 检查是否缺少 DEDENT
    if pos >= len(tokens):
        raise SyntaxError(f"Expected DEDENT to close block at {filename}:{block_start_line}")
    
    if tokens[pos]["type"] != "DEDENT":
        raise SyntaxError(f"Expected DEDENT to close block at {filename}:{tokens[pos]['line']}")
    
    # 消费 DEDENT
    pos += 1
    parser_state["pos"] = pos
    
    return {
        "type": "BLOCK",
        "line": block_start_line,
        "column": block_start_column,
        "children": children
    }

# === helper functions ===

# === OOP compatibility layer ===
