# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this inline implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "function_call", "block", "var_decl", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (函数名、变量名、字面量值等)
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
#   "errors": list                 # 错误列表，元素为 {"message": str, "line": int, "column": int, "error_type": str}
# }

# === main function ===
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理函数调用节点，验证函数已声明且参数匹配。
    
    处理逻辑：
    1. 从 node["value"] 获取被调用函数名
    2. 检查函数是否在 symbol_table["functions"] 中已声明
    3. 如果未声明，记录"未声明函数"错误
    4. 如果已声明，检查实参数量与形参数量是否匹配
    5. 逐个检查实参类型与形参类型是否匹配
    6. 所有错误记录到 symbol_table["errors"]
    
    副作用：可能向 symbol_table["errors"] 追加错误记录
    """
    func_name = node.get("value", "")
    line = node.get("line", 0)
    column = node.get("column", 0)
    actual_args = node.get("children", [])
    
    # Check if function is declared
    functions = symbol_table.get("functions", {})
    if func_name not in functions:
        error = {
            "message": f"Function '{func_name}' is not declared",
            "line": line,
            "column": column,
            "error_type": "undeclared_function"
        }
        symbol_table["errors"].append(error)
        return
    
    # Get function signature
    func_info = functions[func_name]
    expected_params = func_info.get("params", [])
    expected_count = len(expected_params)
    actual_count = len(actual_args)
    
    # Check parameter count
    if actual_count != expected_count:
        error = {
            "message": f"Function '{func_name}' expects {expected_count} arguments, got {actual_count}",
            "line": line,
            "column": column,
            "error_type": "param_count_mismatch"
        }
        symbol_table["errors"].append(error)
        return
    
    # Check parameter types (strict matching)
    for i, arg_node in enumerate(actual_args):
        actual_type = arg_node.get("data_type", "")
        expected_type = expected_params[i]
        
        if actual_type != expected_type:
            error = {
                "message": f"Argument {i + 1} of function '{func_name}' has type '{actual_type}', expected '{expected_type}'",
                "line": line,
                "column": column,
                "error_type": "param_type_mismatch"
            }
            symbol_table["errors"].append(error)
            return

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
