# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this module

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", "function_decl", "param_list", "param", "return", etc.)
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
def _handle_return(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理返回语句节点，验证返回类型与函数声明是否匹配。
    
    副作用：在 symbol_table["errors"] 中记录类型不匹配错误。
    """
    # 确保 errors 列表已初始化
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 从 node 中提取信息
    return_type = node.get("data_type")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 检查是否在函数内部
    current_function = symbol_table.get("current_function")
    if current_function is None or current_function == "":
        error_msg = f"Error at line {line}, column {column}: return statement must be inside a function"
        symbol_table["errors"].append(error_msg)
        return
    
    # 从符号表中获取当前函数的返回类型声明
    functions = symbol_table.get("functions", {})
    func_info = functions.get(current_function)
    
    if func_info is None:
        # 函数未声明，记录错误
        error_msg = f"Error at line {line}, column {column}: function '{current_function}' is not declared"
        symbol_table["errors"].append(error_msg)
        return
    
    declared_return_type = func_info.get("return_type")
    
    # 检查返回类型是否匹配
    # 情况 1: return 语句有返回值类型，但函数声明无返回类型或不匹配
    if return_type is not None and return_type != "":
        if declared_return_type is None or declared_return_type == "":
            error_msg = f"Error at line {line}, column {column}: function '{current_function}' does not return a value, but return statement has a value"
            symbol_table["errors"].append(error_msg)
        elif return_type != declared_return_type:
            error_msg = f"Error at line {line}, column {column}: return type '{return_type}' does not match function return type '{declared_return_type}'"
            symbol_table["errors"].append(error_msg)
    # 情况 2: return 语句无返回值，但函数声明有返回类型
    elif declared_return_type is not None and declared_return_type != "":
        error_msg = f"Error at line {line}, column {column}: function '{current_function}' returns '{declared_return_type}', but return statement has no value"
        symbol_table["errors"].append(error_msg)
    # 情况 3: 两者都为空或无类型，兼容（void return）


# === helper functions ===
# No helper functions needed


# === OOP compatibility layer ===
# Not needed for this function node