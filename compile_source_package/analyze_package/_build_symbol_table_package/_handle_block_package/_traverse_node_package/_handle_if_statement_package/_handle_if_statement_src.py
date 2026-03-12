# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# _traverse_node is the parent dispatcher function, import from parent module
# Import _traverse_node lazily to avoid circular import
# It will be imported inside the function when needed

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
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
#   "scope_stack": list            # 作用域栈
# }


# === main function ===
def _handle_if_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 if_statement 类型节点。
    
    递归遍历 condition、then_branch、可选的 else_branch 子节点。
    通过调用 _traverse_node 进行递归处理。
    
    Args:
        node: if_statement 类型的 AST 节点
        symbol_table: 符号表，会被递归遍历时修改
    """
    # Import _traverse_node_src module lazily to avoid circular import
    # Access _traverse_node through module to allow mocking
    from .. import _traverse_node_src
    
    # 提取 condition 子节点（必需）
    condition = node.get("condition")
    if condition is not None:
        _traverse_node_src._traverse_node(condition, symbol_table)
    
    # 提取 then_branch 子节点（必需）
    then_branch = node.get("then_branch")
    if then_branch is not None:
        _traverse_node_src._traverse_node(then_branch, symbol_table)
    
    # 提取 else_branch 子节点（可选）
    else_branch = node.get("else_branch")
    if else_branch is not None:
        _traverse_node_src._traverse_node(else_branch, symbol_table)


# === helper functions ===
# No helper functions needed for this simple traversal logic

# === OOP compatibility layer ===
# Not needed: this is a helper function node, not a framework entry point
