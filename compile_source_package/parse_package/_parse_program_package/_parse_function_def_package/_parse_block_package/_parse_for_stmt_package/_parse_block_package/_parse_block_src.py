# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Use try-except to allow mocking in tests before import
try:
    from ._parse_statement_package._parse_statement_src import _parse_statement
except (ImportError, AttributeError):
    # Allow tests to provide a mock
    _parse_statement = None

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (INDENT, DEDENT, IDENTIFIER, LITERAL, etc.)
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (PROGRAM, FUNCTION_DEF, PARAM, VAR_DECL, IF_STMT, WHILE_STMT, FOR_STMT, RETURN_STMT, BREAK_STMT, CONTINUE_STMT, EXPR_STMT, BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, BLOCK)
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
def _parse_block(parser_state: dict) -> dict:
    """
    解析 Python 风格的语句块（INDENT/DEDENT 包围）。
    
    输入：parser_state（pos 指向 INDENT token）
    输出：BLOCK 类型 AST 节点
    副作用：原地更新 parser_state["pos"] 到 DEDENT 之后
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查入口 token 必须是 INDENT
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected INDENT")
    
    if tokens[pos]["type"] != "INDENT":
        raise SyntaxError(f"Expected INDENT at line {tokens[pos]['line']}")
    
    # 记录块起始位置并跳过 INDENT
    indent_token = tokens[pos]
    pos += 1
    
    # 收集块内语句
    statements = []
    
    # 循环解析语句直到 DEDENT 或文件结束
    while pos < len(tokens) and tokens[pos]["type"] != "DEDENT":
        stmt = _parse_statement(parser_state)
        statements.append(stmt)
        pos = parser_state["pos"]
    
    # 检查并跳过 DEDENT
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected DEDENT")
    
    if tokens[pos]["type"] != "DEDENT":
        raise SyntaxError(f"Expected DEDENT at line {tokens[pos]['line']}")
    
    pos += 1  # 跳过 DEDENT
    
    # 更新 parser_state 位置
    parser_state["pos"] = pos
    
    # 构建 BLOCK 节点
    return {
        "type": "BLOCK",
        "children": statements,
        "line": indent_token["line"],
        "column": indent_token["column"]
    }

# === helper functions ===
# No helper functions needed for this simple block parser

# === OOP compatibility layer ===
# No OOP wrapper needed for parser internal functions
