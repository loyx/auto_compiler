# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "name": str,
#   "params": list,
#   "body": AST,
#   "return_type": str,
#   "line": int,
#   "column": int,
#   "condition": AST,
#   "then_branch": AST,
#   "else_branch": AST (optional)
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list
# }

# === main function ===
def _handle_if_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 if 语句节点，递归遍历条件表达式和分支语句。
    
    处理逻辑：
    1. 从 node 中提取 "condition" 字段作为条件表达式
    2. 从 node 中提取 "then_branch" 字段作为 then 分支
    3. 从 node 中提取 "else_branch" 字段（可选，可为 None）
    4. 递归调用 _traverse_node 处理 condition
    5. 递归调用 _traverse_node 处理 then_branch
    6. 如果 else_branch 存在（不为 None），递归调用 _traverse_node 处理 else_branch
    """
    condition = node.get("condition")
    then_branch = node.get("then_branch")
    else_branch = node.get("else_branch")
    
    if condition is not None:
        _traverse_node(condition, symbol_table)
    
    if then_branch is not None:
        _traverse_node(then_branch, symbol_table)
    
    if else_branch is not None:
        _traverse_node(else_branch, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node