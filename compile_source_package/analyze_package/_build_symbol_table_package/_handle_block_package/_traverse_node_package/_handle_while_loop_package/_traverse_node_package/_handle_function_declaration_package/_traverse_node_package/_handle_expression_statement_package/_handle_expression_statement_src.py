# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "name": str,             # 函数名/节点名
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
def _handle_expression_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理表达式语句节点。
    
    从 node 中提取 expression 字段，递归遍历表达式 AST。
    表达式语句本身不产生副作用，但表达式内部可能包含函数调用等操作会修改符号表。
    """
    expression = node.get("expression")
    if expression is not None:
        _traverse_node(expression, symbol_table)

# === helper functions ===
# No helper functions needed for this simple delegation

# === OOP compatibility layer ===
# Not needed - this is a helper function, not a framework entry point
