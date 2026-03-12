# === std / third-party imports ===
from typing import Any, Dict

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
def _handle_program(node: AST, symbol_table: SymbolTable) -> None:
    """处理 program 节点：初始化符号表作用域并遍历子节点。"""
    # 延迟导入以避免循环依赖
    from ._traverse_node_package._traverse_node_src import _traverse_node
    
    # 初始化符号表
    symbol_table["current_scope"] = 0
    symbol_table["scope_stack"] = []
    
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 递归遍历子节点
    if "children" in node and node["children"]:
        for child in node["children"]:
            _traverse_node(child, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node