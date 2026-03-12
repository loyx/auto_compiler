# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code
from .generate_statement_code_package.generate_statement_code_src import generate_statement_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_start": int,
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
#   "body": list,
# }

# === main function ===
def handle_while(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle WHILE statement: generate labels, condition code, body code, and jumps."""
    # Extract condition and body from statement
    condition = stmt["condition"]
    body = stmt["body"]
    
    # Generate unique labels using label_counter (increment in-place)
    start_count = label_counter["while_start"]
    end_count = label_counter["while_end"]
    label_counter["while_start"] = start_count + 1
    label_counter["while_end"] = end_count + 1
    
    start_label = f"{func_name}_while_start_{start_count}"
    end_label = f"{func_name}_while_end_{end_count}"
    
    # Generate condition evaluation code
    cond_code, offset_after_cond, result_reg = generate_expression_code(
        condition, var_offsets, next_offset
    )
    
    # Generate body statements code
    body_codes = []
    current_offset = offset_after_cond
    for body_stmt in body:
        body_code, current_offset = generate_statement_code(
            body_stmt, func_name, label_counter, var_offsets, current_offset
        )
        body_codes.append(body_code)
    
    # Assemble the complete WHILE structure
    lines = []
    lines.append(f"{start_label}:")
    lines.append(f"    {cond_code}")
    lines.append(f"    cbz {result_reg}, {end_label}")
    if body_codes:
        lines.append("\n".join(body_codes))
    lines.append(f"    b {start_label}")
    lines.append(f"{end_label}:")
    
    assembled_code = "\n".join(lines)
    return (assembled_code, current_offset)

# === helper functions ===
# No helper functions needed; all logic is in main function

# === OOP compatibility layer ===
# Not needed for this function node
