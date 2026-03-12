# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No subfunctions needed for this handler

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "continue": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,
# }

# === main function ===
def handle_continue_stmt(stmt: Stmt, func_name: str, label_counter: LabelCounter) -> Tuple[str, int]:
    """
    Handle CONTINUE statement in function dependency tree.
    
    Increments label_counter["continue"] in-place and generates branch instruction
    to innermost while condition label.
    
    Args:
        stmt: CONTINUE statement dict (type field only)
        func_name: Current function name for label naming
        label_counter: Mutable dict for unique labels, modified in-place
    
    Returns:
        Tuple of (branch code string, unchanged next_offset)
    """
    # Increment continue counter in-place
    label_counter["continue"] = label_counter.get("continue", 0) + 1
    count = label_counter["continue"]
    
    # Generate branch instruction to innermost while condition label
    branch_code = f"b {func_name}_while_cond_{count}"
    
    # Return branch code with unchanged next_offset (0 indicates no offset change)
    return (branch_code, 0)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node