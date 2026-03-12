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
#   "type": str,
#   "condition": dict,
#   "body": list,
# }

# === main function ===
def handle_while(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly for WHILE loop statement."""
    # Generate unique labels using read-then-increment pattern
    start_num = label_counter.get("while_start", 0)
    label_counter["while_start"] = start_num + 1
    end_num = label_counter.get("while_end", 0)
    label_counter["while_end"] = end_num + 1
    
    loop_start_label = f"{func_name}_while_{start_num}_start"
    loop_end_label = f"{func_name}_while_{end_num}_end"
    
    # Generate condition evaluation code
    condition_code, cond_offset = generate_expression_code(
        stmt["condition"], func_name, label_counter, var_offsets, next_offset
    )
    
    # Generate body code by iterating through statements
    body_lines = []
    body_offset = cond_offset
    for body_stmt in stmt.get("body", []):
        stmt_code, body_offset = generate_statement_code(
            body_stmt, func_name, label_counter, var_offsets, body_offset
        )
        body_lines.append(stmt_code)
    body_code = "\n".join(body_lines)
    
    # Assemble complete WHILE loop structure
    asm_lines = [
        f"{loop_start_label}:",
        condition_code,
        "CMP R0, #0",
        f"B.EQ {loop_end_label}",
        body_code,
        f"B {loop_start_label}",
        f"{loop_end_label}:",
    ]
    
    asm_code = "\n".join(asm_lines)
    return (asm_code, body_offset)

# === helper functions ===

# === OOP compatibility layer ===
