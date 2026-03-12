# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions needed for this simple code generation

# === ADT defines ===
Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,      # expression type, e.g., "NUM"
#   "value": int,     # numeric value for NUM type
# }

CodeResult = Tuple[str, int, str]
# CodeResult possible fields:
# {
#   [0]: str,  # assembly code string with indentation and newline
#   [1]: int,  # next available stack offset
#   [2]: str,  # result register name
# }

# === main function ===
def generate_num_code(expr: Expr, next_offset: int) -> CodeResult:
    """
    Generate ARM64 assembly code for NUM expression type.
    
    Loads immediate numeric value into x0 register using mov instruction.
    """
    value = expr["value"]
    assembly_code = f"    mov x0, {value}\n"
    result_register = "x0"
    
    return (assembly_code, next_offset, result_register)

# === helper functions ===
# No helper functions needed - logic is simple and self-contained

# === OOP compatibility layer ===
# Not needed - this is a utility function, not a framework entry point
