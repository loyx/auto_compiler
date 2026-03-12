# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "if_else": int,
#   "if_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields for IF:
# {
#   "type": "IF",
#   "condition": dict,       # Expression dict
#   "then_body": list,       # List of Stmt
#   "else_body": list,       # List of Stmt (optional)
# }

# === main function ===
def handle_if(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle IF statement type. Generate condition code, then/else branches with proper labels."""
    code = ""
    
    # Get current label counts
    else_count = label_counter.get("if_else", 0)
    end_count = label_counter.get("if_end", 0)
    
    # Generate label names
    else_label = f"{func_name}_else_{else_count}"
    end_label = f"{func_name}_end_{end_count}"
    
    # Get condition
    condition = stmt.get("condition")
    if condition is None:
        code += "    // ERROR: IF missing condition\n"
        label_counter["if_else"] = else_count + 1
        label_counter["if_end"] = end_count + 1
        return code, next_offset
    
    # Generate condition code
    cond_code, next_offset, cond_reg = generate_expression_code(condition, var_offsets, next_offset)
    code += cond_code
    
    # Jump to else if condition is false (zero)
    code += f"    cbz {cond_reg}, {else_label}\n"
    
    # Process then_body statements
    then_body = stmt.get("then_body", [])
    # Lazy import to avoid circular dependency
    from .generate_statement_code_package.generate_statement_code_src import generate_statement_code
    for then_stmt in then_body:
        stmt_code, next_offset = generate_statement_code(then_stmt, func_name, label_counter, var_offsets, next_offset)
        code += stmt_code
    
    # Handle else_body
    else_body = stmt.get("else_body")
    if else_body:
        # Jump to end after then_body
        code += f"    b {end_label}\n"
        # Add else label
        code += f"{else_label}:\n"
        # Process else_body statements
        for else_stmt in else_body:
            stmt_code, next_offset = generate_statement_code(else_stmt, func_name, label_counter, var_offsets, next_offset)
            code += stmt_code
        # Add end label
        code += f"{end_label}:\n"
    else:
        # No else branch, just add end label
        code += f"{end_label}:\n"
    
    # Update label counter
    label_counter["if_else"] = else_count + 1
    label_counter["if_end"] = end_count + 1
    
    return code, next_offset

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node
