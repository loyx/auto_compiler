# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions needed for this implementation

# === ADT defines ===
Expression = Dict[str, Any]
# Expression possible fields:
# {
#   "type": str,  # "LITERAL" | "IDENTIFIER" | "BINARY_OP" | "UNARY_OP" | "CALL"
#   "value": Any,  # For LITERAL: the literal value
#   "literal_type": str,  # For LITERAL: "int" | "bool" | "string" | "null"
# }

# === main function ===
def generate_literal_code(expr: Expression, next_offset: int) -> Tuple[str, int]:
    """
    Generate ARM assembly code to load a literal value into x0 register.
    
    Args:
        expr: LITERAL expression dict with 'type', 'value', 'literal_type'
        next_offset: Current next available stack offset (unchanged)
    
    Returns:
        Tuple of (generated_code, next_offset) where next_offset is unchanged
    """
    literal_type = expr.get("literal_type", "int")
    value = expr.get("value")
    
    if literal_type == "int":
        code = _generate_int_literal_code(value)
    elif literal_type == "bool":
        code = _generate_bool_literal_code(value)
    elif literal_type == "null":
        code = "mov x0, #0"
    elif literal_type == "string":
        code = _generate_string_literal_code(value)
    else:
        raise ValueError(f"Unknown literal type: {literal_type}")
    
    return (code, next_offset)

# === helper functions ===
def _generate_int_literal_code(value: int) -> str:
    """Generate ARM code for integer literal."""
    # ARM64 mov immediate supports 16-bit value with optional left shift (0, 16, 32, 48)
    # Simple heuristic: if value fits in 16 bits or is small, use direct mov
    if -65536 <= value <= 65535:
        return f"mov x0, #{value}"
    else:
        # Use movz/movk pattern for large integers
        # Load 16-bit chunks at different offsets
        lines = []
        abs_value = abs(value)
        
        # Extract 16-bit chunks
        chunk0 = abs_value & 0xFFFF
        chunk1 = (abs_value >> 16) & 0xFFFF
        chunk2 = (abs_value >> 32) & 0xFFFF
        chunk3 = (abs_value >> 48) & 0xFFFF
        
        # Start with movz for the highest non-zero chunk
        chunks = [(chunk3, 48), (chunk2, 32), (chunk1, 16), (chunk0, 0)]
        started = False
        
        for chunk, shift in chunks:
            if chunk != 0:
                if not started:
                    lines.append(f"movz x0, #{chunk}, lsl #{shift}")
                    started = True
                else:
                    lines.append(f"movk x0, #{chunk}, lsl #{shift}")
        
        # Handle negative values
        if value < 0:
            lines.append("mvn x0, x0")
        
        return "\n".join(lines) if lines else "mov x0, #0"

def _generate_bool_literal_code(value: bool) -> str:
    """Generate ARM code for boolean literal."""
    if value:
        return "mov x0, #1"
    else:
        return "mov x0, #0"

def _generate_string_literal_code(value: str) -> str:
    """Generate ARM code for string literal (load address)."""
    # Use placeholder: load address from data section
    # In practice, this would reference a label in the data section
    return f"ldr x0, =str_literal"

# === OOP compatibility layer ===
# Not needed: this is a pure function node, not a framework entry point
