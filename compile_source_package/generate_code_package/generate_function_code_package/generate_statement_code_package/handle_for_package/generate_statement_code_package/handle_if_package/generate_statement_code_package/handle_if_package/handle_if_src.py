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
# Stmt possible fields:
# {
#   "type": str,
#   "condition": dict,
#   "then_body": list,
#   "else_body": list,
# }

# === main function ===
def handle_if(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly for IF-THEN-ELSE conditional branching."""
    asm_lines = []
    offset = next_offset
    
    # Generate unique labels using read-then-increment pattern
    else_label_num = label_counter.get("if_else", 0)
    label_counter["if_else"] = else_label_num + 1
    end_label_num = label_counter.get("if_end", 0)
    label_counter["if_end"] = end_label_num + 1
    
    else_label = f"{func_name}_if_else_{else_label_num}"
    end_label = f"{func_name}_if_end_{end_label_num}"
    
    # Generate condition evaluation code (result in R0)
    condition = stmt.get("condition", {})
    cond_asm, _, offset = generate_expression_code(condition, var_offsets, offset)
    asm_lines.append(cond_asm)
    
    # Generate: CMP R0, #0; B.EQ <else_label>
    asm_lines.append("CMP R0, #0")
    asm_lines.append(f"B.EQ {else_label}")
    
    # Generate then_body code
    then_body = stmt.get("then_body", [])
    for then_stmt in then_body:
        stmt_asm, offset = generate_statement_code(then_stmt, func_name, label_counter, var_offsets, offset)
        asm_lines.append(stmt_asm)
    
    # Generate: B <end_label>
    asm_lines.append(f"B {end_label}")
    
    # Generate else_label: and else_body code (if else_body not empty)
    asm_lines.append(f"{else_label}:")
    else_body = stmt.get("else_body", [])
    for else_stmt in else_body:
        stmt_asm, offset = generate_statement_code(else_stmt, func_name, label_counter, var_offsets, offset)
        asm_lines.append(stmt_asm)
    
    # Generate end_label:
    asm_lines.append(f"{end_label}:")
    
    # Join all assembly lines and return
    asm_code = "\n".join(asm_lines)
    return (asm_code, offset)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
