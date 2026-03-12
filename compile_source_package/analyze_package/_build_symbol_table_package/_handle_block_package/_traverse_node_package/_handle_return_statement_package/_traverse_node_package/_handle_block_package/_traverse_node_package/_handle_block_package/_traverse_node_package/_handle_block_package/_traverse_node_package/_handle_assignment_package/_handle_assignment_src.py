# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

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
    """处理赋值节点：验证变量已声明并遍历赋值表达式。"""
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 确保 variables 字典存在
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 获取变量名和位置信息
    var_name = node.get("value", "")
    line = node.get("line", -1)
    column = node.get("column", -1)
    
    # 检查变量是否已声明
    if var_name not in symbol_table["variables"]:
        # 记录错误：变量未声明
        error_entry = {
            "type": "error",
            "message": f"Undefined variable: {var_name}",
            "line": line,
            "column": column
        }
        symbol_table["errors"].append(error_entry)
        return
    
    # 变量已声明，遍历赋值表达式（children[0]）
    children = node.get("children", [])
    if children:
        _traverse_node(children[0], symbol_table)

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# No OOP wrapper needed for this semantic analysis function
