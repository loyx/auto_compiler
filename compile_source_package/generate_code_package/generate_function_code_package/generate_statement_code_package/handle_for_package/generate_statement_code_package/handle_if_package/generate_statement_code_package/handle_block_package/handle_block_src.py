# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ..generate_statement_code_src import generate_statement_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "if_else": int,
#   "if_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,
#   "statements": list,
# }

# === main function ===
def handle_block(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle BLOCK statement code generation.
    
    Iterates through statements list, calling generate_statement_code for each,
    joining results with newlines. Propagates offset through sequence.
    """
    statements = stmt.get("statements", [])
    
    if not statements:
        return ("", next_offset)
    
    all_codes = []
    current_offset = next_offset
    
    for s in statements:
        code, current_offset = generate_statement_code(s, func_name, label_counter, var_offsets, current_offset)
        all_codes.append(code)
    
    return ("\n".join(all_codes), current_offset)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
