# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions - all logic inline

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name to stack byte offset
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": "BINOP" | "UNOP" | "LITERAL" | "IDENT",
#   "op": str,  # for BINOP/UNOP: "+|-|*|/|==|!=|<|>|<=|>=|&&|||!|-"
#   "left": Expr,  # for BINOP
#   "right": Expr,  # for BINOP
#   "operand": Expr,  # for UNOP
#   "value": int,  # for LITERAL
#   "name": str,  # for IDENT
# }

# === main function ===
def evaluate_expression(expr: Expr, var_offsets: VarOffsets) -> str:
    """Generate ARM assembly code to evaluate expr, result in r0."""
    if var_offsets is None:
        raise TypeError("var_offsets cannot be None")
    expr_type = expr.get("type")
    
    if expr_type == "LITERAL":
        value = expr.get("value", 0)
        return f"mov r0, #{value}"
    
    elif expr_type == "IDENT":
        name = expr.get("name", "")
        offset = var_offsets.get(name, 0)
        return f"ldr r0, [sp, #{offset}]"
    
    elif expr_type == "UNOP":
        op = expr.get("op", "")
        operand = expr.get("operand", {})
        if not operand:
            operand_code = ""
        else:
            operand_code = evaluate_expression(operand, var_offsets)
        if op == "-":
            if operand_code:
                return f"{operand_code}\n    rsb r0, r0, #0"
            else:
                return "rsb r0, r0, #0"
        elif op == "!":
            if operand_code:
                return f"{operand_code}\n    cmp r0, #0\n    moveq r0, #1\n    movne r0, #0"
            else:
                return ""
        else:
            return operand_code
    
    elif expr_type == "BINOP":
        op = expr.get("op", "")
        left = expr.get("left", {})
        right = expr.get("right", {})
        
        # Arithmetic operators
        if op == "+":
            left_code = evaluate_expression(left, var_offsets)
            right_code = evaluate_expression(right, var_offsets)
            return f"{left_code}\n    mov r1, r0\n{right_code}\n    add r0, r1, r0"
        
        elif op == "-":
            left_code = evaluate_expression(left, var_offsets)
            right_code = evaluate_expression(right, var_offsets)
            return f"{left_code}\n    mov r1, r0\n{right_code}\n    sub r0, r1, r0"
        
        elif op == "*":
            left_code = evaluate_expression(left, var_offsets)
            right_code = evaluate_expression(right, var_offsets)
            return f"{left_code}\n    mov r1, r0\n{right_code}\n    mul r0, r1, r0"
        
        elif op == "/":
            left_code = evaluate_expression(left, var_offsets)
            right_code = evaluate_expression(right, var_offsets)
            return f"{left_code}\n    mov r1, r0\n{right_code}\n    sdiv r0, r1, r0"
        
        # Comparison operators - result is 1 or 0
        elif op == "==":
            left_code = evaluate_expression(left, var_offsets)
            right_code = evaluate_expression(right, var_offsets)
            return f"{left_code}\n    mov r1, r0\n{right_code}\n    cmp r1, r0\n    moveq r0, #1\n    movne r0, #0"
        
        elif op == "!=":
            left_code = evaluate_expression(left, var_offsets)
            right_code = evaluate_expression(right, var_offsets)
            return f"{left_code}\n    mov r1, r0\n{right_code}\n    cmp r1, r0\n    movne r0, #1\n    moveq r0, #0"
        
        elif op == "<":
            left_code = evaluate_expression(left, var_offsets)
            right_code = evaluate_expression(right, var_offsets)
            return f"{left_code}\n    mov r1, r0\n{right_code}\n    cmp r1, r0\n    movlt r0, #1\n    movge r0, #0"
        
        elif op == ">":
            left_code = evaluate_expression(left, var_offsets)
            right_code = evaluate_expression(right, var_offsets)
            return f"{left_code}\n    mov r1, r0\n{right_code}\n    cmp r1, r0\n    movgt r0, #1\n    movle r0, #0"
        
        elif op == "<=":
            left_code = evaluate_expression(left, var_offsets)
            right_code = evaluate_expression(right, var_offsets)
            return f"{left_code}\n    mov r1, r0\n{right_code}\n    cmp r1, r0\n    movle r0, #1\n    movgt r0, #0"
        
        elif op == ">=":
            left_code = evaluate_expression(left, var_offsets)
            right_code = evaluate_expression(right, var_offsets)
            return f"{left_code}\n    mov r1, r0\n{right_code}\n    cmp r1, r0\n    movge r0, #1\n    movlt r0, #0"
        
        # Logical operators (short-circuit using bitwise for simplicity)
        elif op == "&&":
            left_code = evaluate_expression(left, var_offsets)
            right_code = evaluate_expression(right, var_offsets)
            return f"{left_code}\n    cmp r0, #0\n    moveq r0, #0\n    movne r0, #1\n{right_code}\n    cmp r0, #0\n    moveq r0, #0\n    movne r0, #1\n    and r0, r0, r1"
        
        elif op == "||":
            left_code = evaluate_expression(left, var_offsets)
            right_code = evaluate_expression(right, var_offsets)
            return f"{left_code}\n    cmp r0, #0\n    movne r0, #1\n    moveq r0, #0\n    mov r1, r0\n{right_code}\n    cmp r0, #0\n    movne r0, #1\n    moveq r0, #0\n    orr r0, r1, r0"
        
        else:
            return ""
    
    else:
        return ""

# === helper functions ===
# No helper functions - all logic in main

# === OOP compatibility layer ===
# Not needed - this is a pure function node
