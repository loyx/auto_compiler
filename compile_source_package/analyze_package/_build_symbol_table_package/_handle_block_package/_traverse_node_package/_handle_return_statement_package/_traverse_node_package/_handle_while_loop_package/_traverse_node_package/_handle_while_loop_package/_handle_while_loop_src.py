# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# _traverse_node is a direct child function, must use package layer
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表 (List[AST])
#   "line": int,             # 行号
#   "column": int,           # 列号
#   "condition": Any,        # 循环条件表达式 (AST 节点)
#   "body": Any,             # 循环体代码块 (AST 节点，通常是 block)
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_while_loop(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 while_loop 类型 AST 节点。
    
    递归遍历 condition 和 body 子节点，由 _traverse_node 分发处理。
    不修改 symbol_table，不处理作用域管理。
    """
    # 处理循环条件表达式
    condition = node.get("condition")
    if condition is not None:
        _traverse_node(condition, symbol_table)
    
    # 处理循环体代码块
    body = node.get("body")
    if body is not None:
        _traverse_node(body, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
