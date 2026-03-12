# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .evaluate_expression_package.evaluate_expression_src import evaluate_expression

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
#   "body": list
# }

# === main function ===
def handle_for(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for a FOR loop statement."""
    # Generate unique labels using label_counter
    cond_idx = label_counter.get("for_cond", 0)
    end_idx = label_counter.get("for_end", 0)
    update_idx = label_counter.get("for_update", 0)
    
    cond_label = f".L_for_cond_{cond_idx}"
    end_label = f".L_for_end_{end_idx}"
    update_label = f".L_for_update_{update_idx}"
    
    # Increment label counters in-place
    label_counter["for_cond"] = cond_idx + 1
    label_counter["for_end"] = end_idx + 1
    label_counter["for_update"] = update_idx + 1
    
    code_parts = []
    
    # --- INIT section ---
    init_stmt = stmt.get("init")
    if init_stmt:
        from .. import generate_statement_code
        init_code, next_offset = generate_statement_code(
            init_stmt, func_name, label_counter, var_offsets, next_offset
        )
        code_parts.append(init_code)
    
    # --- CONDITION label and check ---
    code_parts.append(f"{cond_label}:")
    
    condition_expr = stmt.get("condition")
    if condition_expr:
        cond_code = evaluate_expression(condition_expr, var_offsets)
        code_parts.append(cond_code)
        code_parts.append("    cmp r0, #0")
        code_parts.append(f"    beq {end_label}")
    
    # --- BODY section ---
    body_stmts = stmt.get("body", [])
    from .. import generate_statement_code
    for body_stmt in body_stmts:
        body_code, next_offset = generate_statement_code(
            body_stmt, func_name, label_counter, var_offsets, next_offset
        )
        code_parts.append(body_code)
    
    # --- UPDATE section ---
    code_parts.append(f"{update_label}:")
    update_stmt = stmt.get("update")
    if update_stmt:
        update_code, next_offset = generate_statement_code(
            update_stmt, func_name, label_counter, var_offsets, next_offset
        )
        code_parts.append(update_code)
    
    # --- Branch back to condition ---
    code_parts.append(f"    b {cond_label}")
    
    # --- END label ---
    code_parts.append(f"{end_label}:")
    
    return "\n".join(code_parts), next_offset

# === helper functions ===
# No helper functions needed; logic is delegated to child functions

# === OOP compatibility layer ===
# No OOP wrapper needed; this is a plain function node
