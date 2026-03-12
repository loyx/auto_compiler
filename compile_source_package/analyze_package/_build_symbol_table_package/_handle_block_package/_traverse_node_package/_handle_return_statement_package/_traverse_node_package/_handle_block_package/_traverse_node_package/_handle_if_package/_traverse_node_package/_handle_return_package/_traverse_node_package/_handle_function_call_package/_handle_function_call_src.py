# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple lookup operation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("function_call")
#   "function_name": str,    # 被调用的函数名
#   "arguments": list,       # 参数列表 (可选)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> str:
    """
    Handle function call AST nodes by looking up function definitions in the symbol table.
    
    Returns the return_type of the called function, or 'void' if not found.
    May add error messages to symbol_table['errors'] if function is undefined.
    """
    function_name = node.get("function_name", "")
    line = node.get("line", 0)
    
    functions_dict = symbol_table.get("functions", {})
    func_def = functions_dict.get(function_name)
    
    if func_def is not None:
        return func_def.get("return_type", "void")
    else:
        _add_undefined_function_error(symbol_table, function_name, line)
        return "void"

# === helper functions ===
def _add_undefined_function_error(symbol_table: SymbolTable, function_name: str, line: int) -> None:
    """
    Add an 'undefined function' error to the symbol table's errors list.
    
    Creates the errors list if it doesn't exist.
    """
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    error_message = f"undefined function '{function_name}' at line {line}"
    symbol_table["errors"].append(error_message)

# === OOP compatibility layer ===
# Not needed: This is a helper function node, not a framework entry point
