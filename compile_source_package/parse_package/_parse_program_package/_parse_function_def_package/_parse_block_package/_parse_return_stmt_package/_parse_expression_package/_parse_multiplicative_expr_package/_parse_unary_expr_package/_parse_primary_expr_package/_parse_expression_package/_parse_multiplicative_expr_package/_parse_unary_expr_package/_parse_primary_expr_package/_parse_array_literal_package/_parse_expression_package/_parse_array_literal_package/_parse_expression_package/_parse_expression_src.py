# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# 注意：以下子函数将在后续由子 agent 实现，当前按声明直接 import
from ._parse_array_literal_package._parse_array_literal_src import _parse_array_literal
from ._parse_object_literal_package._parse_object_literal_src import _parse_object_literal
from ._parse_grouped_expression_package._parse_grouped_expression_src import _parse_grouped_expression
from ._parse_literal_package._parse_literal_src import _parse_literal
from ._parse_identifier_package._parse_identifier_src import _parse_identifier

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,        # e.g., "LEFT_BRACKET", "STRING", "IDENTIFIER"
#   "value": Any,       # token 的实际值
#   "line": int,        # 行号
#   "column": int       # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,        # 节点类型，如 "ArrayLiteral", "Identifier"
#   "children": list,   # 子节点列表
#   "value": Any,       # 叶节点的实际值
#   "line": int,        # 起始行号
#   "column": int       # 起始列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,     # Token 列表
#   "pos": int,         # 当前位置索引
#   "filename": str,    # 源文件名
#   "error": str        # 错误信息（可选）
# }


# === main function ===
def _parse_expression(parser_state: ParserState) -> AST:
    """
    解析通用表达式的入口函数/分发器。
    
    根据当前 token 类型分发到具体解析器：
    - LEFT_BRACKET '[' -> _parse_array_literal
    - LEFT_BRACE '{' -> _parse_object_literal
    - LEFT_PAREN '(' -> _parse_grouped_expression
    - STRING/NUMBER/BOOLEAN/NULL -> _parse_literal
    - IDENTIFIER -> _parse_identifier
    
    返回解析得到的 AST 节点。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # 检查输入结束
    if pos >= len(tokens):
        raise SyntaxError(
            f"{filename}:?:? Unexpected end of input, expected expression"
        )
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # 根据 token 类型分发
    if token_type == "LEFT_BRACKET":
        return _parse_array_literal(parser_state)
    elif token_type == "LEFT_BRACE":
        return _parse_object_literal(parser_state)
    elif token_type == "LEFT_PAREN":
        return _parse_grouped_expression(parser_state)
    elif token_type in ("STRING", "NUMBER", "BOOLEAN", "NULL"):
        return _parse_literal(parser_state)
    elif token_type == "IDENTIFIER":
        return _parse_identifier(parser_state)
    else:
        # 未知 token 类型
        raise SyntaxError(
            f"{filename}:{current_token.get('line', '?')}:{current_token.get('column', '?')} "
            f"Unexpected token {token_type}"
        )


# === helper functions ===
# 无额外 helper 函数，分发逻辑已在 main function 中完成


# === OOP compatibility layer ===
# 不需要 OOP wrapper，此为普通函数节点
