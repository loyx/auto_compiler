# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block", "variable_declaration", "expression" 等)
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
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """递归遍历 AST 节点并根据节点类型分发到对应处理函数。"""
    node_type = node.get("type", "")
    
    if node_type == "variable_declaration":
        _handle_variable_declaration(node, symbol_table)
    elif node_type == "function_declaration":
        _handle_function_declaration(node, symbol_table)
    elif node_type in ("program", "block", "expression"):
        _process_children(node, symbol_table)
    else:
        _process_children(node, symbol_table)

# === helper functions ===
def _process_children(node: AST, symbol_table: SymbolTable) -> None:
    """递归处理节点的所有子节点。"""
    children = node.get("children", [])
    for child in children:
        _traverse_node(child, symbol_table)

# === OOP compatibility layer ===
