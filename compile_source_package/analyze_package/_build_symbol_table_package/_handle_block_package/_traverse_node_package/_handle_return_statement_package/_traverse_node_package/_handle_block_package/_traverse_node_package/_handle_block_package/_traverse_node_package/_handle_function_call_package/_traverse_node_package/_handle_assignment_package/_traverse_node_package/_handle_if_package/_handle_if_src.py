# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "assignment", "var_decl", "if", "while", "block", "binary_op", "literal", "identifier", "expression", etc.)
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
def _handle_if(node: AST, symbol_table: SymbolTable) -> None:
    """处理 if 语句节点，遍历条件表达式和分支语句，管理作用域层级。"""
    # 提取条件表达式和分支节点
    condition = node.get("condition")
    then_branch = node.get("then_branch")
    else_branch = node.get("else_branch")
    children = node.get("children", [])

    # 遍历条件表达式的子节点
    if condition is not None:
        _traverse_node(condition, symbol_table)

    # 处理 then 分支：进入新作用域
    if then_branch is not None:
        # 保存当前作用域层级
        old_scope = symbol_table.get("current_scope", 0)
        symbol_table["current_scope"] = old_scope + 1

        # 遍历 then 分支
        _traverse_node(then_branch, symbol_table)

        # 恢复作用域层级
        symbol_table["current_scope"] = old_scope

    # 处理 else 分支：进入新作用域
    if else_branch is not None:
        old_scope = symbol_table.get("current_scope", 0)
        symbol_table["current_scope"] = old_scope + 1

        # 遍历 else 分支
        _traverse_node(else_branch, symbol_table)

        # 恢复作用域层级
        symbol_table["current_scope"] = old_scope

    # 如果没有明确的 condition/then/else 字段，遍历所有 children
    if not condition and not then_branch and not else_branch:
        for child in children:
            _traverse_node(child, symbol_table)


# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node