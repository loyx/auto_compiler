# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Import parent function for mutual recursion (allowed pattern for AST verification)
# Use lazy import to avoid circular dependency
_verify_node = None

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("binary_op")
#   "left": dict,            # 左操作数节点 (must exist)
#   "right": dict,           # 右操作数节点 (must exist)
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int,           # 列号
#   "operator": str          # 操作符
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
# }

ContextStack = list
# ContextStack possible fields:
# [
#   {"type": "function", "name": str, "return_type": str},
#   {"type": "loop", "stmt_type": "while"|"for"}
# ]

# === main function ===
def _verify_binary_op(node: dict, symbol_table: dict, context_stack: list, filename: str) -> None:
    """
    Verify a binary operation AST node.
    
    Recursively validates left and right operands, checks type matching,
    and sets node['data_type'] to the operand type.
    """
    # Lazy import to avoid circular dependency
    global _verify_node
    if _verify_node is None:
        from .._verify_node_src import _verify_node
    
    # Recursively verify left and right operands
    _verify_node(node['left'], symbol_table, context_stack, filename)
    _verify_node(node['right'], symbol_table, context_stack, filename)
    
    # Extract types from verified children
    left_type = node['left']['data_type']
    right_type = node['right']['data_type']
    
    # Check type matching (left type is the expected type)
    if left_type != right_type:
        raise ValueError(
            f"{filename}:{node['line']}:{node['column']}: "
            f"error: type mismatch: expected '{left_type}' but got '{right_type}'"
        )
    
    # Set the node's data_type to the operand type
    node['data_type'] = left_type

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# No OOP wrapper needed for this internal verification function
