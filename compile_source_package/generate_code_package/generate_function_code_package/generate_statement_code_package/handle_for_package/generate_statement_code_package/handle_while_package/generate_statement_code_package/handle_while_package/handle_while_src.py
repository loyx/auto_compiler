# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .evaluate_expression_package.evaluate_expression_src import evaluate_expression
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
#   "type": "WHILE",
#   "condition": dict,
#   "body": list,
# }

# === main function ===
def handle_while(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM32 assembly for WHILE loop statement."""
    condition = stmt["condition"]
    body = stmt["body"]
    
    # Generate unique labels using label_counter (modify in-place)
    cond_idx = label_counter.get("while_cond", 0)
    end_idx = label_counter.get("while_end", 0)
    cond_label = f"{func_name}_while_cond_{cond_idx}"
    end_label = f"{func_name}_while_end_{end_idx}"
    label_counter["while_cond"] = cond_idx + 1
    label_counter["while_end"] = end_idx + 1
    
    # Build assembly code
    lines = []
    offset = next_offset
    
    # Emit condition label
    lines.append(f"{cond_label}:")
    
    # Evaluate condition into r0
    cond_code, offset = evaluate_expression(condition, func_name, var_offsets, offset)
    lines.append(cond_code)
    
    # Branch to end if condition is false (r0 == 0)
    lines.append(f"    cmp r0, #0")
    lines.append(f"    beq {end_label}")
    
    # Generate body statements
    for body_stmt in body:
        body_code, offset = generate_statement_code(body_stmt, func_name, label_counter, var_offsets, offset)
        lines.append(body_code)
    
    # Branch back to condition
    lines.append(f"    b {cond_label}")
    
    # Emit end label
    lines.append(f"{end_label}:")
    
    assembly = "\n".join(lines)
    return (assembly, offset)

# === helper functions ===

# === OOP compatibility layer ===
