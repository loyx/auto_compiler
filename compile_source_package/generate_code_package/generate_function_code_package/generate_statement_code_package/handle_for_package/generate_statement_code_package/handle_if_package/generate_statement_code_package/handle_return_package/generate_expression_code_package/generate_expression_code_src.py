# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===

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

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,  # "LITERAL" | "VAR" | "BINOP" | "UNOP" | "CALL"
#   "value": int | bool,  # for LITERAL
#   "name": str,  # for VAR
#   "op": str,  # for BINOP/UNOP: "+"|"-"|"*"|"/"|"=="|"!="|"<"|">"|"<="|">="|"-"|"!"
#   "left": dict,  # for BINOP
#   "right": dict,  # for BINOP
#   "operand": dict,  # for UNOP
#   "func_name": str,  # for CALL
#   "args": list,  # for CALL
# }

# === main function ===
def generate_expression_code(expr: Expr, func_name: str, label_counter: LabelCounter, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for evaluating an expression."""
    expr_type = expr["type"]
    
    if expr_type == "LITERAL":
        value = expr["value"]
        if isinstance(value, bool):
            int_val = 1 if value else 0
        else:
            int_val = value
        return f"MOV R0, #{int_val}", next_offset
    
    elif expr_type == "VAR":
        name = expr["name"]
        offset = var_offsets.get(name, 0)
        return f"LDR R0, [FP, #{offset}]", next_offset
    
    elif expr_type == "BINOP":
        op = expr["op"]
        left = expr["left"]
        right = expr["right"]
        
        # Evaluate left
        left_code, offset_after_left = generate_expression_code(left, func_name, label_counter, var_offsets, next_offset)
        
        # Evaluate right
        right_code, offset_after_right = generate_expression_code(right, func_name, label_counter, var_offsets, offset_after_left)
        
        # Perform operation
        if op in ["+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="]:
            if op == "+":
                asm_op = "ADD R0, R1, R0"
            elif op == "-":
                asm_op = "SUB R0, R1, R0"
            elif op == "*":
                asm_op = "MUL R0, R1, R0"
            elif op == "/":
                asm_op = "SDIV R0, R1, R0"
            elif op == "==":
                asm_op = "CMP R1, R0\nMOVEQ R0, #1\nMOVNE R0, #0"
            elif op == "!=":
                asm_op = "CMP R1, R0\nMOVNE R0, #1\nMOVEQ R0, #0"
            elif op == "<":
                asm_op = "CMP R1, R0\nMOVLO R0, #1\nMOVHS R0, #0"
            elif op == ">":
                asm_op = "CMP R1, R0\nMOVHI R0, #1\nMOVLS R0, #0"
            elif op == "<=":
                asm_op = "CMP R1, R0\nMOVLS R0, #1\nMOVHI R0, #0"
            elif op == ">=":
                asm_op = "CMP R1, R0\nMOVHS R0, #1\nMOVLO R0, #0"
            else:
                asm_op = ""
            
            code = f"{left_code}\nPUSH {{R0}}\n{right_code}\nPOP {{R1}}\n{asm_op}"
        else:
            code = f"{left_code}\n{right_code}"
        
        return code, offset_after_right
    
    elif expr_type == "UNOP":
        op = expr["op"]
        operand = expr["operand"]
        
        operand_code, new_offset = generate_expression_code(operand, func_name, label_counter, var_offsets, next_offset)
        
        if op == "-":
            unop_asm = "RSB R0, R0, #0"
        elif op == "!":
            unop_asm = "CMP R0, #0\nMOVEQ R0, #1\nMOVNE R0, #0"
        else:
            unop_asm = ""
        
        return f"{operand_code}\n{unop_asm}", new_offset
    
    elif expr_type == "CALL":
        func = expr["func_name"]
        args = expr["args"]
        
        arg_code_parts = []
        offset = next_offset
        
        for i, arg in enumerate(args):
            arg_asm, offset = generate_expression_code(arg, func_name, label_counter, var_offsets, offset)
            if i < 4:
                if i == 0:
                    arg_code_parts.append(arg_asm)
                else:
                    arg_code_parts.append(f"{arg_asm}\nMOV R{i}, R0")
            else:
                arg_code_parts.append(arg_asm)
        
        arg_code = "\n".join(arg_code_parts)
        call_code = f"BL {func}"
        
        full_code = f"{arg_code}\n{call_code}"
        return full_code, offset
    
    else:
        return "", next_offset

# === helper functions ===

# === OOP compatibility layer ===
