# === std / third-party imports ===
from typing import Any, Dict, List, Tuple

# === sub function imports ===
# Note: Using lazy imports to avoid circular dependency with generate_statement_code

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
#   "else_body": list
# }

# === main function ===
def handle_if(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for an IF statement with optional else branch."""
    # Lazy imports to avoid circular dependency
    from .generate_expression_code_package.generate_expression_code_src import generate_expression_code
    from .generate_statement_code_package.generate_statement_code_src import generate_statement_code
    
    # Extract body lists
    then_body: List[Stmt] = stmt.get("then_body", [])
    else_body: List[Stmt] = stmt.get("else_body", [])
    has_else: bool = bool(else_body)
    
    # Generate unique labels (read-then-increment pattern)
    if has_else:
        else_num = label_counter.get("if_else", 0)
        label_counter["if_else"] = else_num + 1
        else_label = f"{func_name}_if_{else_num}_else"
    
    end_num = label_counter.get("if_end", 0)
    label_counter["if_end"] = end_num + 1
    end_label = f"{func_name}_if_{end_num}_end"
    
    # Evaluate condition (result in R0)
    condition: dict = stmt["condition"]
    cond_code, offset_after_cond = generate_expression_code(
        condition, func_name, label_counter, var_offsets, next_offset
    )
    
    # Build code lines
    code_lines: List[str] = []
    code_lines.append(cond_code)
    code_lines.append("CMP R0, #0")
    
    current_offset = offset_after_cond
    
    # Branch to else (or end if no else)
    if has_else:
        code_lines.append(f"B.EQ {else_label}")
    else:
        code_lines.append(f"B.EQ {end_label}")
    
    # Process then_body
    then_code_parts: List[str] = []
    for s in then_body:
        stmt_code, current_offset = generate_statement_code(
            s, func_name, label_counter, var_offsets, current_offset
        )
        then_code_parts.append(stmt_code)
    
    code_lines.append("\n".join(then_code_parts))
    
    # Handle else branch
    if has_else:
        code_lines.append(f"B {end_label}")
        code_lines.append(f"{else_label}:")
        
        else_code_parts: List[str] = []
        for s in else_body:
            stmt_code, current_offset = generate_statement_code(
                s, func_name, label_counter, var_offsets, current_offset
            )
            else_code_parts.append(stmt_code)
        
        code_lines.append("\n".join(else_code_parts))
    
    # End label
    code_lines.append(f"{end_label}:")
    
    return "\n".join(code_lines), current_offset

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
