# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (必填，永不为空)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (可选)
#   "data_type": str,        # 类型信息 "int" 或 "char" (可选)
#   "line": int,             # 行号 (必填，最小为 0)
#   "column": int            # 列号 (必填，最小为 0)
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
    """处理条件语句节点，管理 then/else 分支的作用域。"""
    then_branch = node.get("then_branch")
    if then_branch:
        symbol_table.setdefault("scope_stack", []).append(symbol_table.get("current_scope", 0))
        symbol_table["current_scope"] = symbol_table.get("current_scope", 0) + 1
        
        for child in then_branch.get("children", []):
            _traverse_node(child, symbol_table)
        
        if symbol_table.get("scope_stack"):
            symbol_table["current_scope"] = symbol_table["scope_stack"].pop()
    
    else_branch = node.get("else_branch")
    if else_branch:
        symbol_table.setdefault("scope_stack", []).append(symbol_table.get("current_scope", 0))
        symbol_table["current_scope"] = symbol_table.get("current_scope", 0) + 1
        
        for child in else_branch.get("children", []):
            _traverse_node(child, symbol_table)
        
        if symbol_table.get("scope_stack"):
            symbol_table["current_scope"] = symbol_table["scope_stack"].pop()

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for internal function node
