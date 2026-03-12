# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._traverse_node_src import _traverse_node

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

ErrorRecord = Dict[str, Any]
# ErrorRecord possible fields:
# {
#   "type": str,
#   "message": str,
#   "line": int,
#   "column": int
# }


# === main function ===
def _handle_while(node: AST, symbol_table: SymbolTable) -> None:
    """处理 while 循环语句节点，管理作用域并递归遍历子节点。"""
    children = node.get("children", [])
    
    # 验证 children 数量
    if len(children) < 2:
        _record_error(
            symbol_table,
            "While loop requires at least 2 children: condition and body",
            node.get("line", "?"),
            node.get("column", "?")
        )
        return
    
    # 验证子节点有效性
    condition_node = children[0]
    body_node = children[1]
    
    if condition_node is None or body_node is None:
        _record_error(
            symbol_table,
            "While loop has invalid child node (None)",
            node.get("line", "?"),
            node.get("column", "?")
        )
        return
    
    # 进入新作用域
    old_scope = symbol_table.get("current_scope", 0)
    symbol_table["current_scope"] = old_scope + 1
    symbol_table.setdefault("scope_stack", []).append(old_scope)
    
    # 递归处理条件表达式和循环体
    _traverse_node(condition_node, symbol_table)
    _traverse_node(body_node, symbol_table)
    
    # 退出作用域
    scope_stack = symbol_table.get("scope_stack", [])
    if scope_stack:
        symbol_table["current_scope"] = scope_stack.pop()
    else:
        _record_error(
            symbol_table,
            "Scope stack underflow: attempted to pop from empty stack",
            node.get("line", "?"),
            node.get("column", "?")
        )


# === helper functions ===
def _record_error(
    symbol_table: SymbolTable,
    message: str,
    line: Any,
    column: Any
) -> None:
    """记录错误到符号表的 errors 列表中。"""
    error: ErrorRecord = {
        "type": "error",
        "message": message,
        "line": line if isinstance(line, int) else "?",
        "column": column if isinstance(column, int) else "?"
    }
    symbol_table.setdefault("errors", []).append(error)


# === OOP compatibility layer ===
# Not required for this handler function; omitted.
