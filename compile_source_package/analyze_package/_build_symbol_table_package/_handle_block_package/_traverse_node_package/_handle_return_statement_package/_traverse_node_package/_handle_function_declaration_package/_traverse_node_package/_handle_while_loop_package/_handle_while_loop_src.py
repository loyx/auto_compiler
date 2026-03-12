# === std / third-party imports ===
from typing import Any, Dict, Callable, Optional, List

# === sub function imports ===
# No child functions needed for this handler

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (e.g., "while_loop", "binary_op", "identifier")
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值 (e.g., operator symbol, literal value)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],    # 变量符号表
#   "functions": Dict[str, Dict],    # 函数符号表
#   "current_scope": int,            # 当前作用域层级
#   "scope_stack": list,             # 作用域栈
#   "current_function": str,         # 当前函数名
#   "errors": list                   # 错误列表
# }

# === main function ===
def _handle_while_loop(
    node: AST,
    symbol_table: SymbolTable,
    traverse_fn: Optional[Callable[[AST, SymbolTable], None]] = None
) -> None:
    """
    Handle while_loop AST nodes with proper scope management.
    
    Processes condition and loop body by delegating traversal to parent via callback.
    Manages scope level for loop body (increment before, decrement after).
    
    Args:
        node: AST node of type "while_loop"
        symbol_table: Symbol table for scope management (modified in-place)
        traverse_fn: Callback function for traversing child nodes
    
    Side effects:
        - Modifies symbol_table["current_scope"] during body traversal
        - May append errors to symbol_table["errors"]
        - Traverses condition and body children via traverse_fn
    """
    children: List[AST] = node.get("children", [])
    
    # Validate node structure
    if len(children) < 2:
        symbol_table["errors"].append({
            "type": "AST_ERROR",
            "message": "while_loop node must have at least 2 children (condition, body)",
            "line": node.get("line", 0),
            "column": node.get("column", 0)
        })
        return
    
    condition_node: AST = children[0]
    body_node: AST = children[1]
    
    # Traverse condition expression
    if traverse_fn:
        traverse_fn(condition_node, symbol_table)
    
    # Handle loop body with scope management
    if body_node.get("type") == "block":
        # Increment scope before entering loop body
        symbol_table["current_scope"] = symbol_table.get("current_scope", 0) + 1
        symbol_table["scope_stack"].append(symbol_table["current_scope"])
        
        # Traverse body children
        body_children: List[AST] = body_node.get("children", [])
        if traverse_fn:
            for child in body_children:
                traverse_fn(child, symbol_table)
        
        # Decrement scope after leaving loop body
        symbol_table["scope_stack"].pop()
        symbol_table["current_scope"] = symbol_table.get("current_scope", 1) - 1
    else:
        # Body is not a block, traverse directly
        if traverse_fn:
            traverse_fn(body_node, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node