# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_equality_package._parse_equality_src import _parse_equality

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,        # token 类型，如 "AND", "IDENTIFIER", "NUMBER" 等
#   "value": str,       # token 原始值
#   "line": int,        # 行号
#   "column": int       # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,        # 节点类型，如 "BINARY", "IDENTIFIER", "NUMBER" 等
#   "children": list,   # 子节点列表（可选）
#   "value": Any,       # 节点值（可选）
#   "operator": str,    # 运算符（BINARY 节点）
#   "left": dict,       # 左操作数（BINARY 节点）
#   "right": dict,      # 右操作数（BINARY 节点）
#   "line": int,        # 行号
#   "column": int       # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,     # Token 列表
#   "filename": str,    # 源文件名
#   "pos": int,         # 当前位置索引
#   "error": str        # 错误信息（可选）
# }

# === main function ===
def _parse_and(parser_state: ParserState) -> AST:
    """
    解析 AND 表达式（优先级 Level 5）。
    
    支持左结合，循环处理多个 AND 运算符。
    例如：a AND b AND c 解析为 ((a AND b) AND c)
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 解析左侧操作数（更高优先级的相等性表达式）
    left_ast = _parse_equality(parser_state)
    
    # 循环处理 AND 运算符
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        if current_token.get("type") != "AND":
            break
        
        # 记录 AND 运算符位置
        and_line = current_token.get("line", 0)
        and_column = current_token.get("column", 0)
        
        # 消耗 AND token
        parser_state["pos"] += 1
        
        # 解析右侧操作数
        right_ast = _parse_equality(parser_state)
        
        # 构建 BINARY AST 节点（左结合）
        left_ast = {
            "type": "BINARY",
            "operator": "AND",
            "left": left_ast,
            "right": right_ast,
            "line": and_line,
            "column": and_column
        }
    
    return left_ast

# === helper functions ===
def _raise_syntax_error(parser_state: ParserState, expected: str) -> None:
    """
    抛出语法错误异常。
    
    Args:
        parser_state: 当前解析器状态
        expected: 预期的 token 类型或内容
    
    Raises:
        SyntaxError: 格式为 "{filename}:{line}:{column}: 预期 XXX，但得到 'YYY'"
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos < len(tokens):
        token = tokens[pos]
        line = token.get("line", 0)
        column = token.get("column", 0)
        value = token.get("value", "")
    else:
        line = 0
        column = 0
        value = "EOF"
    
    raise SyntaxError(f"{filename}:{line}:{column}: 预期 {expected}，但得到 '{value}'")

# === OOP compatibility layer ===
# Not required for parser function nodes
