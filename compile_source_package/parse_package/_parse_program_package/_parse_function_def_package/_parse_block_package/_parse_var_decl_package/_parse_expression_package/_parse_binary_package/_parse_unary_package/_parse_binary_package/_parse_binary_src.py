# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._get_operator_precedence_package._get_operator_precedence_src import _get_operator_precedence
from ._is_binary_operator_package._is_binary_operator_src import _is_binary_operator
from ._parse_unary_package._parse_unary_src import _parse_unary

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (如 STAR, PLUS, AND 等)
#   "value": str,            # token 值 (如 "*", "+", "and" 等)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值 (对于 BINARY_OP，包含 {"operator": str})
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
def _parse_binary(parser_state: ParserState, min_precedence: int = 0) -> AST:
    """
    使用 Pratt parsing 算法解析二元表达式。
    
    输入：parser_state（pos 指向表达式起始）、min_precedence（最小优先级）
    处理：根据优先级解析左操作数、运算符、右操作数，构建 BINARY_OP 节点
    副作用：直接修改 parser_state["pos"] 消耗 token
    返回：AST 节点
    异常：遇到无效 token 或期望 token 缺失时抛出 SyntaxError
    """
    # 1. 解析左操作数
    left = _parse_unary(parser_state)
    
    # 2. 循环处理二元运算符
    while True:
        # 获取当前 token
        tokens = parser_state["tokens"]
        pos = parser_state["pos"]
        
        # 检查是否还有 token
        if pos >= len(tokens):
            break
        
        current_token = tokens[pos]
        
        # 检查是否为二元运算符
        if not _is_binary_operator(current_token):
            break
        
        # 获取运算符优先级和结合性
        precedence, associativity = _get_operator_precedence(current_token)
        
        # 如果优先级 < min_precedence，跳出循环
        if precedence < min_precedence:
            break
        
        # 对于左结合运算符，如果优先级 == min_precedence，继续循环
        # 对于右结合运算符（**），如果优先级 == min_precedence，停止循环
        if associativity == "left" and precedence == min_precedence:
            break
        
        # 消耗运算符 token
        parser_state["pos"] += 1
        op_token = current_token
        
        # 计算下一次递归的 min_precedence
        if associativity == "left":
            next_min_prec = precedence + 1
        else:
            next_min_prec = precedence
        
        # 递归解析右操作数
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
# No helper functions in this file

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
