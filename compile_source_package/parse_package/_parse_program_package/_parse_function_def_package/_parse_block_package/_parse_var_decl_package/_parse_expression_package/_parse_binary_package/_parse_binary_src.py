# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._get_operator_precedence_package._get_operator_precedence_src import _get_operator_precedence

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
#   "value": Any,            # 节点值 (对于 BINARY_OP，包含 operator 字段)
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
def _parse_binary(parser_state: dict, min_precedence: int = 0) -> dict:
    """
    使用优先级爬升算法（Pratt Parsing）解析二元运算符表达式。
    输入：parser_state（pos 指向左侧操作数起始）、min_precedence（最小优先级阈值）。
    输出：AST 节点（BINARY_OP 或单个操作数）。
    """
    # 延迟导入以避免循环依赖
    from ._parse_unary_package._parse_unary_src import _parse_unary
    
    # 1. 解析左侧操作数
    left = _parse_unary(parser_state)
    
    # 2. 循环处理二元运算符
    while _current_token_is_operator(parser_state):
        op_token = _peek_token(parser_state)
        precedence, is_right_assoc = _get_operator_precedence(op_token["type"])
        
        # 优先级不足则停止
        if precedence < min_precedence:
            break
        
        # 消耗运算符 token
        _advance(parser_state)
        
        # 计算右侧递归的最小优先级
        next_min_prec = precedence + 1 if not is_right_assoc else precedence
        
        # 解析右侧操作数
        right = _parse_binary(parser_state, next_min_prec)
        
        # 构建 BINARY_OP 节点
        left = {
            "type": "BINARY_OP",
            "value": {"operator": op_token["value"]},
            "children": [left, right],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
def _current_token_is_operator(parser_state: ParserState) -> bool:
    """检查当前 token 是否为二元运算符。"""
    token = _peek_token(parser_state)
    if token is None:
        return False
    prec, _ = _get_operator_precedence(token["type"])
    return prec > 0

def _peek_token(parser_state: ParserState) -> Token:
    """查看当前 token（不消耗）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos >= len(tokens):
        return None
    return tokens[pos]

def _advance(parser_state: ParserState) -> None:
    """消耗当前 token，前进到下一个。"""
    parser_state["pos"] += 1

def _expect_token(parser_state: ParserState, expected_type: str) -> Token:
    """期望当前 token 为指定类型，否则抛出 SyntaxError。"""
    token = _peek_token(parser_state)
    if token is None or token["type"] != expected_type:
        filename = parser_state.get("filename", "<unknown>")
        line = token["line"] if token else 0
        col = token["column"] if token else 0
        raise SyntaxError(
            f"{filename}:{line}:{col}: 期望 '{expected_type}'，但得到 '{token['type'] if token else 'EOF'}'"
        )
    _advance(parser_state)
    return token

# === OOP compatibility layer ===
# Not required for this function node (parser internal function)
