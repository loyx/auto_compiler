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
#   "body": list,
# }

# === main function ===
def handle_while_stmt(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle while loop code generation."""
    # Generate unique labels using current counter values, then increment
    cond_label = f"{func_name}_while_cond_{label_counter['while_cond']}"
    label_counter['while_cond'] += 1
    
    end_label = f"{func_name}_while_end_{label_counter['while_end']}"
    label_counter['while_end'] += 1
    
    # Start with condition label
    code_lines = [f"{cond_label}:"]
    
    # Generate condition expression code (result in x0)
    condition = stmt.get("condition", {})
    cond_code, next_offset = generate_expression_code(condition, var_offsets, next_offset)
    code_lines.append(cond_code)
    
    # Emit cbz to exit loop if condition is false
    code_lines.append(f"cbz x0, {end_label}")
    
    # Generate code for body statements
    body = stmt.get("body", [])
    for body_stmt in body:
        body_code, next_offset = generate_statement_code(body_stmt, func_name, label_counter, var_offsets, next_offset)
        code_lines.append(body_code)
    
    # Emit branch back to condition check
    code_lines.append(f"b {cond_label}")
    
    # Emit end label
    code_lines.append(f"{end_label}:")
    
    # Join all lines with newlines
    assembly_code = "\n".join(code_lines) + "\n"
    
    return (assembly_code, next_offset)

# === helper functions ===

# === OOP compatibility layer ===
