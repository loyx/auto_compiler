# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# Note: Using lazy imports to avoid circular dependency with generate_statement_code_src

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
#   "if_else": int,
#   "if_end": int,
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
#   "then_body": list,
#   "else_body": list,
# }

# === main function ===
def handle_if_stmt(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle IF statement by generating conditional branch assembly code."""
    # Lazy imports to avoid circular dependency
    from ..generate_expression_code_package.generate_expression_code_src import generate_expression_code
    from ..generate_statement_code_src import generate_statement_code
    
    # Extract components
    condition = stmt["condition"]
    then_body = stmt["then_body"]
    else_body = stmt.get("else_body", [])
    
    # Generate unique labels
    else_label = f"{func_name}_if_else_{label_counter['if_else']}"
    end_label = f"{func_name}_if_end_{label_counter['if_end']}"
    label_counter['if_else'] += 1
    label_counter['if_end'] += 1
    
    # Generate condition code
    cond_code, current_offset = generate_expression_code(condition, var_offsets, next_offset)
    
    # Determine branch target
    branch_target = else_label if else_body else end_label
    
    # Build code
    code_parts = []
    code_parts.append(cond_code)
    code_parts.append(f"cbz x0, {branch_target}\n")
    
    # Generate then_body code
    for stmt_item in then_body:
        stmt_code, current_offset = generate_statement_code(stmt_item, func_name, label_counter, var_offsets, current_offset)
        code_parts.append(stmt_code)
    
    # Handle else_body if exists
    if else_body:
        code_parts.append(f"b {end_label}\n")
        code_parts.append(f"{else_label}:\n")
        for stmt_item in else_body:
            stmt_code, current_offset = generate_statement_code(stmt_item, func_name, label_counter, var_offsets, current_offset)
            code_parts.append(stmt_code)
    
    code_parts.append(f"{end_label}:\n")
    
    return "".join(code_parts), current_offset

# === helper functions ===

# === OOP compatibility layer ===
