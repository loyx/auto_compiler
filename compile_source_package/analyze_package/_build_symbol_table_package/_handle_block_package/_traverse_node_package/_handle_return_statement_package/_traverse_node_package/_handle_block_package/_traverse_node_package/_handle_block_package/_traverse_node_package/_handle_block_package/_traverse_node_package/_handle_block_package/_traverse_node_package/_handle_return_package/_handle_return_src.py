# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions delegated

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "return", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (return 语句中为返回值表达式，可选)
#   "data_type": str,        # 类型信息 ("int" 或 "char"，可选)
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
#   "current_function": str,       # 当前函数名 (可选，None 表示不在函数内)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _handle_return(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 return 语句节点。
    
    验证 return 是否在函数内，检查返回类型是否匹配。
    错误记录到 symbol_table["errors"]，不抛出异常。
    """
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 检查是否在函数内
    current_function = symbol_table.get("current_function")
    if not current_function:
        error_msg = f"Error at line {line}, column {column}: return statement outside function"
        symbol_table["errors"].append(error_msg)
        return
    
    # 获取函数返回类型
    functions = symbol_table.get("functions", {})
    func_info = functions.get(current_function, {})
    expected_return_type = func_info.get("return_type")
    
    # 检查返回值类型 (如果存在返回值)
    return_value = node.get("value")
    if return_value is not None:
        actual_type = node.get("data_type")
        if expected_return_type and actual_type and expected_return_type != actual_type:
            error_msg = f"Error at line {line}, column {column}: return type '{actual_type}' does not match function return type '{expected_return_type}'"
            symbol_table["errors"].append(error_msg)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function node