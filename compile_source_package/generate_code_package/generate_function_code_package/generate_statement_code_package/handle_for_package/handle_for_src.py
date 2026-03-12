# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code
from .generate_statement_code_package.generate_statement_code_src import generate_statement_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields for FOR:
# {
#   "type": "FOR",
#   "init": dict,
#   "condition": dict,
#   "update": dict,
#   "body": list,
# }

# === main function ===
def handle_for(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle FOR statement type. Generate init, condition, update, body with proper labels."""
    lines = []
    
    # Step 1: Get label counts
    cond_count = label_counter.get("for_cond", 0)
    end_count = label_counter.get("for_end", 0)
    update_count = label_counter.get("for_update", 0)
    
    # Step 2: Generate labels
    cond_label = f"{func_name}_for_cond_{cond_count}"
    end_label = f"{func_name}_for_end_{end_count}"
    update_label = f"{func_name}_for_update_{update_count}"
    
    # Step 3: Update label_counter in-place
    label_counter["for_cond"] = cond_count + 1
    label_counter["for_end"] = end_count + 1
    label_counter["for_update"] = update_count + 1
    
    # Step 4: Generate init code if present
    if stmt.get("init"):
        init_code, next_offset = generate_statement_code(stmt["init"], func_name, label_counter, var_offsets, next_offset)
        if init_code:
            lines.append(init_code)
    
    # Step 5: Add condition label
    lines.append(f"{cond_label}:")
    
    # Step 6-7: Generate condition code and branch
    if stmt.get("condition"):
        cond_code, next_offset = generate_expression_code(stmt["condition"], func_name, label_counter, var_offsets, next_offset)
        if cond_code:
            lines.append(cond_code)
        lines.append(f"cbz x0, {end_label}")
    
    # Step 8: Generate body statements
    for body_stmt in stmt.get("body", []):
        body_code, next_offset = generate_statement_code(body_stmt, func_name, label_counter, var_offsets, next_offset)
        if body_code:
            lines.append(body_code)
    
    # Step 9: Add update label
    lines.append(f"{update_label}:")
    
    # Step 10: Generate update code if present
    if stmt.get("update"):
        update_code, next_offset = generate_statement_code(stmt["update"], func_name, label_counter, var_offsets, next_offset)
        if update_code:
            lines.append(update_code)
    
    # Step 11: Loop back to condition
    lines.append(f"b {cond_label}")
    
    # Step 12: Add end label
    lines.append(f"{end_label}:")
    
    # Step 13: Return joined code
    return ("\n".join(lines), next_offset)

# === helper functions ===

# === OOP compatibility layer ===
