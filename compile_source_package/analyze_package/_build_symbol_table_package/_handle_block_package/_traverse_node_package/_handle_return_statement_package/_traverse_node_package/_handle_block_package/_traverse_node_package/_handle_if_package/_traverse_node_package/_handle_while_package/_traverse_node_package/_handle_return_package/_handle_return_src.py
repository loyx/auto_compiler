# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", "return", etc.)
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
    处理 return 类型节点（返回语句）。
    
    验证 return 语句是否在函数内，并可选检查返回值类型匹配。
    错误记录到 symbol_table["errors"]。
    """
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 获取节点位置信息
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 检查当前是否在函数内
    current_function = symbol_table.get("current_function")
    if current_function is None:
        # 不在函数内，记录错误
        symbol_table["errors"].append({
            "line": line,
            "column": column,
            "message": "return statement outside of function"
        })
        return
    
    # 在函数内，可选检查返回值类型匹配
    _check_return_type_match(node, symbol_table, line, column)


# === helper functions ===
def _check_return_type_match(node: AST, symbol_table: SymbolTable, line: int, column: int) -> None:
    """
    检查返回值类型是否与函数声明的返回类型匹配。
    
    如果返回值类型不匹配，记录错误到 symbol_table["errors"]。
    """
    # 获取当前函数信息
    functions = symbol_table.get("functions", {})
    current_function = symbol_table.get("current_function")
    
    if current_function not in functions:
        return
    
    func_info = functions[current_function]
    expected_type = func_info.get("return_type")
    
    # 如果没有返回值（return 语句没有值），不需要检查类型
    if "value" not in node and (not node.get("children") or len(node.get("children", [])) == 0):
        # void return，如果函数声明了返回类型则可能有问题
        # 但为了宽松处理，这里不报错
        return
    
    # 获取实际返回值类型
    actual_type = node.get("data_type")
    
    # 如果节点没有直接的 data_type，尝试从 children 获取
    if actual_type is None and node.get("children"):
        first_child = node["children"][0]
        if isinstance(first_child, dict):
            actual_type = first_child.get("data_type")
    
    # 如果无法确定实际类型，跳过检查
    if actual_type is None or expected_type is None:
        return
    
    # 检查类型是否匹配
    if actual_type != expected_type:
        symbol_table["errors"].append({
            "line": line,
            "column": column,
            "message": f"return type mismatch: expected {expected_type}, got {actual_type}"
        })


# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function node
