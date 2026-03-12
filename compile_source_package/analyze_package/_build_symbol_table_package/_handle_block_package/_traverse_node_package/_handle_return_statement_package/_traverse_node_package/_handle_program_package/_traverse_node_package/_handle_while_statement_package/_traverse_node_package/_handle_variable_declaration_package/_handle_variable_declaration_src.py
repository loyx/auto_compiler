# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple logic

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "variable_declaration")
#   "children": list,        # 子节点列表
#   "value": str,            # 变量名
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
#   "errors": list                 # 错误列表
# }


# === main function ===
def _handle_variable_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 variable_declaration 类型节点。
    提取变量名、类型、位置信息，检查重复声明，注册到符号表。
    副作用：修改 symbol_table["variables"] 和 symbol_table["errors"]
    """
    # 确保必要的数据结构存在
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    if "errors" not in symbol_table:
        symbol_table["errors"] = []

    # 提取变量信息
    var_name = node["value"]
    data_type = node["data_type"]
    line = node["line"]
    column = node["column"]
    current_scope = symbol_table.get("current_scope", 0)

    # 检查是否在同一作用域内重复声明
    if var_name in symbol_table["variables"]:
        existing_var = symbol_table["variables"][var_name]
        if existing_var.get("scope_level") == current_scope:
            # 同一作用域内重复声明，记录错误
            error_info = {
                "type": "duplicate_declaration",
                "var_name": var_name,
                "line": line,
                "column": column,
                "original_line": existing_var["line"],
                "scope_level": current_scope
            }
            symbol_table["errors"].append(error_info)
            return  # 不覆盖已有变量信息

    # 注册变量到符号表
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
# No OOP wrapper needed for this helper function