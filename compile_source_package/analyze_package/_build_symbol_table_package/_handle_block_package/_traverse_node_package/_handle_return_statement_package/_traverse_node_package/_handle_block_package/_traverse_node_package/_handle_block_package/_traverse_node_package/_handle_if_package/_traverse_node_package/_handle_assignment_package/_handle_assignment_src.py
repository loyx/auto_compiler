# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple logic

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
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 assignment 类型节点（赋值语句）。
    
    检查左侧变量是否已声明，若未声明则记录错误到符号表。
    """
    # 提取行列号
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 提取左侧变量名
    var_name = _extract_left_variable(node)
    
    if not var_name:
        return
    
    # 检查变量是否在符号表中存在
    variables = symbol_table.get("variables", {})
    
    if var_name not in variables:
        # 记录未声明变量错误
        error = {
            "type": "error",
            "message": f"Undefined variable: {var_name}",
            "line": line,
            "column": column
        }
        symbol_table.setdefault("errors", []).append(error)
    else:
        # 变量已存在，可选择更新使用信息
        variables[var_name]["is_used"] = True

# === helper functions ===
def _extract_left_variable(node: AST) -> str:
    """
    从 assignment 节点中提取左侧变量名。
    
    尝试从 "value" 字段或 "children"[0] 中获取变量名。
    """
    # 优先尝试从 "value" 字段获取
    value = node.get("value")
    if isinstance(value, str):
        return value
    
    # 尝试从 children[0] 获取
    children = node.get("children", [])
    if children and len(children) > 0:
        left_node = children[0]
        if isinstance(left_node, dict):
            # 如果 left_node 是标识符节点，从 "value" 获取
            return left_node.get("value", "")
        elif isinstance(left_node, str):
            return left_node
    
    return ""

# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function node
