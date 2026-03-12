# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code
from .generate_statement_code_package.generate_statement_code_src import generate_statement_code

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
# Stmt possible fields:
# {
#   "type": str,
#   "condition": dict,     # condition expression for WHILE
#   "body": list,          # body statements
# }

# === main function ===
def handle_while_stmt(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle WHILE statement and generate assembly code."""
    # Extract condition and body
    condition = stmt["condition"]
    body = stmt["body"]
    
    # Increment label counters in-place
    label_counter["while_cond"] = label_counter.get("while_cond", 0) + 1
    label_counter["while_end"] = label_counter.get("while_end", 0) + 1
    
    # Generate unique labels
    cond_label = f"{func_name}_while_cond_{label_counter['while_cond']}"
    end_label = f"{func_name}_while_end_{label_counter['while_end']}"
    
    # Generate condition code
    cond_code, next_offset = generate_expression_code(condition, var_offsets, next_offset)
    
    # Generate body code for each statement
    body_lines = []
    for body_stmt in body:
        stmt_code, next_offset = generate_statement_code(body_stmt, func_name, label_counter, var_offsets, next_offset)
        body_lines.append(stmt_code)
    body_code = "\n".join(body_lines)
    
    # Assemble while loop structure
    lines = [
        f"{cond_label}:",
        cond_code,
        f"    cbz x0, {end_label}",
        body_code,
        f"    b {cond_label}",
        f"{end_label}:"
    ]
    
    assembly_code = "\n".join(lines)
    return (assembly_code, next_offset)

# === helper functions ===

# === OOP compatibility layer ===
