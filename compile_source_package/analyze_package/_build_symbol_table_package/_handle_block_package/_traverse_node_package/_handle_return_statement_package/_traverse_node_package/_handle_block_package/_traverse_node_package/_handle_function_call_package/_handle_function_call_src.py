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
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> None:
    """处理函数调用节点，验证函数是否存在并检查参数。"""
    func_name = node.get("value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    errors = symbol_table.setdefault("errors", [])
    
    # 检查函数是否已声明
    functions = symbol_table.get("functions", {})
    if func_name not in functions:
        errors.append(f"Function '{func_name}' not declared at line {line}, column {column}")
        return
    
    # 检查参数数量
    func_info = functions[func_name]
    expected_params = len(func_info.get("params", []))
    actual_args = len(node.get("children", []))
    
    if actual_args != expected_params:
        errors.append(f"Parameter count mismatch for '{func_name}' at line {line}, column {column}")
    
    # 递归遍历实参表达式
    for arg_node in node.get("children", []):
        _traverse_node(arg_node, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node