# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset for variable
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": "literal" | "identifier" | "binary",
#   "op": str (for binary: "add"|"sub"|"mul"|"div"|"lt"|"gt"|"le"|"ge"|"eq"|"ne"),
#   "left": Expr (for binary),
#   "right": Expr (for binary),
#   "value": int (for literal),
#   "name": str (for identifier)
# }

# === main function ===
def evaluate_expression(expr: Expr, var_offsets: VarOffsets, target_reg: str) -> str:
    """Generate ARM assembly code to evaluate an expression into target_reg."""
    expr_type = expr["type"]
    
    if expr_type == "literal":
        value = expr["value"]
        return f"    mov {target_reg}, #{value}\n"
    
    elif expr_type == "identifier":
        name = expr["name"]
        offset = var_offsets[name]
        return f"    ldr {target_reg}, [fp, #{offset}]\n"
    
    elif expr_type == "binary":
        op = expr["op"]
        left = expr["left"]
        right = expr["right"]
        
        # Determine temp register for right operand
        if target_reg == "r0":
            temp_reg = "r1"
        else:
            temp_reg = "r1"
        
        # Evaluate left operand into target_reg
        code = evaluate_expression(left, var_offsets, target_reg)
        
        # Evaluate right operand into temp_reg
        code += evaluate_expression(right, var_offsets, temp_reg)
        
        # Emit operation
        if op == "add":
            code += f"    add {target_reg}, {target_reg}, {temp_reg}\n"
        elif op == "sub":
            code += f"    sub {target_reg}, {target_reg}, {temp_reg}\n"
        elif op == "mul":
            code += f"    mul {target_reg}, {target_reg}, {temp_reg}\n"
        elif op == "div":
            code += f"    sdiv {target_reg}, {target_reg}, {temp_reg}\n"
        elif op == "lt":
            code += f"    cmp {target_reg}, {temp_reg}\n"
            code += f"    movlt {target_reg}, #1\n"
            code += f"    movge {target_reg}, #0\n"
        elif op == "gt":
            code += f"    cmp {target_reg}, {temp_reg}\n"
            code += f"    movgt {target_reg}, #1\n"
            code += f"    movle {target_reg}, #0\n"
        elif op == "le":
            code += f"    cmp {target_reg}, {temp_reg}\n"
            code += f"    movle {target_reg}, #1\n"
            code += f"    movgt {target_reg}, #0\n"
        elif op == "ge":
            code += f"    cmp {target_reg}, {temp_reg}\n"
            code += f"    movge {target_reg}, #1\n"
            code += f"    movlt {target_reg}, #0\n"
        elif op == "eq":
            code += f"    cmp {target_reg}, {temp_reg}\n"
            code += f"    moveq {target_reg}, #1\n"
            code += f"    movne {target_reg}, #0\n"
        elif op == "ne":
            code += f"    cmp {target_reg}, {temp_reg}\n"
            code += f"    movne {target_reg}, #1\n"
            code += f"    moveq {target_reg}, #0\n"
        else:
            assert False, f"Unknown binary operator: {op}"
        
        return code
    
    else:
        assert False, f"Unknown expression type: {expr_type}"

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
