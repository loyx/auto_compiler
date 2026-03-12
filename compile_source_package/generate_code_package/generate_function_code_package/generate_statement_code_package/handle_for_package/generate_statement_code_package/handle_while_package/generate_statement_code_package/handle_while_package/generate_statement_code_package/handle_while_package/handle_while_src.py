# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# Special architectural exception: import parent function for recursive statement processing
from ..generate_statement_code_src import generate_statement_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
#   "if_end": int,
#   "if_else": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,  # "ASSIGN", "IF", "WHILE", "RETURN", "EXPR"
#   "var_name": str,  # for ASSIGN
#   "value": dict,  # for ASSIGN
#   "condition": dict,  # for IF/WHILE
#   "then_body": list,  # for IF
#   "else_body": list,  # for IF
#   "body": list,  # for WHILE
#   "expression": dict,  # for RETURN/EXPR
# }

# === main function ===
def handle_while(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM32 assembly code for a WHILE statement."""
    # Allocate labels
    cond_counter = label_counter.get("while_cond", 0)
    end_counter = label_counter.get("while_end", 0)
    label_counter["while_cond"] = cond_counter + 1
    label_counter["while_end"] = end_counter + 1
    
    cond_label = f"{func_name}_while_cond_{cond_counter}"
    end_label = f"{func_name}_while_end_{end_counter}"
    
    code_lines = []
    
    # Condition label
    code_lines.append(f"{cond_label}:")
    
    # Evaluate condition expression
    condition = stmt.get("condition", {})
    cond_code, offset = _generate_expression_code(condition, func_name, label_counter, var_offsets, next_offset)
    code_lines.append(cond_code)
    
    # Compare with 0 and branch to end if false
    code_lines.append("    cmp r0, #0")
    code_lines.append(f"    beq {end_label}")
    
    # Process body statements
    offset = next_offset
    body = stmt.get("body", [])
    for s in body:
        body_code, offset = generate_statement_code(s, func_name, label_counter, var_offsets, offset)
        code_lines.append(body_code)
    
    # Branch back to condition
    code_lines.append(f"    b {cond_label}")
    
    # End label
    code_lines.append(f"{end_label}:")
    
    assembly_code = "\n".join(code_lines)
    return (assembly_code, offset)

# === helper functions ===
def _generate_expression_code(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """
    Generate assembly code for evaluating an expression.
    Result is placed in r0.
    This is a placeholder - actual implementation depends on expression type.
    """
    # Placeholder: assumes expression evaluation returns value in r0
    # In a full implementation, this would delegate to expression handlers
    return ("    @ evaluate expression (placeholder)", next_offset)

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
