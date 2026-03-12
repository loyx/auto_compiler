# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "if_else": int,
#   "if_end": int,
#   "expr_temp": int,
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
#   "value": dict | None,
# }

# === main function ===
def handle_return(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for RETURN statement."""
    asm_lines = []
    
    # Check if this is a void return or has a value
    return_value = stmt.get("value")
    
    if return_value is not None:
        # Non-void return: evaluate expression first (result in R0)
        expr_code, updated_offset = generate_expression_code(
            return_value, func_name, label_counter, var_offsets, next_offset
        )
        asm_lines.append(expr_code)
    
    # Generate function epilogue (standard for all returns)
    asm_lines.append("MOV SP, FP")
    asm_lines.append("POP FP")
    asm_lines.append("BX LR")
    
    # Join all assembly lines and return (offset unchanged after epilogue)
    asm_code = "\n".join(asm_lines)
    return (asm_code, next_offset)

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node