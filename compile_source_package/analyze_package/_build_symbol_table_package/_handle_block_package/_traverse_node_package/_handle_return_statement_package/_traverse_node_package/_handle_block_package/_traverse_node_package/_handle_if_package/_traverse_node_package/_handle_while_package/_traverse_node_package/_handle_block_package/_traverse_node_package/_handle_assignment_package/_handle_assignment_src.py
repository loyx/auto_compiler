# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple validation logic

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
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理赋值语句节点。验证变量是否已声明，如果未声明则记录错误。
    可选：验证赋值类型与声明类型是否匹配。
    """
    # 1. 从 node 中提取信息
    var_name = node["value"]
    data_type = node.get("data_type")
    line = node["line"]
    column = node["column"]
    
    # 2. 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 3. 检查变量是否已声明
    variables = symbol_table.get("variables", {})
    var_info = variables.get(var_name)
    
    if var_info is None or not var_info.get("is_declared", False):
        # 变量未声明，记录错误
        symbol_table["errors"].append({
            "type": "undeclared_variable",
            "message": f"Variable '{var_name}' used before declaration",
            "line": line,
            "column": column
        })
        return
    
    # 4. 可选：类型匹配检查（如果 data_type 不为 None）
    if data_type is not None:
        declared_type = var_info.get("data_type")
        if declared_type is not None and declared_type != data_type:
            # 类型不匹配，记录错误
            symbol_table["errors"].append({
                "type": "type_mismatch",
                "message": f"Type mismatch for variable '{var_name}'",
                "line": line,
                "column": column
            })

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed for this semantic analysis function node