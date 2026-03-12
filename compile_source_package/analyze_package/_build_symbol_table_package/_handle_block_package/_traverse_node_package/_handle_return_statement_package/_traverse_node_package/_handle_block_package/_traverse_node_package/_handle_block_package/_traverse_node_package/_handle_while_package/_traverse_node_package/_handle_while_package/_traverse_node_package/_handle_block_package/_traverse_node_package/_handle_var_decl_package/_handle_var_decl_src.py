# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this logic

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "var_name": str,         # 变量名 (var_decl 节点特有)
#   "name": str              # 变量名 (备选字段名)
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

VarInfo = Dict[str, Any]
# VarInfo possible fields:
# {
#   "data_type": str,        # "int" 或 "char"
#   "is_declared": bool,     # 是否已声明
#   "line": int,             # 声明位置行号
#   "column": int,           # 声明位置列号
#   "scope_level": int       # 作用域层级
# }

# === main function ===
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点。
    
    从 node 提取变量名、数据类型、位置信息，注册到 symbol_table['variables']。
    如果变量已在当前作用域中声明过，记录重复声明错误。
    """
    # 提取变量名 (支持 "var_name" 或 "name" 字段)
    var_name = node.get("var_name") or node.get("name", "")
    data_type = node.get("data_type", "int")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 获取当前作用域层级 (默认 0)
    current_scope = symbol_table.get("current_scope", 0)
    
    # 获取 variables 字典 (如果不存在则初始化)
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 获取 errors 列表 (如果不存在则初始化)
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    variables = symbol_table["variables"]
    errors = symbol_table["errors"]
    
    # 检查变量是否已存在
    if var_name in variables:
        existing_var = variables[var_name]
        # 检查是否在同一作用域中已声明
        if existing_var.get("is_declared", False) and existing_var.get("scope_level") == current_scope:
            # 重复声明错误
            old_line = existing_var.get("line", 0)
            error_msg = f"Variable '{var_name}' already declared at line {old_line}"
            errors.append(error_msg)
            return
    
    # 注册变量信息
    var_info: VarInfo = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }
    variables[var_name] = var_info

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
