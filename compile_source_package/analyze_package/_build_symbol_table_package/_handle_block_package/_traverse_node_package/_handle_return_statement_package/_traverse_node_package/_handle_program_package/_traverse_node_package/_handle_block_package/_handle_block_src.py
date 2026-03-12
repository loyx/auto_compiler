# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block" 等)
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
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _handle_block(node: AST, symbol_table: SymbolTable) -> None:
    """处理 block 类型节点，管理作用域层级。
    
    进入 block 时增加作用域层级，遍历子节点，退出时恢复。
    """
    # 1. 进入 block：增加作用域层级
    current_scope = symbol_table.get("current_scope", 0) + 1
    symbol_table["current_scope"] = current_scope
    
    # 2. 压入作用域栈
    scope_stack = symbol_table.setdefault("scope_stack", [])
    scope_stack.append(current_scope)
    
    # 3. 遍历 children，递归处理每个子节点
    for child in node.get("children", []):
        _traverse_node(child, symbol_table)
    
    # 4. 退出 block：弹出栈并恢复作用域层级
    scope_stack.pop()
    symbol_table["current_scope"] = scope_stack[-1] if scope_stack else 0

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this handler function
