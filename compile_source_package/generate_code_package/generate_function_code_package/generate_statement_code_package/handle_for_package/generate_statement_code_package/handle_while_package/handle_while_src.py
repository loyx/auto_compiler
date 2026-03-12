# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_statement_code_package.generate_statement_code_src import generate_statement_code
from .evaluate_expression_package.evaluate_expression_src import evaluate_expression

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields for WHILE:
# {
#   "type": "WHILE",
#   "condition": dict,
#   "body": list
# }


# === main function ===
def handle_while(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for a WHILE loop statement."""
    # Get and increment label counter values
    cond_label_num = label_counter.get("while_cond", 0)
    label_counter["while_cond"] = cond_label_num + 1
    
    end_label_num = label_counter.get("while_end", 0)
    label_counter["while_end"] = end_label_num + 1
    
    cond_label = f"{func_name}_while_cond_{cond_label_num}"
    end_label = f"{func_name}_while_end_{end_label_num}"
    
    # Generate condition evaluation code (result in r0)
    condition = stmt.get("condition", {})
    cond_code = evaluate_expression(condition, var_offsets, "r0")
    
    # Generate body statements code
    body_code = ""
    current_offset = next_offset
    for body_stmt in stmt.get("body", []):
        code, current_offset = generate_statement_code(body_stmt, func_name, label_counter, var_offsets, current_offset)
        body_code += code
    
    # Assemble complete WHILE loop
    code = f"""
    b {cond_label}
{cond_label}:
    @ evaluate condition
{cond_code}
    cmp r0, #0
    beq {end_label}
    @ loop body
{body_code}
    b {cond_label}
{end_label}:
"""
    return code, current_offset


# === helper functions ===
# No helper functions needed - expression evaluation delegated


# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
