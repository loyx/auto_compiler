# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this module

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
    """处理变量声明节点。
    
    从 node 中提取变量信息，检查是否已声明，
    未声明则添加到 symbol_table，已声明则记录错误。
    """
    # 从 node 中提取变量信息
    var_name = node.get("value")
    data_type = node.get("data_type")
    line = node.get("line")
    column = node.get("column")
    
    # 获取当前作用域层级
    current_scope = symbol_table.get("current_scope", 0)
    
    # 检查变量是否已声明
    if var_name in symbol_table["variables"]:
        # 变量已声明，记录重复声明错误
        error_msg = f"重复声明变量 '{var_name}' (line {line}, column {column})"
        symbol_table["errors"].append(error_msg)
    else:
        # 变量未声明，添加到 symbol_table
        symbol_table["variables"][var_name] = {
            "data_type": data_type,
            "is_declared": True,
            "line": line,
            "column": column,
            "scope_level": current_scope
        }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node