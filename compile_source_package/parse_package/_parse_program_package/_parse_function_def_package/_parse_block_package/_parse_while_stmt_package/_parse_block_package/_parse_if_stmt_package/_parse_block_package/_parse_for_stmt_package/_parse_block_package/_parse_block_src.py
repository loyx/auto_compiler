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
def _parse_block(parser_state: dict) -> dict:
    """
    解析语句块。
    
    语法格式：{ 语句列表 }
    输入：parser_state（pos 指向 LBRACE token）
    输出：BLOCK 类型 AST 节点
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. 验证并消费 LBRACE token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected '{'")
    
    current_token = tokens[pos]
    if current_token["type"] != "LBRACE":
        raise SyntaxError(f"Expected '{{', got {current_token['type']}")
    
    # 记录起始位置
    start_line = current_token["line"]
    start_column = current_token["column"]
    
    # 消费 LBRACE
    parser_state["pos"] = pos + 1
    
    # 2. 循环解析语句
    statements = []
    while parser_state["pos"] < len(tokens):
        current_pos = parser_state["pos"]
        current_token = tokens[current_pos]
        
        # 检查是否遇到 RBRACE（块结束）
        if current_token["type"] == "RBRACE":
            # 消费 RBRACE
            parser_state["pos"] = current_pos + 1
            break
        
        # 3. 调用语句解析函数
        stmt_ast = _parse_statement(parser_state)
        statements.append(stmt_ast)
    
    # 4. 返回 BLOCK 节点
    return {
        "type": "BLOCK",
        "statements": statements,
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
# No helper functions needed for this simple block parser

# === OOP compatibility layer ===
# No OOP wrapper needed for parser internal function
