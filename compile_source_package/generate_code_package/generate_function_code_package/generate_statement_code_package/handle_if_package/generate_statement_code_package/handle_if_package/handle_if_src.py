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
#   "condition": dict,
#   "then_body": list,
#   "else_body": list,
# }

# === main function ===
def handle_if(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle IF statement: generate condition code, branches, then/else body code, and labels."""
    # Generate unique labels using current count, then increment
    else_label = f"{func_name}_if_else_{label_counter['if_else']}"
    label_counter['if_else'] += 1
    end_label = f"{func_name}_if_end_{label_counter['if_end']}"
    label_counter['if_end'] += 1
    
    lines = []
    
    # Generate condition evaluation code
    condition = stmt.get("condition", {})
    cond_code, next_offset, cond_reg = generate_expression_code(condition, var_offsets, next_offset)
    if cond_code:
        lines.append(cond_code)
    
    # Conditional jump to else (if condition is false/zero)
    lines.append(f"    JZ {else_label}")
    
    # Generate then_body statements
    then_body = stmt.get("then_body", [])
    for s in then_body:
        code, next_offset = generate_statement_code(s, func_name, label_counter, var_offsets, next_offset)
        if code:
            lines.append(code)
    
    # Unconditional jump to end
    lines.append(f"    B {end_label}")
    
    # Else label
    lines.append(f"{else_label}:")
    
    # Generate else_body statements (if any)
    else_body = stmt.get("else_body", [])
    if else_body:
        for s in else_body:
            code, next_offset = generate_statement_code(s, func_name, label_counter, var_offsets, next_offset)
            if code:
                lines.append(code)
    
    # End label
    lines.append(f"{end_label}:")
    
    return ("\n".join(lines), next_offset)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
