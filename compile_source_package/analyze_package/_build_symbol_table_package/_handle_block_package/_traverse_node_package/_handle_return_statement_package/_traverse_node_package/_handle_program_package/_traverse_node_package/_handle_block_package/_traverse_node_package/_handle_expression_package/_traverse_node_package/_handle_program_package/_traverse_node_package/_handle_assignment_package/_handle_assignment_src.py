# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "data_type": str,
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理赋值语句节点，验证左侧变量是否已声明。
    
    处理逻辑：
    1. 从 node 的 children 中提取左侧标识符（identifier 节点）
    2. 获取标识符名称
    3. 检查该变量是否在 symbol_table["variables"] 中已声明
    4. 如果未声明，记录错误到 symbol_table["errors"]
    """
    # 从 children 中提取左侧标识符
    identifier_name = _extract_identifier_name(node)
    
    if identifier_name is None:
        return
    
    # 检查变量是否已声明
    variables = symbol_table.get("variables", {})
    
    if identifier_name not in variables:
        # 记录未声明变量错误
        error = {
            "type": "undefined_variable",
            "message": f"变量未声明：{identifier_name}",
            "line": node.get("line"),
            "column": node.get("column")
        }
        errors = symbol_table.get("errors", [])
        errors.append(error)
        symbol_table["errors"] = errors

# === helper functions ===
def _extract_identifier_name(node: AST) -> str:
    """从 assignment 节点的 children 中提取左侧标识符名称。"""
    children = node.get("children", [])
    
    for child in children:
        if isinstance(child, dict) and child.get("type") == "identifier":
            return child.get("value")
    
    return None

# === OOP compatibility layer ===
# Not needed for this helper function node
