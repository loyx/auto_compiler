# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block" 等)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值 (变量名可能在此字段)
#   "name": str,             # 节点名称 (变量名可能在此字段)
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
    """
    处理 variable_declaration 类型节点。
    从 node 提取变量名、数据类型、行列号，注册到 symbol_table['variables']。
    如果变量已在当前作用域声明，记录重复声明错误到 symbol_table['errors']。
    
    Resource I/O:
    - READ: symbol_table['variables'], symbol_table['current_scope'], symbol_table['errors']
    - WRITE: symbol_table['variables'][var_name], symbol_table['errors'] (mutable state modification)
    """
    # 提取变量名 (可能在 "value" 或 "name" 字段)
    var_name = node.get("value") or node.get("name")
    if not var_name:
        return
    
    # 提取数据类型、行列号
    data_type = node.get("data_type", "int")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 获取当前作用域层级
    current_scope = symbol_table.get("current_scope", 0)
    
    # 初始化 errors 列表 (如果不存在)
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 检查变量是否已声明
    variables = symbol_table.get("variables", {})
    if var_name in variables:
        existing_var = variables[var_name]
        # 检查是否在同一作用域
        if existing_var.get("scope_level") == current_scope:
            # 重复声明错误
            error_msg = f"Duplicate declaration of variable '{var_name}' at line {line}, column {column}"
            symbol_table["errors"].append({
                "type": "duplicate_declaration",
                "message": error_msg,
                "line": line,
                "column": column,
                "variable": var_name
            })
            return
    
    # 注册变量信息
    variables[var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }
    symbol_table["variables"] = variables

# === helper functions ===

# === OOP compatibility layer ===
