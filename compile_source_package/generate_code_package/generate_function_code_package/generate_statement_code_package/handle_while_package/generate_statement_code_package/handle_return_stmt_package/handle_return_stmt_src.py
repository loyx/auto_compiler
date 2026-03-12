# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,
#   "value": dict,         # return value expression (optional)
#   "expression": dict,    # alias for value
# }

# === main function ===
def handle_return_stmt(stmt: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """
    Handle RETURN statement.
    
    Generates assembly code for return value expression (if present),
    then appends 'ret' instruction. Expression result is expected
    to be in x0 register for return.
    
    Args:
        stmt: RETURN statement dict with optional "value" or "expression" field
        var_offsets: Variable name to stack offset mapping
        next_offset: Current next available stack offset
    
    Returns:
        Tuple of (generated assembly code string, updated next_offset)
    """
    code_lines = []
    
    # Extract value/expression from stmt (check both keys)
    # 'value' takes precedence over 'expression'
    if "value" in stmt:
        value = stmt.get("value")
    else:
        value = stmt.get("expression")
    
    # If value key exists (even if value is None or empty dict), generate code
    # Only skip if neither key exists or both are explicitly None
    if "value" in stmt or "expression" in stmt:
        if value is not None:
        expr_code, next_offset = generate_expression_code(
            value, var_offsets, next_offset
        )
        code_lines.append(expr_code)
    
    # Append ret instruction
    code_lines.append("ret")
    
    # Join all code lines
    generated_code = "\n".join(code_lines)
    
    return (generated_code, next_offset)

# === helper functions ===
# No helper functions needed - logic is simple and inline

# === OOP compatibility layer ===
# Not needed - this is a function node, not a framework entry point
