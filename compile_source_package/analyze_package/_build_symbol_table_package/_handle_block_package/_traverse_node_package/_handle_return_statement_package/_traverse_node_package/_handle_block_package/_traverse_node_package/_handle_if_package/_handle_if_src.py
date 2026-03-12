# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
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
#   "scope_stack": list,           # 作用域栈 (存储旧 scope 值)
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _handle_if(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理条件语句节点。
    
    遍历条件表达式和各个分支块，递归调用 _traverse_node 处理子节点。
    错误记录到 symbol_table["errors"]，不抛出异常。
    """
    children = node.get("children", [])
    line = node.get("line", 0)
    column = node.get("column", 0)
    errors = symbol_table.get("errors", [])
    
    # 验证 if 语句结构：至少需要条件表达式和 then 分支
    if len(children) < 2:
        errors.append(f"Invalid if statement at line {line}, column {column}")
        return
    
    # 遍历条件表达式子节点（第一个子节点）
    _traverse_node(children[0], symbol_table)
    
    # 遍历 then 分支块子节点（第二个子节点）
    _traverse_node(children[1], symbol_table)
    
    # 如果存在 else 分支，遍历 else 分支块子节点（第三个子节点）
    if len(children) >= 3:
        _traverse_node(children[2], symbol_table)

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
