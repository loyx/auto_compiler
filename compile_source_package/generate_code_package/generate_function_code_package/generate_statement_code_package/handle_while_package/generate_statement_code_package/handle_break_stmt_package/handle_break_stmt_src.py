# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions needed for this simple handler

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "break": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,
# }

# === main function ===
def handle_break_stmt(stmt: Stmt, func_name: str, label_counter: LabelCounter) -> Tuple[str, int]:
    """
    Handle BREAK statement in function dependency tree.
    
    Generates branch instruction to innermost while end label.
    Modifies label_counter in-place to track break count.
    
    Args:
        stmt: BREAK statement dict (type field only)
        func_name: Current function name for label naming
        label_counter: Mutable dict for unique labels (modified in-place)
    
    Returns:
        Tuple of (branch code string, unchanged next_offset)
    """
    # Increment break counter in-place
    label_counter["break"] = label_counter.get("break", 0) + 1
    count = label_counter["break"]
    
    # Generate branch instruction to innermost while end label
    branch_code = f"b {func_name}_while_end_{count}"
    
    # Return branch code with unchanged next_offset (0 for branch instructions)
    return (branch_code, 0)

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed - this is a statement handler, not a framework entry point
