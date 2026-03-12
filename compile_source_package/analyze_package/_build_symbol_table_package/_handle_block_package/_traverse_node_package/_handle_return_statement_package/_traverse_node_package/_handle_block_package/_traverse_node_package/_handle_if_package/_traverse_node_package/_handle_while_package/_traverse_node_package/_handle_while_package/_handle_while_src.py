# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._traverse_node import _traverse_node

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
def _handle_while(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 while 类型节点（循环语句）。
    
    验证节点结构，遍历条件表达式和循环体块，收集错误到 symbol_table。
    """
    # 防御性初始化 errors 列表
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 获取行列号（默认值为 0）
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 检查 children 是否存在且包含 2 个子节点
    children = node.get("children", [])
    if len(children) < 2:
        error_entry = {
            "line": line,
            "column": column,
            "message": "while statement requires condition and body",
        }
        symbol_table["errors"].append(error_entry)
        return
    
    # 遍历条件表达式（children[0]）
    _traverse_node(children[0], symbol_table)
    
    # 遍历循环体块（children[1]）
    _traverse_node(children[1], symbol_table)


# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
