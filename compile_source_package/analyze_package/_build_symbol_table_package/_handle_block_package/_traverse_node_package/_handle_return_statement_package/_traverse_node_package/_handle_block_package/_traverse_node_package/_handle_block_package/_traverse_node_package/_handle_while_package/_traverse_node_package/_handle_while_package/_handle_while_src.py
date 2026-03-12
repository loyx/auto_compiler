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
def _handle_while(node: AST, symbol_table: SymbolTable) -> None:
    """处理 while 循环节点。递归遍历条件和循环体，验证变量使用。"""
    if node is None:
        return

    children = node.get("children", [])
    if len(children) < 2:
        return

    line = node.get("line", 0)
    column = node.get("column", 0)

    condition_node = children[0]
    body_node = children[1]

    # 递归遍历条件表达式和循环体
    _traverse_node(condition_node, symbol_table)
    _traverse_node(body_node, symbol_table)


# === helper functions ===
def _check_variable_usage(node: AST, symbol_table: SymbolTable, context: str) -> None:
    """检查节点中的变量是否已声明。"""
    if node is None:
        return

    node_type = node.get("type", "")
    line = node.get("line", 0)

    if node_type == "identifier":
        var_name = node.get("value", "")
        variables = symbol_table.get("variables", {})
        if var_name not in variables:
            error_msg = f"Line {line}: Variable '{var_name}' used in {context} is not declared"
            errors = symbol_table.get("errors", [])
            if errors is not None:
                errors.append(error_msg)


# === OOP compatibility layer ===
