# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_package._parse_multiplicative_src import _parse_multiplicative
from ._expect_token_package._expect_token_src import _expect_token

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
#   "op": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "name": AST,
#   "args": list,
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
def _parse_additive(parser_state: ParserState) -> AST:
    """
    解析加法/减法表达式。
    
    处理逻辑：
    1. 调用 _parse_multiplicative 解析左操作数
    2. 检查当前 token 是否为加减运算符类型（PLUS, MINUS）
    3. 若是，消费运算符 token，解析右操作数，构建 BINOP 节点
    4. 返回 AST 节点
    
    异常：语法错误时抛出 SyntaxError，包含 line/column 信息。
    """
    # 解析左操作数（乘除表达式）
    left_ast = _parse_multiplicative(parser_state)
    
    # 检查是否有加减运算符
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        return left_ast
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    
    if token_type not in ("PLUS", "MINUS"):
        return left_ast
    
    # 消费运算符 token
    op_token = _expect_token(parser_state, token_type)
    line = op_token.get("line", 0)
    column = op_token.get("column", 0)
    
    # 解析右操作数（乘除表达式）
    right_ast = _parse_multiplicative(parser_state)
    
    # 确定运算符
    op = "add" if token_type == "PLUS" else "sub"
    
    # 构建 BINOP 节点
    binop_node: AST = {
        "type": "BINOP",
        "op": op,
        "left": left_ast,
        "right": right_ast,
        "line": line,
        "column": column,
        "children": [left_ast, right_ast]
    }
    
    return binop_node


# === helper functions ===
# No helper functions needed; all logic is in main function


# === OOP compatibility layer ===
# Not needed for parser function nodes
