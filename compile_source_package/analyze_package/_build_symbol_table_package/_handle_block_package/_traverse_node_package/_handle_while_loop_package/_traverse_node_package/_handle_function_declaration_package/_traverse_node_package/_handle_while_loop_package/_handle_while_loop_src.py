# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Deferred import to avoid circular dependency
_traverse_node = None

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "name": str,             # 函数名
#   "params": list,          # 参数列表
#   "body": AST,             # 函数体
#   "return_type": str,      # 返回类型
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,
#   "scope_stack": list
# }

# === main function ===
def _handle_while_loop(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 while 循环节点，递归遍历条件表达式和循环体。
    
    Args:
        node: while_loop 类型的 AST 节点，包含 condition 和 body 字段
        symbol_table: 符号表，会被递归遍历过程修改
    """
    condition = node.get("condition")
    body = node.get("body")
    
    if condition is not None:
        _traverse_node(condition, symbol_table)
    
    if body is not None:
        _traverse_node(body, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
