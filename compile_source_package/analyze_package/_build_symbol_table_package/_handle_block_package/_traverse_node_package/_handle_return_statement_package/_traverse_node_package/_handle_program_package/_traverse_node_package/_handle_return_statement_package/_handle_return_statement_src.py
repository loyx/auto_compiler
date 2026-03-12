# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block" 等)
#   "children": list,        # 子节点列表
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
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }


# === main function ===
def _handle_return_statement(node: AST, symbol_table: SymbolTable) -> None:
    """处理 return_statement 类型节点，验证返回值类型与当前函数返回类型是否匹配。"""
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 获取当前函数名
    current_function_name = symbol_table.get("current_function")
    
    # 检查是否在函数外使用 return
    if current_function_name is None:
        symbol_table["errors"].append({
            "message": "Return statement outside function",
            "line": node.get("line", 0),
            "column": node.get("column", 0),
            "type": "return_outside_function"
        })
        return
    
    # 获取返回值表达式
    expression_node = node.get("expression")
    
    # 获取当前函数的返回类型
    func_info = symbol_table.get("functions", {}).get(current_function_name, {})
    expected_return_type = func_info.get("return_type")
    
    # 处理无返回值的 return 语句
    if expression_node is None:
        # void return，检查函数返回类型是否为 void 或无类型
        if expected_return_type is not None and expected_return_type != "void":
            symbol_table["errors"].append({
                "message": f"Return type mismatch: expected '{expected_return_type}' but got 'void'",
                "line": node.get("line", 0),
                "column": node.get("column", 0),
                "type": "return_type_mismatch"
            })
        return
    
    # 递归处理返回值表达式
    _traverse_node(expression_node, symbol_table)
    
    # 获取表达式的类型
    actual_return_type = expression_node.get("data_type")
    
    # 验证返回类型是否匹配
    if expected_return_type is not None and actual_return_type is not None:
        if expected_return_type != actual_return_type:
            symbol_table["errors"].append({
                "message": f"Return type mismatch: expected '{expected_return_type}' but got '{actual_return_type}'",
                "line": node.get("line", 0),
                "column": node.get("column", 0),
                "type": "return_type_mismatch"
            })


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
