# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions delegated; expression evaluation is handled inline

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields for RETURN:
# {
#   "type": "RETURN",
#   "value": dict or None  # expression dict or None/empty for void return
# }

# === main function ===
def handle_return(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """
    Generate ARM32 assembly code for a RETURN statement.
    
    If value is present: emit code to evaluate expression into R0, then branch to epilogue.
    If value is None/empty: branch directly to epilogue.
    
    Returns Tuple[assembly_code, next_offset] where next_offset is unchanged.
    """
    lines = []
    value = stmt.get("value")
    
    # Check if value is present and non-empty
    if value is not None and isinstance(value, dict) and len(value) > 0:
        # Evaluate expression and place result in R0
        expr_code = _evaluate_expression(value, var_offsets, func_name)
        lines.append(expr_code)
    
    # Branch to function epilogue (epilogue handles actual BX LR)
    epilogue_label = f"{func_name}_epilogue"
    lines.append(f"    B {epilogue_label}")
    
    code = "\n".join(lines)
    return (code, next_offset)

# === helper functions ===
def _evaluate_expression(expr: dict, var_offsets: dict, func_name: str) -> str:
    """
    Evaluate an expression and generate ARM code to place result in R0.
    
    Supported expression types:
    - CONST_INT: load immediate integer
    - CONST_FLOAT: load immediate float (simplified)
    - VAR_REF: load from stack variable
    - ADD, SUB, MUL, DIV: binary operations
    """
    expr_type = expr.get("type", "")
    
    if expr_type == "CONST_INT":
        val = expr.get("value", 0)
        return f"    MOV R0, #{val}"
    
    elif expr_type == "CONST_FLOAT":
        # Simplified: treat as integer for now (real impl would use VFP)
        val = int(expr.get("value", 0))
        return f"    MOV R0, #{val}"
    
    elif expr_type == "VAR_REF":
        var_name = expr.get("var_name", "")
        if var_name in var_offsets:
            offset = var_offsets[var_name]
            return f"    LDR R0, [FP, #{offset}]"
        else:
            # Variable not found; load 0 as default
            return "    MOV R0, #0"
    
    elif expr_type in ("ADD", "SUB", "MUL", "DIV"):
        # Evaluate left operand into R0
        left = expr.get("left", {})
        left_code = _evaluate_expression(left, var_offsets, func_name)
        
        # Evaluate right operand into R1 (temp register)
        right = expr.get("right", {})
        right_code = _evaluate_expression(right, var_offsets, func_name)
        # right_code expects result in R0, so we need to move it to R1
        right_code = right_code.replace("MOV R0,", "MOV R1,").replace("LDR R0,", "LDR R1,")
        
        # Perform operation
        op_map = {"ADD": "ADD", "SUB": "SUB", "MUL": "MUL", "DIV": "SDIV"}
        op = op_map.get(expr_type, "ADD")
        result_code = f"    {op} R0, R0, R1"
        
        return f"{left_code}\n{right_code}\n{result_code}"
    
    else:
        # Unknown expression type; default to 0
        return "    MOV R0, #0"

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
