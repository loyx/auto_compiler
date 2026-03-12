# === std / third-party imports ===
from typing import Any, Dict

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
#   "tokens": list[Token],
#   "filename": str,
#   "pos": int,
#   "error": str
# }


# === main function ===
def _parse_primary(parser_state: ParserState) -> AST:
    """
    解析初级表达式（原子表达式）。
    支持：标识符（IDENT）、数字字面量（NUMBER）、字符串字面量（STRING）、括号表达式 (expr)。
    输入：parser_state，其中 pos 指向初级表达式起始 token。
    输出：AST 节点。
    副作用：更新 parser_state["pos"] 到初级表达式结束位置。
    异常：无法解析时抛出 SyntaxError。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")

    # 检查是否越界
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input")

    token = tokens[pos]
    token_type = token.get("type", "")
    line = token.get("line", 0)
    column = token.get("column", 0)

    # 处理标识符
    if token_type == "IDENT":
        parser_state["pos"] += 1
        return {
            "type": "IDENT",
            "value": token.get("value", ""),
            "line": line,
            "column": column
        }

    # 处理数字字面量
    if token_type == "NUMBER":
        parser_state["pos"] += 1
        value_str = token.get("value", "0")
        # 尝试转为 int，失败则转为 float
        try:
            value = int(value_str)
        except ValueError:
            try:
                value = float(value_str)
            except ValueError:
                value = 0.0
        return {
            "type": "NUMBER",
            "value": value,
            "line": line,
            "column": column
        }

    # 处理字符串字面量
    if token_type == "STRING":
        parser_state["pos"] += 1
        return {
            "type": "STRING",
            "value": token.get("value", ""),
            "line": line,
            "column": column
        }

    # 处理括号表达式
    if token_type == "LPAREN":
        parser_state["pos"] += 1  # 消耗 '('
        # 递归解析括号内的完整表达式（延迟导入以避免循环依赖）
        from ._parse_binary_expression_package._parse_binary_expression_src import _parse_binary_expression
        expr = _parse_binary_expression(parser_state, min_precedence=0)
        # 检查并消耗右括号
        pos = parser_state["pos"]
        if pos >= len(tokens):
            raise SyntaxError(f"{filename}:{line}:{column}: Expected ')', found end of input")
        next_token = tokens[pos]
        if next_token.get("type") != "RPAREN":
            next_line = next_token.get("line", line)
            next_column = next_token.get("column", column)
            raise SyntaxError(f"{filename}:{next_line}:{next_column}: Expected ')', found {next_token.get('type', 'UNKNOWN')}")
        parser_state["pos"] += 1  # 消耗 ')'
        return expr

    # 无法识别的 token 类型
    raise SyntaxError(f"{filename}:{line}:{column}: Expected expression, found {token_type}")


# === helper functions ===
# No helper functions needed for this simple parser

# === OOP compatibility layer ===
# Not needed for parser function nodes
