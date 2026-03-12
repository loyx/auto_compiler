# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions for this inline implementation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,  # "literal", "variable", "binop"
#   "value": int,  # for literal
#   "var_name": str,  # for variable
#   "op": str,  # for binop: "add", "sub", "mul", "div", "lt", "gt", "eq", "and", "or"
#   "left": dict,  # for binop
#   "right": dict,  # for binop
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets) -> str:
    """Generate ARM assembly code to evaluate expression with result in R0."""
    expr_type = expr.get("type")
    
    if expr_type == "literal":
        value = expr.get("value", 0)
        return f"    MOV R0, #{value}"
    
    elif expr_type == "variable":
        var_name = expr.get("var_name", "")
        offset = var_offsets.get(var_name, 0)
        return f"    LDR R0, [SP, #{offset}]"
    
    elif expr_type == "binop":
        op = expr.get("op", "")
        left = expr.get("left", {})
        right = expr.get("right", {})
        
        left_code = generate_expression_code(left, var_offsets)
        right_code = generate_expression_code(right, var_offsets)
        
        lines = [left_code, "    PUSH {R0}", right_code, "    POP {R1}"]
        
        if op == "add":
            lines.append("    ADD R0, R1, R0")
        elif op == "sub":
            lines.append("    SUB R0, R1, R0")
        elif op == "mul":
            lines.append("    MUL R0, R1, R0")
        elif op == "div":
            lines.append("    SDIV R0, R1, R0")
        elif op == "lt":
            lines.append("    CMP R1, R0")
            lines.append("    MOVLT R0, #1")
            lines.append("    MOVGE R0, #0")
        elif op == "gt":
            lines.append("    CMP R1, R0")
            lines.append("    MOVGT R0, #1")
            lines.append("    MOVLE R0, #0")
        elif op == "eq":
            lines.append("    CMP R1, R0")
            lines.append("    MOVEQ R0, #1")
            lines.append("    MOVNE R0, #0")
        elif op == "and":
            lines.append("    AND R0, R1, R0")
        elif op == "or":
            lines.append("    ORR R0, R1, R0")
        else:
            raise ValueError(f"Unknown operator: {op}")
        
        return "\n".join(lines)
    
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# Not needed for this function node
