# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Import parent's _traverse_node for recursive traversal
from ..traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
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
#   "scope_stack": list,           # 作用域栈 (存储旧 scope 值)
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }


# === main function ===
def _handle_if(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle if-statement node during AST traversal.
    
    Manages scope for then/else branches, processes condition expression,
    and collects semantic errors. Does not throw exceptions.
    """
    # Handle None node silently
    if node is None:
        return
    
    # Initialize errors list if not exists
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # Extract node components
    condition = node.get("condition")
    then_branch = node.get("then_branch")
    else_branch = node.get("else_branch")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # Enter new scope for if statement
    symbol_table["scope_stack"].append(symbol_table["current_scope"])
    symbol_table["current_scope"] += 1
    
    # Process condition expression
    if condition is not None:
        _traverse_node(condition, symbol_table)
    
    # Process then branch (in same scope as if condition)
    if then_branch is not None:
        # Enter new scope for then branch body
        symbol_table["scope_stack"].append(symbol_table["current_scope"])
        symbol_table["current_scope"] += 1
        
        _traverse_node(then_branch, symbol_table)
        
        # Exit then branch scope
        symbol_table["current_scope"] = symbol_table["scope_stack"].pop()
    
    # Process else branch if exists
    if else_branch is not None:
        # Enter new scope for else branch body
        symbol_table["scope_stack"].append(symbol_table["current_scope"])
        symbol_table["current_scope"] += 1
        
        _traverse_node(else_branch, symbol_table)
        
        # Exit else branch scope
        symbol_table["current_scope"] = symbol_table["scope_stack"].pop()
    
    # Exit if statement scope
    symbol_table["current_scope"] = symbol_table["scope_stack"].pop()


# === helper functions ===
# No helper functions needed for this simple handler

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
