# === std / third-party imports ===
from typing import Any, Dict, List, Tuple

# === sub function imports ===
# No child functions needed - this is a simple leaf node

# === ADT defines ===
LabelCounter = Dict[str, Any]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
#   "loop_stack": List[str],  # Stack of end labels for nested loops
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields for BREAK:
# {
#   "type": "BREAK",
#   "target_loop_type": "FOR" | "WHILE",
#   "loop_depth": int
# }

# === main function ===
def handle_break(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for a BREAK statement.
    
    Reads the innermost loop's end label from label_counter["loop_stack"]
    and generates an unconditional branch instruction to that label.
    """
    loop_stack: List[str] = label_counter.get("loop_stack", [])
    
    if not loop_stack:
        raise ValueError("BREAK statement outside of loop context")
    
    end_label = loop_stack[-1]
    code = f"    B {end_label}\n"
    
    return code, next_offset

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required - this is a plain function node