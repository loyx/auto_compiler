# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

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
def _parse_expression_stmt(parser_state: ParserState) -> AST:
    """
    解析表达式语句。
    
    语法：expression ;
    
    输入：parser_state（pos 指向表达式起始 token）
    输出：EXPRESSION_STMT AST 节点
    副作用：修改 parser_state["pos"] 指向语句结束后的下一个 token
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 获取当前 token 位置信息用于错误报告
    if pos < len(tokens):
        current_token = tokens[pos]
        line = current_token.get("line", 1)
        column = current_token.get("column", 1)
    else:
        line = 1
        column = 1
    
    # 1. 解析表达式
    expression_ast = _parse_expression(parser_state)
    
    # 2. 消费 SEMICOLON
    pos = parser_state["pos"]
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{line}:{column}: Expected ';' after expression")
    
    current_token = tokens[pos]
    if current_token.get("type") != "SEMICOLON":
        token_line = current_token.get("line", line)
        token_column = current_token.get("column", column)
        raise SyntaxError(f"{filename}:{token_line}:{token_column}: Expected ';' after expression")
    
    # 消费分号，移动到下一个 token
    parser_state["pos"] = pos + 1
    
    # 3. 返回 EXPRESSION_STMT AST 节点
    result: AST = {
        "type": "EXPRESSION_STMT",
        "expression": expression_ast,
        "line": line,
        "column": column
    }
    
    return result

# === helper functions ===
# No helper functions needed for this simple orchestration

# === OOP compatibility layer ===
# Not needed for parser function nodes
