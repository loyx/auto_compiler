# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Lazy import to avoid circular dependency
_traverse_node = None

def _get_traverse_node():
    global _traverse_node
    if _traverse_node is None:
        from ._traverse_node_package._traverse_node_src import _traverse_node as _tn
        _traverse_node = _tn
    return _traverse_node

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
def _handle_variable_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """处理 variable_declaration 类型节点，注册变量到符号表。"""
    # 初始化符号表必要字段
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    if "current_scope" not in symbol_table:
        symbol_table["current_scope"] = 0
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 提取变量信息
    var_name = node["value"]
    data_type = node["data_type"]
    line = node["line"]
    column = node["column"]
    scope_level = symbol_table["current_scope"]
    
    # 检查变量是否已存在于当前作用域
    if var_name in symbol_table["variables"]:
        existing_var = symbol_table["variables"][var_name]
        if existing_var["scope_level"] == scope_level:
            # 同一作用域内重复定义，记录错误
            error = {
                "message": f"Variable '{var_name}' already declared",
                "line": line,
                "column": column,
                "type": "redefinition"
            }
            symbol_table["errors"].append(error)
        # 不同作用域允许 shadowing，不记录错误，继续注册
        symbol_table["variables"][var_name] = {
            "data_type": data_type,
            "is_declared": True,
            "line": line,
            "column": column,
            "scope_level": scope_level
        }
    else:
        # 注册新变量
        symbol_table["variables"][var_name] = {
            "data_type": data_type,
            "is_declared": True,
            "line": line,
            "column": column,
            "scope_level": scope_level
        }
    
    # 处理初始化表达式（如果有）
    children = node.get("children", [])
    if children:
        _get_traverse_node()(children[0], symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
