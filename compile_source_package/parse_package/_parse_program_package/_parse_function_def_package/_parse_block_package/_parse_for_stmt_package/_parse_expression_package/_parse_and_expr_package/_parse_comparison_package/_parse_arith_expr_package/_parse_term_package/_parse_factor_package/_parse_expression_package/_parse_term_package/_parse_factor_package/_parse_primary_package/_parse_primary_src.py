# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple parser

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (PLUS, MINUS, MULTI, DIV, MOD, LPAREN, RPAREN, IDENTIFIER, LITERAL, etc.)
#   "value": str,            # token 值 (+, -, *, /, %, (, ), 标识符名，字面量值等)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, ERROR, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值（运算符字符串或标识符/字面量值）
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }


# === main function ===
def _parse_primary(parser_state: ParserState) -> AST:
    """
    解析 primary（标识符或字面量）。
    
    输入：parser_state（pos 指向 primary 起始 token）
    输出：AST 节点（IDENTIFIER 或 LITERAL 或 ERROR）
    副作用：更新 parser_state['pos'] 越过已处理的 tokens，错误时设置 parser_state['error']
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否还有 token 可用
    if pos >= len(tokens):
        error_msg = "Unexpected end of input: expected identifier or literal"
        parser_state["error"] = error_msg
        return {
            "type": "ERROR",
            "value": error_msg,
            "children": [],
            "line": tokens[-1]["line"] if tokens else 0,
            "column": tokens[-1]["column"] if tokens else 0
        }
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    token_value = current_token["value"]
    token_line = current_token["line"]
    token_column = current_token["column"]
    
    # 处理 IDENTIFIER
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {
            "type": "IDENTIFIER",
            "value": token_value,
            "children": [],
            "line": token_line,
            "column": token_column
        }
    
    # 处理 LITERAL
    elif token_type == "LITERAL":
        parser_state["pos"] = pos + 1
        return {
            "type": "LITERAL",
            "value": token_value,
            "children": [],
            "line": token_line,
            "column": token_column
        }
    
    # 其他情况：错误
    else:
        error_msg = f"Expected identifier or literal, got '{token_value}' ({token_type})"
        parser_state["error"] = error_msg
        return {
            "type": "ERROR",
            "value": error_msg,
            "children": [],
            "line": token_line,
            "column": token_column
        }


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for internal parser function