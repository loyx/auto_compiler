# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("var_decl")
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值（变量名）
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
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """处理变量声明节点，将变量记录到符号表，检测重复声明。"""
    # 从 node 提取信息
    var_name = node.get("value")
    data_type = node.get("data_type")
    line = node.get("line", 0)
    column = node.get("column", 0)
    current_scope = symbol_table.get("current_scope", 0)
    
    # 确保 variables 和 errors 存在
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    variables = symbol_table["variables"]
    errors = symbol_table["errors"]
    
    # 检查是否在当前作用域已声明
    if var_name in variables:
        existing = variables[var_name]
        if existing.get("scope_level") == current_scope:
            # 重复声明错误
            errors.append({
                "type": "scope_error",
                "line": line,
                "column": column,
                "message": f"Variable '{var_name}' already declared in current scope"
            })
            return
    
    # 记录变量
    variables[var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
