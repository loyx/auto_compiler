# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this simple parser

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
    解析 primary（标识符、字面量）。
    
    语法定义：primary: IDENTIFIER | LITERAL
    
    输入：parser_state（pos 指向 primary 起始 token）
    输出：AST 节点（IDENTIFIER 或 LITERAL）
    副作用：更新 parser_state['pos'] 越过已处理的 token，错误时设置 parser_state['error']
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 边界检查：tokens 为空或 pos 越界
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input: expected primary"
        return {
            "type": "ERROR",
            "value": "Unexpected end of input",
            "children": [],
            "line": 0,
            "column": 0
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
    if token_type == "LITERAL":
        parser_state["pos"] = pos + 1
        return {
            "type": "LITERAL",
            "value": token_value,
            "children": [],
            "line": token_line,
            "column": token_column
        }
    
    # 其他类型：错误
    parser_state["error"] = f"Unexpected token '{token_value}': expected identifier or literal"
    return {
        "type": "ERROR",
        "value": f"Unexpected token '{token_value}'",
        "children": [],
        "line": token_line,
        "column": token_column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function