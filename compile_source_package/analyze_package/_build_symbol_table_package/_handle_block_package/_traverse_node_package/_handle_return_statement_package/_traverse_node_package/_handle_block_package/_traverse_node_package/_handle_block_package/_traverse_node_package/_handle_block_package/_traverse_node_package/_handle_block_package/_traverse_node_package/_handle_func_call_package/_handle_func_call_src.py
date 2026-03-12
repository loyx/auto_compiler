# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this module

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "func_call", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (对于 func_call 是函数名)
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
def _handle_func_call(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理函数调用节点。
    
    验证被调用函数是否已声明，检查参数数量和类型匹配。
    错误记录到 symbol_table["errors"]，不抛出异常。
    """
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 提取节点信息
    func_name = node.get("value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    children = node.get("children", [])
    
    # 检查函数是否已声明
    functions = symbol_table.get("functions", {})
    
    if func_name not in functions:
        # 函数未声明，记录错误
        error_msg = f"Line {line}, Column {column}: Call to undeclared function '{func_name}'"
        symbol_table["errors"].append(error_msg)
        return
    
    # 函数已声明，获取函数定义信息
    func_def = functions[func_name]
    expected_params = func_def.get("params", [])
    
    # 检查参数数量
    actual_arg_count = len(children)
    expected_arg_count = len(expected_params) if isinstance(expected_params, list) else 0
    
    if actual_arg_count != expected_arg_count:
        error_msg = (
            f"Line {line}, Column {column}: Function '{func_name}' expects "
            f"{expected_arg_count} argument(s), got {actual_arg_count}"
        )
        symbol_table["errors"].append(error_msg)
        return
    
    # 检查参数类型（如果函数定义中包含参数类型信息）
    for i, arg_node in enumerate(children):
        if i < len(expected_params):
            param_def = expected_params[i]
            expected_type = None
            actual_type = arg_node.get("data_type")
            
            # 从参数定义中提取期望类型
            if isinstance(param_def, dict):
                expected_type = param_def.get("data_type")
            elif isinstance(param_def, str):
                expected_type = param_def
            
            # 类型检查（如果两者都有类型信息）
            if expected_type and actual_type and expected_type != actual_type:
                arg_line = arg_node.get("line", line)
                arg_column = arg_node.get("column", column)
                error_msg = (
                    f"Line {arg_line}, Column {arg_column}: Type mismatch for argument {i + 1} "
                    f"of function '{func_name}': expected '{expected_type}', got '{actual_type}'"
                )
                symbol_table["errors"].append(error_msg)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node