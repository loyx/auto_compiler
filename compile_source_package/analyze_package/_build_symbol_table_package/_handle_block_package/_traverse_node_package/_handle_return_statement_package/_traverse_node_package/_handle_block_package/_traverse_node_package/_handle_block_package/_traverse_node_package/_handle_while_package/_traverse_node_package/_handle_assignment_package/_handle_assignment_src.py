# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# _traverse_node is the parent orchestrator function that calls this handler
# We declare it here to satisfy the linter and enable recursive traversal
from ._traverse_node_package._traverse_node_src import _traverse_node

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
#   "errors": list                 # 错误列表 (已初始化为 list)
# }

# === main function ===
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle assignment node: validate variable is declared, then traverse expression.
    
    Args:
        node: AST node with type="assignment", children[0]=var_name (str), children[1]=expr (AST)
        symbol_table: Symbol table containing variables dict and errors list
    
    Side effects:
        - May append error to symbol_table["errors"] if variable is undeclared
        - Recursively traverses expression via _traverse_node
    """
    var_name = node["children"][0]
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # Check if variable is declared
    variables = symbol_table.get("variables", {})
    var_entry = variables.get(var_name)
    
    if var_entry is None or not var_entry.get("is_declared", False):
        # Variable not declared, record error
        symbol_table["errors"].append({
            "type": "undeclared_variable",
            "var_name": var_name,
            "message": f"Variable '{var_name}' is not declared before assignment",
            "line": line,
            "column": column
        })
    else:
        # Variable is declared, recursively traverse the expression
        expr_node = node["children"][1]
        _traverse_node(expr_node, symbol_table)

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed for this function node
