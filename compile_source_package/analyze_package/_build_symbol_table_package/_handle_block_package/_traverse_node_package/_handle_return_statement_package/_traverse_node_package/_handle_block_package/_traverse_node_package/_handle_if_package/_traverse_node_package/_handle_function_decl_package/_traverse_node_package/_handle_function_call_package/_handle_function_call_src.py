# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", "function_decl", "param_list", "param", etc.)
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
    Handle function call node: validate function existence and parameter matching.
    
    Modifies symbol_table["errors"] in place to record any validation errors.
    """
    # Extract function name, actual parameters, and position info
    func_name = node.get("value")
    actual_params = node.get("children", [])
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # Ensure errors list is initialized
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # Get functions dictionary
    functions = symbol_table.get("functions", {})
    
    # Check if function exists in symbol table
    if func_name not in functions:
        symbol_table["errors"].append({
            "type": "undefined_function",
            "message": f"Function '{func_name}' is not defined",
            "line": line,
            "column": column
        })
        return
    
    # Get function definition
    func_def = functions[func_name]
    formal_params = func_def.get("params", [])
    
    # Check parameter count matching
    if len(actual_params) != len(formal_params):
        symbol_table["errors"].append({
            "type": "parameter_count_mismatch",
            "message": f"Function '{func_name}' expects {len(formal_params)} parameters but got {len(actual_params)}",
            "line": line,
            "column": column
        })
        return
    
    # Optional: Check type compatibility for each parameter
    # This is a basic check; can be extended for more sophisticated type system
    for i, (actual_param, formal_param) in enumerate(zip(actual_params, formal_params)):
        actual_type = actual_param.get("data_type")
        formal_type = formal_param.get("data_type")
        
        if actual_type and formal_type and actual_type != formal_type:
            symbol_table["errors"].append({
                "type": "type_mismatch",
                "message": f"Parameter {i+1} type mismatch: expected '{formal_type}', got '{actual_type}'",
                "line": actual_param.get("line", line),
                "column": actual_param.get("column", column)
            })

# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# Not needed for this function node