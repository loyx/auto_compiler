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
    """Generate assembly code for IF statement."""
    code_lines = []
    
    # Generate unique labels
    if_else_idx = label_counter.get("if_else", 0)
    if_end_idx = label_counter.get("if_end", 0)
    
    if_else_label = f"{func_name}_if_else_{if_else_idx}"
    if_end_label = f"{func_name}_if_end_{if_end_idx}"
    
    # Update label counters
    label_counter["if_else"] = if_else_idx + 1
    label_counter["if_end"] = if_end_idx + 1
    
    # Generate condition expression code
    condition = stmt.get("condition", {})
    cond_code, cond_offset, next_offset = generate_expression_code(
        condition, var_offsets, next_offset
    )
    code_lines.append(cond_code)
    
    # Emit JZ instruction to jump to else/end if condition is false (zero)
    has_else = stmt.get("else_body") and len(stmt.get("else_body", [])) > 0
    jump_target = if_else_label if has_else else if_end_label
    code_lines.append(f"    JZ {jump_target}")
    
    # Process then_body statements
    then_body = stmt.get("then_body", [])
    for then_stmt in then_body:
        stmt_code, next_offset = generate_statement_code(
            then_stmt, func_name, label_counter, var_offsets, next_offset
        )
        code_lines.append(stmt_code)
    
    # If else_body exists, emit jump to end and process else_body
    if has_else:
        code_lines.append(f"    JMP {if_end_label}")
        code_lines.append(f"{if_else_label}:")
        
        else_body = stmt.get("else_body", [])
        for else_stmt in else_body:
            stmt_code, next_offset = generate_statement_code(
                else_stmt, func_name, label_counter, var_offsets, next_offset
            )
            code_lines.append(stmt_code)
    
    # Emit end label
    code_lines.append(f"{if_end_label}:")
    
    # Combine all code lines
    assembly_code = "\n".join(code_lines)
    
    return (assembly_code, next_offset)

# === helper functions ===

# === OOP compatibility layer ===
