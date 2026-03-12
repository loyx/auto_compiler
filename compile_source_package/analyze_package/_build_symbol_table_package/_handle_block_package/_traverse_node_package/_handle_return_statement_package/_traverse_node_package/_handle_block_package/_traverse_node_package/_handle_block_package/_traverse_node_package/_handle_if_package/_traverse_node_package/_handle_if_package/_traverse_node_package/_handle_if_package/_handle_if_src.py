# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._process_node_package._process_node_src import _process_node

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
def _handle_if(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 if 控制流节点。
    遍历条件表达式、then 分支、可选的 else 分支。
    管理作用域栈。
    """
    children = node.get("children", [])
    
    # 验证 children 数量
    if len(children) < 2:
        symbol_table["errors"].append({
            "type": "invalid_if",
            "message": "if node must have at least condition and then-branch",
            "line": node.get("line"),
            "column": node.get("column")
        })
        return
    
    # 进入新作用域（if 语句块）
    _push_scope(symbol_table)
    
    try:
        # children[0]: 条件表达式
        _process_node(children[0], symbol_table)
        
        # children[1]: then 分支（block）
        _process_node(children[1], symbol_table)
        
        # children[2]: else 分支（可选）
        if len(children) >= 3:
            _process_node(children[2], symbol_table)
    
    finally:
        # 退出作用域
        _pop_scope(symbol_table)

# === helper functions ===
def _push_scope(symbol_table: SymbolTable) -> None:
    """进入新作用域，push 到 scope_stack。"""
    current_scope = symbol_table.get("current_scope", 0)
    scope_stack = symbol_table.get("scope_stack", [])
    
    scope_stack.append(current_scope)
    symbol_table["scope_stack"] = scope_stack
    symbol_table["current_scope"] = current_scope + 1

def _pop_scope(symbol_table: SymbolTable) -> None:
    """退出当前作用域，pop scope_stack。"""
    scope_stack = symbol_table.get("scope_stack", [])
    
    if scope_stack:
        previous_scope = scope_stack.pop()
        symbol_table["scope_stack"] = scope_stack
        symbol_table["current_scope"] = previous_scope
    else:
        symbol_table["errors"].append({
            "type": "scope_error",
            "message": "attempted to pop empty scope stack",
            "line": None,
            "column": None
        })

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a helper function node
