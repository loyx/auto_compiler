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
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 'assignment' 类型节点。验证赋值目标变量已声明且类型匹配。
    
    处理逻辑：
    1. 从 node["children"] 中提取左侧（目标标识符）和右侧（表达式）
    2. 检查左侧标识符对应的变量是否已声明
    3. 如果已声明，验证右侧表达式类型与变量类型匹配
    4. 递归处理右侧表达式
    5. 未声明或类型不匹配时记录错误到 symbol_table["errors"]
    """
    children = node.get("children", [])
    if len(children) < 2:
        return
    
    target_node = children[0]
    expression_node = children[1]
    
    # 获取目标变量名
    if target_node.get("type") != "identifier":
        return
    
    var_name = target_node.get("value")
    if not var_name:
        return
    
    line = node.get("line", "?")
    column = node.get("column", "?")
    
    # 检查变量是否已声明
    variables = symbol_table.get("variables", {})
    if var_name not in variables:
        error = {
            "message": f"Variable '{var_name}' is not declared",
            "line": line,
            "column": column,
            "type": "undeclared_variable"
        }
        symbol_table.setdefault("errors", []).append(error)
        return
    
    # 获取变量声明的类型
    var_info = variables[var_name]
    declared_type = var_info.get("data_type")
    
    # 递归处理右侧表达式
    _traverse_node(expression_node, symbol_table)
    
    # 获取表达式的类型
    expr_type = expression_node.get("data_type")
    
    # 类型检查
    if declared_type and expr_type and declared_type != expr_type:
        error = {
            "message": f"Type mismatch: cannot assign '{expr_type}' to '{declared_type}' variable '{var_name}'",
            "line": line,
            "column": column,
            "type": "type_mismatch"
        }
        symbol_table.setdefault("errors", []).append(error)

# === helper functions ===

# === OOP compatibility layer ===
