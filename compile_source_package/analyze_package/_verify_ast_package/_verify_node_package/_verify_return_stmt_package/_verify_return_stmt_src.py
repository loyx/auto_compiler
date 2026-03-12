# === std / third-party imports ===
from typing import Any, Dict, List, Optional

# === sub function imports ===
# No child functions needed; all logic is self-contained

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("return_stmt", "int_literal", "variable_ref", etc.)
#   "value": Optional[dict], # 返回值表达式（可选，None 表示无返回值）
#   "line": int,             # 行号
#   "column": int,           # 列号
#   "data_type": Optional[str], # 表达式的数据类型（如 "int", "char", "void"）
#   "name": Optional[str],   # 变量引用名（用于 variable_ref 类型）
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # 变量名 -> {data_type: str, scope: int, ...}
#   "functions": Dict[str, Dict],
#   "current_scope": int,
# }

ContextStack = List[Dict[str, Any]]
# ContextStack possible fields:
# [
#   {"type": "function", "name": str, "return_type": str},
#   {"type": "loop", "stmt_type": "while" | "for"}
# ]

# === main function ===
def _verify_return_stmt(node: dict, symbol_table: dict, context_stack: list, filename: str) -> None:
    """
    Verify return statement is in valid function context and return type matches.
    
    Args:
        node: Return statement node with 'value' (optional), 'line', 'column'
        symbol_table: Symbol table for variable type information
        context_stack: Control flow context stack (top is most recent)
        filename: Source file name for error messages
    
    Raises:
        ValueError: If return is outside function or type mismatch occurs
    """
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # Step 1: Check if we're in a function context
    # context_stack should have at least one frame, and top should be function
    if not context_stack or context_stack[-1].get("type") != "function":
        raise ValueError(
            f"{filename}:{line}:{column}: error: return statement outside of function"
        )
    
    current_func = context_stack[-1]
    expected_return_type = current_func.get("return_type", "void")
    
    # Step 2: Get return value expression node
    return_value = node.get("value")
    
    # Step 3: Handle case with no return value
    if return_value is None:
        if expected_return_type != "void":
            raise ValueError(
                f"{filename}:{line}:{column}: error: function expects return value of type "
                f"'{expected_return_type}', but no value returned"
            )
        return  # void function with no return value is valid
    
    # Step 4: Determine actual return type from return_value node
    actual_type: Optional[str] = return_value.get("data_type")
    
    # If data_type is not set, infer from node type
    if actual_type is None:
        value_type = return_value.get("type", "")
        
        if value_type in ("int_literal", "binary_op"):
            actual_type = "int"
        elif value_type == "char_literal":
            actual_type = "char"
        elif value_type == "variable_ref":
            # Look up variable type in symbol_table
            var_name = return_value.get("name")
            if var_name:
                var_info = symbol_table.get("variables", {}).get(var_name)
                if var_info:
                    actual_type = var_info.get("data_type")
        
        # If still cannot determine type, raise error
        if actual_type is None:
            raise ValueError(
                f"{filename}:{line}:{column}: error: unable to determine return value type"
            )
    
    # Step 5: Check type matching
    if actual_type != expected_return_type:
        raise ValueError(
            f"{filename}:{line}:{column}: error: return type mismatch, expected "
            f"'{expected_return_type}', got '{actual_type}'"
        )

# === helper functions ===
# No helper functions needed; all logic is in main function

# === OOP compatibility layer ===
# Not required for this utility function; omitted