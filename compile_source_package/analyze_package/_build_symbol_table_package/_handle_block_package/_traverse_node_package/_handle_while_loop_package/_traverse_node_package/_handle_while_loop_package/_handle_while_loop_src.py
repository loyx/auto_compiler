# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Import _traverse_node from parent module as specified in requirements
# Note: Use lazy import to avoid circular dependency

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "condition": AST,        # while_loop 条件节点
#   "body": AST              # while_loop 循环体节点
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list            # 作用域栈
# }

# === main function ===
def _handle_while_loop(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 while_loop 节点，递归遍历其子节点。
    
    处理逻辑：
    1. 从 node 中提取 "condition" 字段（AST 节点）
    2. 从 node 中提取 "body" 字段（AST 节点）
    3. 如果 condition 不为 None，调用 _traverse_node(condition, symbol_table)
    4. 如果 body 不为 None，调用 _traverse_node(body, symbol_table)
    
    副作用：通过递归调用 _traverse_node 可能修改 symbol_table
    """
    # Lazy import to avoid circular dependency
    from .._traverse_node_src import _traverse_node
    
    condition = node.get("condition")
    body = node.get("body")
    
    if condition is not None:
        _traverse_node(condition, symbol_table)
    
    if body is not None:
        _traverse_node(body, symbol_table)

# === helper functions ===
# No helper functions needed for this simple traversal logic

# === OOP compatibility layer ===
# Not needed - this is a helper function in a function dependency tree