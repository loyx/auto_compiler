# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
#   "expr": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": "BINOP",
#   "op": str,
#   "left": dict,
#   "right": dict,
# }

# === main function ===
def generate_binop_code(expr: dict, func_name: str, label_counter: dict, var_offsets: dict) -> Tuple[str, int]:
    """Generate ARM assembly code for BINOP expressions."""
    # Validate required fields
    op = expr["op"]
    left = expr["left"]
    right = expr["right"]
    
    # Check for logical operators (not supported)
    if op in ("and", "or"):
        raise NotImplementedError("Logical operators require short-circuit evaluation")
    
    # Evaluate left operand
    left_code, left_reg = generate_expression_code(left, func_name, label_counter, var_offsets)
    
    # Evaluate right operand
    right_code, right_reg = generate_expression_code(right, func_name, label_counter, var_offsets)
    
    code_lines = []
    if left_code:
        code_lines.append(left_code)
    if right_code:
        code_lines.append(right_code)
    
    # Handle register conflict: if both operands in same register, move one
    if left_reg == right_reg:
        temp_reg = 1 if left_reg != 1 else 2
        code_lines.append(f"MOV R{temp_reg}, R{right_reg}")
        right_reg = temp_reg
    
    # Generate operation-specific code
    op_code = _generate_operator_code(op, left_reg, right_reg)
    code_lines.append(op_code)
    
    return ("\n".join(code_lines), 0)

# === helper functions ===
def _generate_operator_code(op: str, left_reg: int, right_reg: int) -> str:
    """Generate ARM instruction for the given operator."""
    # Arithmetic operators
    if op == "+":
        return f"ADD R0, R{left_reg}, R{right_reg}"
    elif op == "-":
        return f"SUB R0, R{left_reg}, R{right_reg}"
    elif op == "*":
        return f"MUL R0, R{left_reg}, R{right_reg}"
    elif op == "/":
        return f"SDIV R0, R{left_reg}, R{right_reg}"
    elif op == "%":
        # ARM: SDIV + MLS (multiply subtract): remainder = left - (left/right)*right
        lines = [
            f"SDIV R2, R{left_reg}, R{right_reg}",
            f"MLS R0, R2, R{right_reg}, R{left_reg}"
        ]
        return "\n".join(lines)
    
    # Bitwise operators
    elif op == "&":
        return f"AND R0, R{left_reg}, R{right_reg}"
    elif op == "|":
        return f"ORR R0, R{left_reg}, R{right_reg}"
    elif op == "^":
        return f"EOR R0, R{left_reg}, R{right_reg}"
    elif op == "<<":
        return f"LSL R0, R{left_reg}, R{right_reg}"
    elif op == ">>":
        return f"ASR R0, R{left_reg}, R{right_reg}"
    
    # Comparison operators (result is 0 or 1)
    elif op == "==":
        return f"CMP R{left_reg}, R{right_reg}\nMOVEQ R0, #1\nMOVNE R0, #0"
    elif op == "!=":
        return f"CMP R{left_reg}, R{right_reg}\nMOVNE R0, #1\nMOVEQ R0, #0"
    elif op == "<":
        return f"CMP R{left_reg}, R{right_reg}\nMOVLT R0, #1\nMOVGE R0, #0"
    elif op == ">":
        return f"CMP R{left_reg}, R{right_reg}\nMOVGT R0, #1\nMOVLE R0, #0"
    elif op == "<=":
        return f"CMP R{left_reg}, R{right_reg}\nMOVLE R0, #1\nMOVGT R0, #0"
    elif op == ">=":
        return f"CMP R{left_reg}, R{right_reg}\nMOVGE R0, #1\nMOVLT R0, #0"
    
    else:
        raise NotImplementedError(f"Operator '{op}' not supported")

# === OOP compatibility layer ===
# Not required for this function node
