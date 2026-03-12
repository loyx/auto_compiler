# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block" 等)
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
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _handle_if_statement(node: AST, symbol_table: SymbolTable) -> None:
    """处理 if_statement 类型节点。递归遍历条件表达式和分支 block。"""
    # 验证必填字段
    if "condition" not in node:
        symbol_table["errors"].append({
            "message": "if_statement missing 'condition' field",
            "line": node.get("line", "unknown"),
            "column": node.get("column", "unknown"),
            "type": "missing_field"
        })
        return
    
    if "then_branch" not in node:
        symbol_table["errors"].append({
            "message": "if_statement missing 'then_branch' field",
            "line": node.get("line", "unknown"),
            "column": node.get("column", "unknown"),
            "type": "missing_field"
        })
        return
    
    # 递归处理条件表达式
    _traverse_node(node["condition"], symbol_table)
    
    # 递归处理 then 分支
    _traverse_node(node["then_branch"], symbol_table)
    
    # 递归处理 else 分支（如果存在）
    else_branch = node.get("else_branch")
    if else_branch is not None:
        _traverse_node(else_branch, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node