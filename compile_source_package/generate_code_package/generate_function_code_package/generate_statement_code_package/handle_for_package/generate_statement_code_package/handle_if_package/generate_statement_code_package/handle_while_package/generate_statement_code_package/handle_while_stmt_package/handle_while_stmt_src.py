# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code
from .generate_statement_code_package.generate_statement_code_src import generate_statement_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "if_else": int,
#   "if_end": int,
#   "while_start": int,
#   "while_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,  # "while", "if", "assign", "return", "expr_stmt"
#   "condition": dict,  # for while/if
#   "body": list,  # for while/if
#   "else_body": list,  # for if
#   "variable": str,  # for assign
#   "value": dict,  # for assign
#   "expression": dict,  # for expr_stmt
#   "return_value": dict,  # for return
# }

# === main function ===
def handle_while_stmt(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for a while loop statement."""
    # Generate unique labels by incrementing counters
    label_counter["while_start"] = label_counter.get("while_start", 0) + 1
    label_counter["while_end"] = label_counter.get("while_end", 0) + 1
    start_label = f"{func_name}_while_start_{label_counter['while_start']}"
    end_label = f"{func_name}_while_end_{label_counter['while_end']}"
    
    # Generate condition evaluation code (result in R0)
    condition_code, cond_offset = generate_expression_code(
        stmt["condition"], func_name, label_counter, var_offsets, next_offset
    )
    
    # Generate body code by iterating over each statement
    body_code_parts = []
    current_offset = cond_offset
    for body_stmt in stmt["body"]:
        code, current_offset = generate_statement_code(
            body_stmt, func_name, label_counter, var_offsets, current_offset
        )
        body_code_parts.append(code)
    body_code = "\n".join(body_code_parts)
    
    # Assemble final ARM assembly code
    asm_code = f"""{start_label}:
{condition_code}
    CMP R0, #0
    BEQ {end_label}
{body_code}
    B {start_label}
{end_label}:
"""
    
    return asm_code, current_offset

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
