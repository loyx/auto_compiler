# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No direct child functions; _verify_node uses lazy import due to circular dependency

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("function_call")
#   "name": str,             # 函数名
#   "args": list,            # 参数列表（AST 节点列表）
#   "data_type": str,        # 返回类型
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,
# }

ContextStack = list
# ContextStack possible fields:
# [
#   {"type": "function", "name": str, "return_type": str},
#   {"type": "loop", "stmt_type": "while"|"for"}
# ]

# === main function ===
def _verify_function_call(node: dict, symbol_table: dict, context_stack: list, filename: str) -> None:
    """
    Verify a function call node.
    
    Checks:
    1. Function is declared in symbol_table
    2. Argument count matches parameter count
    3. Each argument type matches corresponding parameter type
    4. Sets node['data_type'] to function return type
    """
    # Lazy import to avoid circular dependency
    from .._verify_node_src import _verify_node
    
    func_name = node.get('name', '')
    line = node.get('line', 0)
    column = node.get('column', 0)
    args = node.get('args', [])
    
    # Check if function is declared
    functions = symbol_table.get('functions', {})
    if func_name not in functions:
        raise ValueError(
            f"{filename}:{line}:{column}: error: function '{func_name}' was not declared"
        )
    
    func_info = functions[func_name]
    params = func_info.get('params', [])
    return_type = func_info.get('return_type', '')
    
    # Check argument count
    if len(args) != len(params):
        raise ValueError(
            f"{filename}:{line}:{column}: error: function '{func_name}' expects {len(params)} arguments but got {len(args)}"
        )
    
    # Verify each argument and check type matching
    for i, arg_node in enumerate(args):
        # Recursively verify the argument node
        _verify_node(arg_node, symbol_table, context_stack, filename)
        
        # Check type match (exact string matching)
        arg_data_type = arg_node.get('data_type', '')
        param_data_type = params[i].get('data_type', '')
        
        if arg_data_type != param_data_type:
            raise ValueError(
                f"{filename}:{line}:{column}: error: type mismatch for argument {i+1} in function '{func_name}': expected '{param_data_type}' but got '{arg_data_type}'"
            )
    
    # Set the return type of the function call
    node['data_type'] = return_type

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this internal verification function
