# === std / third-party imports ===
from typing import Dict, Any, Tuple

# === sub function imports ===
# No sub functions - inline implementation

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

Expression = Dict[str, Any]
# Expression possible fields:
# {
#   "type": str,  # "LITERAL" | "VAR" | "BINOP" | "UNOP" | "CALL"
#   "value": int,  # for LITERAL
#   "name": str,  # for VAR
#   "op": str,  # for BINOP/UNOP
#   "left": dict,  # for BINOP
#   "right": dict,  # for BINOP
#   "operand": dict,  # for UNOP
#   "func_name": str,  # for CALL
#   "args": list,  # for CALL
# }

# === main function ===
def generate_expression_code(expr: Expression, func_name: str, label_counter: LabelCounter, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for an expression. Result placed in R0."""
    expr_type = expr["type"]
    
    if expr_type == "LITERAL":
        value = expr["value"]
        if 0 <= value <= 4095:
            return f"    MOV R0, #{value}\n", next_offset
        else:
            return f"    MVN R0, #{~value & 0xFFFFFFFF}\n", next_offset
    
    elif expr_type == "VAR":
        var_name = expr["name"]
        offset = var_offsets[var_name]
        return f"    LDR R0, [SP, #{offset}]\n", next_offset
    
    elif expr_type == "BINOP":
        op = expr["op"]
        left = expr["left"]
        right = expr["right"]
        
        left_code, offset_after_left = generate_expression_code(left, func_name, label_counter, var_offsets, next_offset)
        save_code = f"    STR R0, [SP, #{offset_after_left}]\n"
        right_code, offset_after_right = generate_expression_code(right, func_name, label_counter, var_offsets, offset_after_left + 4)
        
        op_map = {"ADD": "ADD", "SUB": "SUB", "MUL": "MUL", "DIV": "SDIV", 
                  "AND": "AND", "ORR": "ORR", "EOR": "EOR"}
        cmp_map = {"EQ": "CMP", "NE": "CMP", "LT": "CMP", "LE": "CMP", "GT": "CMP", "GE": "CMP"}
        
        if op in op_map:
            asm_op = op_map[op]
            result_code = f"    {asm_op} R0, R0, R1\n"
        elif op in cmp_map:
            cmp_code = f"    CMP R0, R1\n"
            cond_map = {"EQ": "EQ", "NE": "NE", "LT": "LT", "LE": "LE", "GT": "GT", "GE": "GE"}
            result_code = f"{cmp_code}    MOV R0, #0\n    MOV{cond_map[op]} R0, #1\n"
        else:
            raise ValueError(f"Unknown binary operator: {op}")
        
        return f"{left_code}{save_code}{right_code}{result_code}", offset_after_right
    
    elif expr_type == "UNOP":
        op = expr["op"]
        operand = expr["operand"]
        
        operand_code, new_offset = generate_expression_code(operand, func_name, label_counter, var_offsets, next_offset)
        
        if op == "NEG":
            result_code = "    RSBS R0, R0, #0\n"
        elif op == "NOT":
            result_code = "    MVN R0, R0\n"
        elif op == "LNOT":
            result_code = "    CMP R0, #0\n    MOV R0, #0\n    MOV EQ R0, #1\n"
        else:
            raise ValueError(f"Unknown unary operator: {op}")
        
        return f"{operand_code}{result_code}", new_offset
    
    elif expr_type == "CALL":
        call_func = expr["func_name"]
        args = expr["args"]
        
        arg_codes = []
        offset = next_offset
        for i, arg in enumerate(reversed(args)):
            arg_code, offset = generate_expression_code(arg, func_name, label_counter, var_offsets, offset)
            arg_codes.append(f"{arg_code}    STR R0, [SP, #{offset - 4}]\n")
        
        arg_codes.reverse()
        args_count = len(args)
        call_code = f"    BL {call_func}\n"
        
        return "".join(arg_codes) + call_code, offset
    
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions - all logic in main

# === OOP compatibility layer ===
# Not needed - this is a pure function node