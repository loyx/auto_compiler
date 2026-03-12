# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (函数名、变量名、字面量等)
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
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> None:
    """处理函数调用节点。验证函数是否已声明，检查参数数量，递归处理参数表达式。"""
    func_name = node.get("value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 检查函数是否已声明
    functions = symbol_table.get("functions", {})
    if func_name not in functions:
        symbol_table["errors"].append({
            "error_type": "undefined_function",
            "line": line,
            "column": column,
            "message": f"Undefined function '{func_name}'",
            "function_name": func_name
        })
        return
    
    # 函数已声明，验证参数数量
    func_def = functions[func_name]
    expected_params = func_def.get("params", [])
    actual_args = node.get("children", [])
    
    if len(actual_args) != len(expected_params):
        symbol_table["errors"].append({
            "error_type": "parameter_count_mismatch",
            "line": line,
            "column": column,
            "message": f"Function '{func_name}' expects {len(expected_params)} arguments, got {len(actual_args)}",
            "function_name": func_name
        })
    
    # 递归处理每个参数表达式
    for arg_node in actual_args:
        _traverse_node(arg_node, symbol_table)


# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
