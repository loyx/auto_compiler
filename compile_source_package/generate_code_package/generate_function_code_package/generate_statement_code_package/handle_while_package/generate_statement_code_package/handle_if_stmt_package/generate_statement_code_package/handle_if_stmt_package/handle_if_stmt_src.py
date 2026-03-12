# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code
from ..generate_statement_code_package.generate_statement_code_src import generate_statement_code

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
def handle_if_stmt(stmt: Stmt, func_name: str, label_counter: LabelCounter, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate assembly code for if-else statement with proper branching and labels."""
    condition = stmt["condition"]
    then_body = stmt["then_body"]
    else_body = stmt.get("else_body")
    
    # Generate unique labels using label_counter (increment after use)
    else_label = f"{func_name}_if_else_{label_counter['if_else']}"
    label_counter['if_else'] += 1
    end_label = f"{func_name}_if_end_{label_counter['if_end']}"
    label_counter['if_end'] += 1
    
    # Generate condition expression code (result in x0)
    code, next_offset = generate_expression_code(condition, var_offsets, next_offset)
    
    # Emit cbz to skip then_body if condition is false
    code += f"cbz x0, {else_label}\n"
    
    # Generate code for then_body statements
    for s in then_body:
        body_code, next_offset = generate_statement_code(s, func_name, label_counter, var_offsets, next_offset)
        code += body_code
    
    # If else_body exists, emit jump to end and else branch
    if else_body:
        code += f"b {end_label}\n"
        code += f"{else_label}:\n"
        for s in else_body:
            body_code, next_offset = generate_statement_code(s, func_name, label_counter, var_offsets, next_offset)
            code += body_code
    
    # Emit end label
    code += f"{end_label}:\n"
    
    return code, next_offset

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
