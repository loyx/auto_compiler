# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_binary_package._parse_binary_src import _parse_binary
from ._get_current_token_package._get_current_token_src import _get_current_token
from ._advance_parser_package._advance_parser_src import _advance_parser
from ._check_unary_op_package._check_unary_op_src import _check_unary_op
from ._extract_literal_value_package._extract_literal_value_src import _extract_literal_value
from ._expect_token_type_package._expect_token_type_src import _expect_token_type

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (IDENTIFIER, NUMBER, STRING, MINUS, PLUS, NOT, TILDE, LPAREN, RPAREN, etc.)
#   "value": str,            # token 值 (如 "x", "42", "-", "not", etc.)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (UNARY_OP, IDENTIFIER, LITERAL, BINARY_OP, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值 (UNARY_OP 包含 {"operator": str}，IDENTIFIER/LITERAL 包含具体值)
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
def _parse_unary(parser_state: ParserState) -> AST:
    """
    解析一元表达式或基础项（primary expression）。
    
    处理内容：
    1. 一元运算符（-, +, !, ~, not）：构建 UNARY_OP 节点，递归解析操作数
    2. 标识符（IDENTIFIER）：构建 IDENTIFIER 节点
    3. 字面量（NUMBER/STRING）：构建 LITERAL 节点
    4. 括号表达式（LPAREN）：调用 _parse_binary 解析括号内表达式，期望 RPAREN
    
    副作用：直接修改 parser_state["pos"] 消耗 token。
    异常：遇到无效 token 时抛出 SyntaxError。
    """
    token = _get_current_token(parser_state)
    
    # 检查是否为一元运算符
    if _check_unary_op(token):
        op_token = token
        _advance_parser(parser_state)
        operand = _parse_unary(parser_state)
        return {
            "type": "UNARY_OP",
            "value": {"operator": op_token["value"]},
            "children": [operand],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    # 检查是否为标识符
    if token and token["type"] == "IDENTIFIER":
        _advance_parser(parser_state)
        return {
            "type": "IDENTIFIER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    # 检查是否为字面量
    if token and token["type"] in ("NUMBER", "STRING"):
        _advance_parser(parser_state)
        value = _extract_literal_value(token)
        return {
            "type": "LITERAL",
            "value": value,
            "line": token["line"],
            "column": token["column"]
        }
    
    # 检查是否为括号表达式
    if token and token["type"] == "LPAREN":
        _advance_parser(parser_state)
        expr = _parse_binary(parser_state, min_precedence=0)
        _expect_token_type(parser_state, "RPAREN", ")")
        return expr
    
    # 无效 token
    filename = parser_state.get("filename", "<unknown>")
    line = token["line"] if token else 0
    col = token["column"] if token else 0
    actual = token["type"] if token else "EOF"
    raise SyntaxError(f"{filename}:{line}:{col}: 期望表达式起始，但得到 '{actual}'")

# === helper functions ===
# 所有 helper 逻辑已拆分到子函数节点

# === OOP compatibility layer ===
# 不需要 OOP wrapper，这是内部解析函数节点