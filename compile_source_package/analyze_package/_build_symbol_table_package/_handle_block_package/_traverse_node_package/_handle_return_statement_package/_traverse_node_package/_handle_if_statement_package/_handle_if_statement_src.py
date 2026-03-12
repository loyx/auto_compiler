# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this handler

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "if_statement")
#   "children": list,        # 子节点列表 [condition, then_branch, else_branch?]
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
    """
    Handle if_statement type AST node.
    
    Checks if the condition expression is of int type.
    Records error to symbol_table["errors"] if type mismatch.
    Does not traverse children (handled by parent _traverse_node).
    """
    children = node.get("children", [])
    line = node.get("line", "?")
    column = node.get("column", "?")
    
    # Check condition expression type (children[0])
    if len(children) >= 1:
        condition_node = children[0]
        condition_type = condition_node.get("data_type")
        
        # Condition must be int type (0 = false, non-zero = true)
        if condition_type != "int":
            error_msg = f"Error: Condition expression must be int type at line {line}, column {column}"
            symbol_table.setdefault("errors", []).append(error_msg)


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this handler function
