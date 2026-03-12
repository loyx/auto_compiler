# === std / third-party imports ===
from typing import Any, Dict

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

# === main function ===
def _handle_block(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 block 类型节点，管理作用域层级。
    
    进入 block 时增加作用域层级，处理所有子节点后恢复。
    """
    # 延迟导入以避免循环导入
    from ._traverse_node_package._traverse_node_src import _traverse_node
    
    # 进入 block：增加作用域层级
    symbol_table["current_scope"] += 1
    symbol_table["scope_stack"].append(symbol_table["current_scope"])
    
    # 遍历所有子节点
    children = node.get("children", [])
    for child_node in children:
        _traverse_node(child_node, symbol_table)
    
    # 离开 block：恢复作用域层级
    symbol_table["scope_stack"].pop()
    symbol_table["current_scope"] = symbol_table["scope_stack"][-1] if symbol_table["scope_stack"] else 0

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
