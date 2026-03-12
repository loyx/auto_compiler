# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No sub functions needed for this inline implementation

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
#   "skip": int,
#   "true": int,
#   "false": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

ExprDict = Dict[str, Any]
# ExprDict possible fields:
# {
#   "type": str,
#   "operator": str,
#   "left": ExprDict,
#   "right": ExprDict,
#   "value": Any,
#   "name": str,
# }

# === main function ===
def generate_const_code(value: Any, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 assembly code to load a constant value into x0 register."""
    # Handle boolean values: convert to 0 or 1
    if isinstance(value, bool):
        value = 1 if value else 0
    
    # Type validation
    if not isinstance(value, int):
        raise ValueError(f"Unsupported constant type: {type(value).__name__}")
    
    # Generate assembly code based on value range
    if 0 <= value <= 65535:
        # Simple MOV for 16-bit range
        code = f"// load constant {value}\nMOV x0, #{value}\n"
    else:
        # MOVZ/MOVK sequence for larger values (including negative via two's complement)
        code_lines = [f"// load constant {value}"]
        
        # Convert to 64-bit unsigned representation for negative values
        unsigned_value = value & 0xFFFFFFFFFFFFFFFF
        
        # Extract 16-bit chunks and generate MOVZ/MOVK instructions
        first_chunk = True
        for shift in [0, 16, 32, 48]:
            chunk = (unsigned_value >> shift) & 0xFFFF
            if chunk != 0:
                if first_chunk:
                    # First non-zero chunk uses MOVZ
                    code_lines.append(f"MOVZ x0, #{chunk}, LSL #{shift}")
                    first_chunk = False
                else:
                    # Subsequent chunks use MOVK
                    code_lines.append(f"MOVK x0, #{chunk}, LSL #{shift}")
        
        # Handle the case where value is 0 (all chunks are 0)
        if first_chunk:
            code_lines.append("MOVZ x0, #0")
        
        code = "\n".join(code_lines) + "\n"
    
    # Return code with unchanged offset (constants don't use stack space)
    return (code, next_offset)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
