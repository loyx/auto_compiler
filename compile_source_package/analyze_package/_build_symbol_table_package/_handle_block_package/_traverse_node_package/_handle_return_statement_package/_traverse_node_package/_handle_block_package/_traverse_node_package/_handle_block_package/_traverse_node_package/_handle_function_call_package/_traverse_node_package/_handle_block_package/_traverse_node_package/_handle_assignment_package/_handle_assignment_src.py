# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", etc.)
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
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理赋值节点：验证变量已声明，检查类型兼容性。
    
    输入：assignment 类型的 AST 节点和符号表
    处理：查找变量，验证存在性和类型
    副作用：可能记录类型错误到 symbol_table['errors']
    """
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 从 children 中提取左值和右值
    children = node.get("children", [])
    if len(children) < 2:
        return
    
    left_value = children[0]  # identifier node
    right_value = children[1]  # expression node
    
    # 获取左值变量名
    var_name = left_value.get("value")
    if not var_name:
        return
    
    line = left_value.get("line", node.get("line", 0))
    column = left_value.get("column", node.get("column", 0))
    
    # 在符号表中查找变量
    variables = symbol_table.get("variables", {})
    var_info = variables.get(var_name)
    
    # 变量未声明
    if var_info is None or not var_info.get("is_declared", False):
        error = {
            "type": "undeclared_variable",
            "message": f"Variable '{var_name}' is not declared",
            "line": line,
            "column": column,
            "variable": var_name
        }
        symbol_table["errors"].append(error)
        return
    
    # 变量已声明，检查类型兼容性
    declared_type = var_info.get("data_type")
    expr_type = right_value.get("data_type")
    
    # 如果右值有明确的类型信息
    if expr_type and declared_type:
        if declared_type != expr_type:
            error = {
                "type": "type_mismatch",
                "message": f"Type mismatch: cannot assign {expr_type} to {declared_type}",
                "line": line,
                "column": column,
                "variable": var_name,
                "expected_type": declared_type,
                "actual_type": expr_type
            }
            symbol_table["errors"].append(error)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
