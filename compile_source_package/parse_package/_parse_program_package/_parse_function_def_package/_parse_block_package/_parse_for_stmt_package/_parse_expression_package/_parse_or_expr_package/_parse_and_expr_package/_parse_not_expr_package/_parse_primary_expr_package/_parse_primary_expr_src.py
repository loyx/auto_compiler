# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_identifier_package._handle_identifier_src import _handle_identifier
from ._handle_paren_expr_package._handle_paren_expr_src import _handle_paren_expr
from ._build_error_node_package._build_error_node_src import _build_error_node

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (大写字符串)
#   "value": str,            # token 值 (原始字符串)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (IDENTIFIER, LITERAL, CALL, ERROR, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
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
def _parse_primary_expr(parser_state: dict) -> dict:
    """
    解析 primary 表达式（标识符、字面量、括号表达式、函数调用）。
    输入：parser_state，pos 指向表达式起始 token。
    输出：AST 节点，parser_state['pos'] 更新为表达式结束后的位置。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 边界检查
    if pos >= len(tokens):
        last_line = tokens[-1]["line"] if tokens else 0
        last_col = tokens[-1]["column"] if tokens else 0
        return _build_error_node(parser_state, "unexpected end of input", last_line, last_col)
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # 1. 标识符处理
    if token_type == "IDENTIFIER":
        return _handle_identifier(parser_state, current_token)
    
    # 2. 字面量处理
    elif token_type == "LITERAL":
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "value": current_token["value"],
            "line": current_token["line"],
            "column": current_token["column"]
        }
    
    # 3. 括号表达式处理
    elif token_type == "LPAREN":
        return _handle_paren_expr(parser_state, current_token)
    
    # 4. 其他情况：错误
    else:
        return _build_error_node(
            parser_state,
            f"unexpected token: {token_type} at line {current_token['line']}, column {current_token['column']}",
            current_token["line"],
            current_token["column"]
        )


# === helper functions ===
# No helper functions in this file; all delegated to child nodes


# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function
