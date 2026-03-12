# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple validation logic

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
    处理赋值节点。
    
    验证变量是否已声明，如果未声明则记录错误到符号表。
    不抛出异常，只原地修改 symbol_table["errors"]。
    """
    # 1. 从 node 中提取变量名、行号、列号
    var_name = node.get("value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 2. 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 3. 检查变量是否在符号表中存在
    variables = symbol_table.get("variables", {})
    
    if var_name not in variables:
        # 4. 变量不存在，记录错误
        error_msg = f"未声明变量赋值: '{var_name}'"
        error_info = {
            "type": "undeclared_variable_assignment",
            "message": error_msg,
            "variable": var_name,
            "line": line,
            "column": column
        }
        symbol_table["errors"].append(error_info)
    else:
        # 5. 变量存在，可以选择更新变量信息（标记为已使用）
        # 这里可以选择更新变量的使用信息，但根据需求不是必须的
        pass

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function