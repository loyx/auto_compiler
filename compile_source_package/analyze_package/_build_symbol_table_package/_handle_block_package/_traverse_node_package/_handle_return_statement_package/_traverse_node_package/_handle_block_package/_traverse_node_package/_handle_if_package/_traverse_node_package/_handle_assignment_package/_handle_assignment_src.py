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
#   "errors": list                 # 错误列表 [{"type": str, "line": int, "column": int, "message": str}]
# }

# === main function ===
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量赋值节点。
    
    处理逻辑：
    1. 获取变量名和位置信息
    2. 检查变量是否已声明
    3. 递归处理赋值表达式
    4. 验证类型匹配
    5. 记录错误到 symbol_table["errors"]
    """
    # 获取位置信息
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 获取变量名（从 children[0] 获取变量名节点）
    var_name_node = node["children"][0] if len(node["children"]) > 0 else None
    if var_name_node is None:
        return
    
    var_name = var_name_node.get("value", "")
    
    # 检查变量是否已声明
    variables = symbol_table.get("variables", {})
    if var_name not in variables or not variables[var_name].get("is_declared", False):
        error = {
            "type": "error",
            "line": line,
            "column": column,
            "message": f"Variable '{var_name}' is not declared"
        }
        symbol_table.setdefault("errors", []).append(error)
        return
    
    # 获取变量类型
    var_info = variables[var_name]
    var_data_type = var_info.get("data_type", "")
    
    # 获取赋值表达式节点（children[1]）
    expr_node = node["children"][1] if len(node["children"]) > 1 else None
    if expr_node is None:
        return
    
    # 递归处理赋值表达式
    _traverse_node(expr_node, symbol_table)
    
    # 获取表达式类型
    expr_data_type = expr_node.get("data_type", "")
    
    # 验证类型匹配
    if var_data_type and expr_data_type and var_data_type != expr_data_type:
        error = {
            "type": "error",
            "line": line,
            "column": column,
            "message": f"Type mismatch: cannot assign '{expr_data_type}' to '{var_data_type}'"
        }
        symbol_table.setdefault("errors", []).append(error)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
