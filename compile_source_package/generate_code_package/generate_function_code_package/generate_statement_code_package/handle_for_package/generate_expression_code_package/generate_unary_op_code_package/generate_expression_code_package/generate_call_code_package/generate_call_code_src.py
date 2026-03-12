# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "counter": int,
# }

Expression = Dict[str, Any]
# Expression possible fields:
# {
#   "type": str,
#   "function": Dict,  # For CALL - function name expression
#   "arguments": list,  # For CALL - list of argument expressions
#   "name": str,  # For IDENTIFIER
#   "value": Any,  # For LITERAL
#   "literal_type": str,  # For LITERAL
#   "operator": str,  # For BINARY_OP/UNARY_OP
#   "left": Dict,  # For BINARY_OP
#   "right": Dict,  # For BINARY_OP
#   "operand": Dict,  # For UNARY_OP
# }

# === main function ===
def generate_call_code(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 assembly code for function calls per AAPCS convention."""
    lines = []
    current_offset = next_offset
    
    # Extract function expression and arguments
    func_expr = expr.get("function", {})
    arguments = expr.get("arguments", [])
    
    # Step 1: Generate code to evaluate function name expression (result in x0)
    func_code, current_offset = generate_expression_code(func_expr, func_name, label_counter, var_offsets, current_offset)
    lines.append(func_code)
    
    # Step 2: Evaluate each argument and place in x0-x7 or stack
    # Per AAPCS: first 8 args in x0-x7, rest on stack (right-to-left)
    num_args = len(arguments)
    stack_arg_start = 8  # Arguments beyond index 7 go on stack
    
    # Calculate stack space needed for arguments beyond x0-x7
    stack_args_count = max(0, num_args - stack_arg_start)
    
    # Process arguments left-to-right
    for i, arg_expr in enumerate(arguments):
        # Generate code for this argument (result in x0)
        arg_code, current_offset = generate_expression_code(arg_expr, func_name, label_counter, var_offsets, current_offset)
        lines.append(arg_code)
        
        if i < stack_arg_start:
            # Move result from x0 to appropriate argument register x{i}
            if i > 0:  # Skip if already in x0
                lines.append(f"    mov x{i}, x0")
        else:
            # Store on stack at computed offset
            # Stack grows downward; allocate space for all stack args first
            stack_slot_offset = (i - stack_arg_start) * 8
            lines.append(f"    str x0, [sp, #{stack_slot_offset}]")
    
    # Step 3: Generate call instruction
    # Extract function name if it's an IDENTIFIER
    if func_expr.get("type") == "IDENTIFIER":
        target_name = func_expr.get("name", "unknown")
        lines.append(f"    bl {target_name}")
    else:
        # Function address is already in x0 from evaluate func_expr
        # Use indirect call: blr x0
        lines.append("    blr x0")
    
    # Step 4: Update next_offset to account for stack space used
    # Stack space for arguments beyond x0-x7 (8 bytes each)
    stack_space_used = stack_args_count * 8
    updated_next_offset = next_offset + stack_space_used
    
    # Combine all code lines
    generated_code = "\n".join(filter(None, lines))
    
    return (generated_code, updated_next_offset)

# === helper functions ===
# No helper functions needed; logic is straightforward

# === OOP compatibility layer ===
# Not needed for this function node
