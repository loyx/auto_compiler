# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# _verify_node will be imported with delay inside the function to avoid circular dependency

# === ADT defines ===
ASTNode = Dict[str, Any]
# ASTNode possible fields:
# {
#   "type": str,
#   "target": Dict[str, Any],
#   "value": Dict[str, Any],
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "current_scope": int
# }

ContextStack = list
# ContextStack possible fields:
# [
#   {"type": "function", "name": str, "return_type": str},
#   {"type": "loop", "stmt_type": str}
# ]

# === main function ===
def _verify_assignment(node: ASTNode, symbol_table: SymbolTable, context_stack: ContextStack, filename: str) -> None:
    """
    Verify assignment node: validate right-hand value, check variable existence, ensure type match.
    Raises ValueError on undefined variable, type mismatch, or unable to determine value type.
    """
    target = node['target']
    value = node['value']
    line = target.get('line', node.get('line', 0))
    column = target.get('column', node.get('column', 0))
    
    # 1. Recursively verify right-hand value expression
    from .. import _verify_node_src
    _verify_node_src._verify_node(value, symbol_table, context_stack, filename)
    
    # 2. Get right-hand value type
    value_type = value.get('data_type')
    if value_type is None:
        raise ValueError(f"{filename}:{line}:{column}: error: unable to determine type of assignment value")
    
    # 3. Look up left-hand variable
    var_name = target['name']
    if var_name not in symbol_table['variables']:
        raise ValueError(f"{filename}:{line}:{column}: error: undefined variable '{var_name}'")
    
    var_info = symbol_table['variables'][var_name]
    expected_type = var_info['data_type']
    
    # 4. Type match check (exact string equality)
    if value_type != expected_type:
        raise ValueError(f"{filename}:{line}:{column}: error: type mismatch in assignment, expected {expected_type} but got {value_type}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
