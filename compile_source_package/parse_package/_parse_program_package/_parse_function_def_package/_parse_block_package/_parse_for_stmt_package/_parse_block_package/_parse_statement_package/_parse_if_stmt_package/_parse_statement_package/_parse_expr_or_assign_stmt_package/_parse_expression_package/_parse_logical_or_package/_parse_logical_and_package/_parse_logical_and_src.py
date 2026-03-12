# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_equality_package._parse_equality_src import _parse_equality

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
def _parse_logical_and(parser_state: ParserState) -> AST:
    """
    解析逻辑 AND 表达式（&& 运算符）。
    
    算法：
    1. 先调用 _parse_equality 解析左侧操作数
    2. 当遇到 && token 时，循环：消耗 &&，继续解析右侧操作数，构建 BINARY_OP 节点
    3. 返回最终的 AST 节点（可能是单个节点或左结合的 BINARY_OP 链）
    
    输入：parser_state（pos 指向表达式起始）
    输出：AST 节点（BINARY_OP with value="&&" 或其他表达式节点）
    副作用：更新 parser_state["pos"] 到表达式结束
    异常：语法错误抛出 SyntaxError
    """
    # 解析左侧操作数
    left = _parse_equality(parser_state)
    
    # 循环处理连续的 && 运算符
    while _is_logical_and_token(parser_state):
        # 消耗 && token
        op_token = _consume_token(parser_state)
        
        # 解析右侧操作数
        right = _parse_equality(parser_state)
        
        # 构建 BINARY_OP 节点
        left = _build_binary_op(op_token, left, right)
    
    return left


# === helper functions ===
def _is_logical_and_token(parser_state: ParserState) -> bool:
    """
    检查当前位置是否为 && 运算符 token。
    
    返回 True 如果当前 token 是 type="OPERATOR" 且 value="&&"
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        return False
    
    token = tokens[pos]
    return (
        token.get("type") == "OPERATOR" and
        token.get("value") == "&&"
    )


def _consume_token(parser_state: ParserState) -> Token:
    """
    消耗当前位置的 token 并更新 pos。
    
    返回当前 token，副作用是 parser_state["pos"] += 1
    如果 token 列表耗尽，抛出 SyntaxError
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token


def _build_binary_op(op_token: Token, left: AST, right: AST) -> AST:
    """
    构建 BINARY_OP AST 节点。
    
    参数：
    - op_token: 运算符 token（包含 line, column 位置信息）
    - left: 左操作数 AST 节点
    - right: 右操作数 AST 节点
    
    返回：
    {
        "type": "BINARY_OP",
        "value": "&&",
        "children": [left, right],
        "line": op_token["line"],
        "column": op_token["column"]
    }
    """
    return {
        "type": "BINARY_OP",
        "value": op_token.get("value"),
        "children": [left, right],
        "line": op_token.get("line", 0),
        "column": op_token.get("column", 0)
    }


# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node
