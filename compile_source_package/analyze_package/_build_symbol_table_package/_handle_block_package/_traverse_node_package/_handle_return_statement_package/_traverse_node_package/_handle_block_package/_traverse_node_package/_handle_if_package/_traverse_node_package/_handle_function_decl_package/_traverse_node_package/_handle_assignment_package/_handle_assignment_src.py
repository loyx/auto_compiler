# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple validation logic

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", "function_decl", "param_list", "param", etc.)
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
    处理赋值语句节点：检查变量是否已声明，验证类型兼容性。
    
    副作用：可能更新变量值，或在 symbol_table['errors'] 中记录错误。
    """
    # 确保 errors 列表已初始化
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 从 node 中提取信息
    var_name = node.get("value")
    assign_type = node.get("data_type")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 检查 variables 字典是否存在
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 检查变量是否已声明
    if var_name not in symbol_table["variables"]:
        error_msg = f"Error: Undeclared variable '{var_name}' at line {line}, column {column}"
        symbol_table["errors"].append(error_msg)
        return
    
    # 变量已存在，检查类型兼容性
    var_info = symbol_table["variables"][var_name]
    declared_type = var_info.get("data_type")
    
    # 类型兼容性规则：int 只能赋值给 int，char 只能赋值给 char
    if declared_type != assign_type:
        error_msg = f"Error: Type mismatch for variable '{var_name}' at line {line}, column {column}. Expected '{declared_type}', got '{assign_type}'"
        symbol_table["errors"].append(error_msg)


# === helper functions ===
# No helper functions needed - logic is simple and self-contained

# === OOP compatibility layer ===
# Not needed - this is a helper function for semantic analysis, not a framework entry point