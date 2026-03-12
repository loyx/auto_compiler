# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions delegated

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
    处理 assignment 类型节点（赋值语句）。
    
    检查被赋值的变量是否已声明，若未声明则记录错误到 symbol_table["errors"]。
    """
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 确保 variables 字典存在
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 提取变量名：优先从 node["value"] 获取，否则从 children[0] 获取
    var_name = None
    if "value" in node:
        var_name = node["value"]
    elif "children" in node and len(node["children"]) > 0:
        child = node["children"][0]
        if isinstance(child, dict) and "value" in child:
            var_name = child["value"]
    
    # 如果无法提取变量名，直接返回
    if var_name is None:
        return
    
    # 获取行号和列号（用于错误报告）
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 检查变量是否已声明
    variables = symbol_table.get("variables", {})
    var_info = variables.get(var_name)
    
    # 如果变量不存在或 is_declared 为 False，记录错误
    if var_info is None or not var_info.get("is_declared", False):
        error = {
            "line": line,
            "column": column,
            "message": f"use of undeclared variable: {var_name}"
        }
        symbol_table["errors"].append(error)


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node