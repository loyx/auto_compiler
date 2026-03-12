# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple validation logic

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("break_stmt" 或 "continue_stmt")
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ContextStack = list
# ContextStack possible fields:
# [
#   {"type": "function", "name": str, "return_type": str},
#   {"type": "loop", "stmt_type": "while"|"for"}
# ]

# === main function ===
def _verify_control_flow_stmt(node: dict, context_stack: list, filename: str) -> None:
    """
    Verify that break/continue statements only appear inside loop contexts.
    
    Checks context_stack from top to bottom for a loop frame.
    Raises ValueError if no loop context is found.
    """
    # Search from stack top to bottom for a loop frame
    has_loop_context = False
    for frame in reversed(context_stack):
        if isinstance(frame, dict) and frame.get("type") == "loop":
            has_loop_context = True
            break
    
    # If no loop context found, raise appropriate error
    if not has_loop_context:
        line = node.get("line", 0)
        column = node.get("column", 0)
        node_type = node.get("type", "")
        
        if node_type == "break_stmt":
            raise ValueError(f"{filename}:{line}:{column}: error: 'break' is not allowed outside of a loop")
        elif node_type == "continue_stmt":
            raise ValueError(f"{filename}:{line}:{column}: error: 'continue' is not allowed outside of a loop")

# === helper functions ===
# No helper functions needed for this simple validation logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure validation function