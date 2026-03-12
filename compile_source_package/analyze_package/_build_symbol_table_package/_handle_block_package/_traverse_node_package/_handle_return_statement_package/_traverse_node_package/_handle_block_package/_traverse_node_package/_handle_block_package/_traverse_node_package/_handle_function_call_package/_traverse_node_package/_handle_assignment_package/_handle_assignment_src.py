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
    """
    处理 assignment 节点：验证左侧变量已声明，未声明则记录错误，
    然后递归遍历右侧表达式。
    """
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []

    # 从 children 中提取左侧标识符和右侧表达式
    children = node.get("children", [])
    if len(children) < 1:
        return  # 无左侧变量，跳过

    identifier_node = children[0]
    var_name = identifier_node.get("value")

    # 检查变量是否已声明
    variables = symbol_table.get("variables", {})
    if var_name not in variables or not variables[var_name].get("is_declared", False):
        # 记录未声明变量错误
        error = {
            "error_type": "undeclared_variable",
            "message": f"Variable '{var_name}' is not declared",
            "line": node.get("line", 0),
            "column": node.get("column", 0),
            "var_name": var_name
        }
        symbol_table["errors"].append(error)
        return  # 变量未声明，不继续遍历表达式

    # 变量已声明，遍历右侧表达式（如果有）
    if len(children) >= 2:
        expression_node = children[1]
        _traverse_node(expression_node, symbol_table)


# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed for this function node
