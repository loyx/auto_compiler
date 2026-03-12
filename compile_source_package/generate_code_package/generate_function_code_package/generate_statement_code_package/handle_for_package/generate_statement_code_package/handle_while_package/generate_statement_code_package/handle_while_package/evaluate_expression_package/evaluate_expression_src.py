# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions - inline implementation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name to stack offset mapping
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,        # "VAR", "LITERAL", "BINOP", "UNOP"
#   "name": str,        # for VAR: variable name
#   "value": int,       # for LITERAL: constant value
#   "op": str,          # for BINOP/UNOP: operator name
#   "left": dict,       # for BINOP: left operand expr
#   "right": dict,      # for BINOP: right operand expr
#   "operand": dict,    # for UNOP: operand expr
# }

# === main function ===
def evaluate_expression(expr: Expr, func_name: str, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """
    Generate ARM32 assembly code to evaluate an expression.
    Result is placed in r0 register.
    Returns (assembly_code, updated_offset).
    """
    expr_type = expr.get("type")
    
    if expr_type == "LITERAL":
        value = expr["value"]
        code = f"mov r0, #{value}"
        return (code, next_offset)
    
    elif expr_type == "VAR":
        var_name = expr["name"]
        offset = var_offsets[var_name]  # Raises KeyError if not found
        code = f"ldr r0, [sp, #{offset}]"
        return (code, next_offset)
    
    elif expr_type == "BINOP":
        op = expr["op"]
        left_expr = expr["left"]
        right_expr = expr["right"]
        
        # Evaluate left operand
        left_code, offset_after_left = evaluate_expression(left_expr, func_name, var_offsets, next_offset)
        
        # Save left result to stack
        save_offset = offset_after_left
        save_code = f"str r0, [sp, #{save_offset}]"
        offset_after_save = save_offset + 4
        
        # Evaluate right operand
        right_code, offset_after_right = evaluate_expression(right_expr, func_name, var_offsets, offset_after_save)
        
        # Load left operand into r1
        load_code = f"ldr r1, [sp, #{save_offset}]"
        
        # Apply operation
        op_code = _generate_binop_instruction(op)
        
        # Combine all code
        all_code = "\n".join([left_code, save_code, right_code, load_code, op_code])
        return (all_code, offset_after_right)
    
    elif expr_type == "UNOP":
        op = expr["op"]
        operand_expr = expr["operand"]
        
        # Evaluate operand
        operand_code, offset_after_operand = evaluate_expression(operand_expr, func_name, var_offsets, next_offset)
        
        # Apply unary operation
        unop_code = _generate_unop_instruction(op)
        
        all_code = "\n".join([operand_code, unop_code])
        return (all_code, offset_after_operand)
    
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
def _generate_binop_instruction(op: str) -> str:
    """Generate ARM32 instruction for binary operation."""
    arithmetic_ops = {
        "add": "add r0, r0, r1",
        "sub": "sub r0, r0, r1",
        "mul": "mul r0, r0, r1",
        "div": "sdiv r0, r0, r1",
    }
    
    logical_ops = {
        "and": "and r0, r0, r1",
        "or": "orr r0, r0, r1",
    }
    
    comparison_ops = {
        "eq": ("cmp r0, r1", "cset r0, eq"),
        "ne": ("cmp r0, r1", "cset r0, ne"),
        "lt": ("cmp r0, r1", "cset r0, lt"),
        "le": ("cmp r0, r1", "cset r0, le"),
        "gt": ("cmp r0, r1", "cset r0, gt"),
        "ge": ("cmp r0, r1", "cset r0, ge"),
    }
    
    if op in arithmetic_ops:
        return arithmetic_ops[op]
    elif op in logical_ops:
        return logical_ops[op]
    elif op in comparison_ops:
        cmp_instr, cset_instr = comparison_ops[op]
        return f"{cmp_instr}\n{cset_instr}"
    elif op == "mod":
        # mod: sdiv + msub
        return "sdiv r2, r0, r1\nmsub r0, r2, r1, r0"
    else:
        raise ValueError(f"Unknown binary operator: {op}")

def _generate_unop_instruction(op: str) -> str:
    """Generate ARM32 instruction for unary operation."""
    unop_map = {
        "neg": "neg r0, r0",
        "not": "mvn r0, r0",
    }
    
    if op in unop_map:
        return unop_map[op]
    else:
        raise ValueError(f"Unknown unary operator: {op}")

# === OOP compatibility layer ===
# Not required for this function node - omitted