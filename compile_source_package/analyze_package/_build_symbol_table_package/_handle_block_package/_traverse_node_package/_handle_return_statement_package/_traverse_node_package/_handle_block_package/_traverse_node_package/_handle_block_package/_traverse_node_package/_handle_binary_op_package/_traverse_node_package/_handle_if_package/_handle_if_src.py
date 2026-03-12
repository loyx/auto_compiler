# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "binary_op", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (如操作符、变量名、字面量值等)
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
    """处理 if 条件语句节点。遍历条件表达式、then 分支、可选 else 分支。"""
    children = node.get("children", [])
    
    if not children:
        line = node.get("line", "unknown")
        column = node.get("column", "unknown")
        symbol_table.setdefault("errors", []).append(
            f"if 语句缺少子节点 at line {line}, column {column}"
        )
        return
    
    if len(children) < 2:
        line = node.get("line", "unknown")
        column = node.get("column", "unknown")
        symbol_table.setdefault("errors", []).append(
            f"if 语句子节点不足 (需要至少 2 个：条件 + then 分支) at line {line}, column {column}"
        )
        return
    
    condition_node = children[0]
    then_branch = children[1]
    
    _traverse_node(condition_node, symbol_table)
    _traverse_node(then_branch, symbol_table)
    
    if len(children) >= 3:
        else_branch = children[2]
        _traverse_node(else_branch, symbol_table)

# === helper functions ===

# === OOP compatibility layer ===
