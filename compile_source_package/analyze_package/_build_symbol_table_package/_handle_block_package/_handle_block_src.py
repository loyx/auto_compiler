# === std / third-party imports ===
from typing import Any, Callable, Dict

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
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list            # 作用域栈
# }

TraverseFn = Callable[[AST, SymbolTable], None]

# 模块级 _traverse_node 引用，用于支持 mock
# 实际导入在运行时进行，但通过此引用可以被 patch
_traverse_node = None

def _init_traverse_node():
    """延迟初始化 _traverse_node，避免循环依赖。"""
    global _traverse_node
    if _traverse_node is None:
        from ._traverse_node_package._traverse_node_src import _traverse_node as traverse_fn
        _traverse_node = traverse_fn
    return _traverse_node

# === main function ===
def _handle_block(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理代码块节点：进入/退出作用域，遍历块内语句。
    
    处理逻辑：
    1. 进入块作用域：current_scope += 1, scope_stack.append("block")
    2. 遍历块内所有子节点，对每个子节点调用 _traverse_node
    3. 退出块作用域：current_scope -= 1, scope_stack.pop()
    
    使用 try-finally 确保退出作用域一定执行。
    """
    traverse_fn = _init_traverse_node()
    
    symbol_table["current_scope"] += 1
    symbol_table["scope_stack"].append("block")
    
    try:
        for child in node.get("children", []):
            traverse_fn(child, symbol_table)
    finally:
        symbol_table["current_scope"] -= 1
        symbol_table["scope_stack"].pop()

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for internal helper function
