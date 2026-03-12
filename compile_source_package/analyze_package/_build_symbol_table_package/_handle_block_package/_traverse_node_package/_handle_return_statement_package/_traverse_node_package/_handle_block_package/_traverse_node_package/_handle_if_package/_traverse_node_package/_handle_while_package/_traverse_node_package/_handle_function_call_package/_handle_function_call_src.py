# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions required for this module

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", etc.)
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
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle function_call type AST nodes.
    
    Validates that the called function is declared in the symbol table.
    Records errors for undeclared function calls.
    
    Args:
        node: AST node with type "function_call", value contains function name
        symbol_table: Symbol table for tracking declared functions and errors
    
    Side effects:
        - May initialize symbol_table["errors"] if not present
        - May initialize symbol_table["functions"] if not present
        - May append error records to symbol_table["errors"]
    """
    # Ensure errors list exists
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # Ensure functions dict exists
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    
    # Extract function name from node
    func_name = node.get("value")
    
    # Get line and column for error reporting
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # Check if function is declared
    if func_name not in symbol_table["functions"]:
        # Record error for undeclared function
        error_record = {
            "line": line,
            "column": column,
            "message": f"call to undeclared function: {func_name}"
        }
        symbol_table["errors"].append(error_record)
    
    # Note: Parameter type checking is optional and not implemented here


# === helper functions ===
# No helper functions required for this module

# === OOP compatibility layer ===
# No OOP wrapper required for this function node
