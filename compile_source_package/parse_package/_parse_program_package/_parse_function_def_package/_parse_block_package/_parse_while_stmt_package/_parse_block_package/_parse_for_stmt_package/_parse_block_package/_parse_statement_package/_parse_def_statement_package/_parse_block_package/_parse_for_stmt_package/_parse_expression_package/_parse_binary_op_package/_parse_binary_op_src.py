# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._is_binary_operator_package._is_binary_operator_src import _is_binary_operator
from ._get_operator_precedence_package._get_operator_precedence_src import _get_operator_precedence
from ._parse_primary_package._parse_primary_src import _parse_primary

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
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_binary_op(parser_state: ParserState, min_precedence: int) -> AST:
    """
    使用优先级攀爬算法解析二元运算表达式。
    输入：parser_state（pos 指向左操作数起始）、min_precedence（最小优先级阈值）
    输出：二元运算 AST 节点或单个操作数节点
    副作用：更新 parser_state["pos"] 消费运算符和右操作数 token
    """
    # 左操作数已由 _parse_primary 解析完成（调用方负责）
    # 这里从当前 pos 开始检查是否有二元运算符
    
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 解析左操作数（如果 pos 还没指向操作数之后的位置）
    # 注意：调用方可能已经解析了左操作数，这里需要判断
    # 按照设计，pos 应该指向左操作数的起始位置
    left = _parse_primary(parser_state)
    left_line = left.get("line", 0)
    left_column = left.get("column", 0)
    
    # 循环处理二元运算符
    while True:
        if parser_state["pos"] >= len(tokens):
            break
        
        current_token = tokens[parser_state["pos"]]
        
        # 检查是否为二元运算符
        if not _is_binary_operator(current_token):
            break
        
        # 检查优先级
        op_precedence = _get_operator_precedence(current_token)
        if op_precedence < min_precedence:
            break
        
        # 记录运算符
        op_token = current_token
        
        # 消费运算符 token
        parser_state["pos"] += 1
        
        # 计算右绑定优先级（左结合：right_precedence = op_precedence + 1）
        right_precedence = op_precedence + 1
        
        # 检查是否有右操作数
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(
                f"Syntax error in {parser_state.get('filename', '<unknown>')}: "
                f"missing right operand after operator '{op_token.get('value', '')}' "
                f"at line {op_token.get('line', 0)}, column {op_token.get('column', 0)}"
            )
        
        # 递归解析右操作数
        right = _parse_binary_op(parser_state, right_precedence)
        
        # 构建二元运算 AST 节点
        left = {
            "type": "BinaryOp",
            "op": op_token,
            "left": left,
            "right": right,
            "line": left_line,
            "column": left_column
        }
    
    return left

# === helper functions ===
# Helper functions are delegated to child modules

# === OOP compatibility layer ===
# Not required for this parser function node
