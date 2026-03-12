# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code
from ..generate_statement_code_src import generate_statement_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_body": int,
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
#   "type": str,           # "while"
#   "condition": dict,     # while condition expression
#   "body": list,          # while body statements
# }

# === main function ===
def handle_while_stmt(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle WHILE statement code generation."""
    condition = stmt.get("condition", {})
    body = stmt.get("body", [])
    
    # Generate unique labels (get current values before incrementing)
    cond_id = label_counter.get("while_cond", 0)
    body_id = label_counter.get("while_body", 0)
    end_id = label_counter.get("while_end", 0)
    
    # Modify label_counter in-place
    label_counter["while_cond"] = cond_id + 1
    label_counter["while_body"] = body_id + 1
    label_counter["while_end"] = end_id + 1
    
    # Build label names
    cond_label = f"{func_name}_while_cond_{cond_id}"
    body_label = f"{func_name}_while_body_{body_id}"
    end_label = f"{func_name}_while_end_{end_id}"
    
    # Start with condition label
    code = f"{cond_label}:\n"
    
    # Generate condition expression code
    cond_code, cond_offset, new_offset = generate_expression_code(condition, var_offsets, next_offset)
    code += cond_code
    
    # Jump to end if condition is false
    code += f"    JUMP_IF_FALSE {cond_offset}, {end_label}\n"
    
    # Body label
    code += f"{body_label}:\n"
    
    # Generate code for each body statement
    for body_stmt in body:
        stmt_code, new_offset = generate_statement_code(body_stmt, func_name, label_counter, var_offsets, new_offset)
        code += stmt_code
    
    # Jump back to condition check
    code += f"    JUMP {cond_label}\n"
    
    # End label
    code += f"{end_label}:\n"
    
    return code, new_offset

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node