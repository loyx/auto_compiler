# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# 延迟导入，避免循环依赖问题
# _parse_or_expr 仅在解析括号表达式时使用

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
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
def _parse_primary_expr(parser_state: ParserState) -> AST:
    """解析基本表达式（标识符、字面量、括号表达式）。"""
    if parser_state["pos"] >= len(parser_state["tokens"]):
        raise SyntaxError("意外的文件结束，无法解析基本表达式")

    token = parser_state["tokens"][parser_state["pos"]]
    token_type = token["type"]

    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }

    elif token_type in ("INTEGER", "FLOAT", "STRING", "CHAR"):
        parser_state["pos"] += 1
        value = _convert_literal_value(token)
        return {
            "type": "LITERAL",
            "value": value,
            "line": token["line"],
            "column": token["column"]
        }

    elif token_type in ("TRUE", "FALSE", "NULL"):
        parser_state["pos"] += 1
        value = _convert_special_literal(token_type)
        return {
            "type": "LITERAL",
            "value": value,
            "line": token["line"],
            "column": token["column"]
        }

    elif token_type == "LPAREN":
        parser_state["pos"] += 1  # 消费左括号
        expr_ast = _parse_or_expr(parser_state)
        # 检查并消费右括号
        if parser_state["pos"] >= len(parser_state["tokens"]):
            raise SyntaxError(
                f"{parser_state.get('filename', '<unknown>')}:{token['line']}:{token['column']}: "
                f"意外的文件结束，期望 ')' 但未找到"
            )
        rparen_token = parser_state["tokens"][parser_state["pos"]]
        if rparen_token["type"] != "RPAREN":
            raise SyntaxError(
                f"{parser_state.get('filename', '<unknown>')}:{rparen_token['line']}:{rparen_token['column']}: "
                f"期望 ')' 但得到 '{rparen_token['value']}' ({rparen_token['type']})"
            )
        parser_state["pos"] += 1  # 消费右括号
        return expr_ast

    else:
        raise SyntaxError(
            f"{parser_state.get('filename', '<unknown>')}:{token['line']}:{token['column']}: "
            f"期望基本表达式但得到 '{token['value']}' ({token['type']})"
        )


# === helper functions ===
def _convert_literal_value(token: Token) -> Any:
    """将字面量 token 的值转换为 Python 类型。"""
    token_type = token["type"]
    value = token["value"]

    if token_type == "INTEGER":
        return int(value)
    elif token_type == "FLOAT":
        return float(value)
    elif token_type in ("STRING", "CHAR"):
        # 去除引号
        if len(value) >= 2:
            return value[1:-1]
        return value
    else:
        return value


def _convert_special_literal(token_type: str) -> Any:
    """将特殊字面量转换为 Python 值。"""
    if token_type == "TRUE":
        return True
    elif token_type == "FALSE":
        return False
    elif token_type == "NULL":
        return None
    else:
        return None
