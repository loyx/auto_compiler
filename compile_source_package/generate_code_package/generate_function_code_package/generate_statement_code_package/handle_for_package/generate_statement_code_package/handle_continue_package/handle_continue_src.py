# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions needed for this simple branch generator

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
#   "while_cond": int,
#   "while_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields for CONTINUE:
# {
#   "type": "CONTINUE",
#   "loop_type": "FOR" | "WHILE",
#   "loop_depth": int
# }

# === main function ===
def handle_continue(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """
    Generate ARM assembly code for a CONTINUE statement.
    Emits an unconditional branch to the enclosing loop's update (FOR) or condition (WHILE) label.
    """
    # Validate required fields
    if "loop_type" not in stmt:
        raise ValueError("CONTINUE statement missing loop_type")
    if "loop_depth" not in stmt:
        raise ValueError("CONTINUE statement missing loop_depth")
    
    loop_type = stmt["loop_type"]
    loop_depth = stmt["loop_depth"]
    
    # Determine target label based on loop type
    if loop_type == "FOR":
        target = f"{func_name}_for_{loop_depth}_update"
    elif loop_type == "WHILE":
        target = f"{func_name}_while_{loop_depth}_cond"
    else:
        raise ValueError(f"Invalid loop_type in CONTINUE: {loop_type}")
    
    # Generate ARM branch instruction
    code = f"    B {target}\n"
    
    return (code, next_offset)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
