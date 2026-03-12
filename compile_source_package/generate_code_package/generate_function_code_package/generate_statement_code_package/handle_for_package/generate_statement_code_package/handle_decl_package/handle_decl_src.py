# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields for DECL:
# {
#   "type": "DECL",
#   "var_name": str,
#   "var_type": str,
#   "init_value": dict
# }

# === main function ===
def handle_decl(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    DEVICE_SIZES = {
        "char": 1,
        "short": 2,
        "int": 4,
        "float": 4,
        "double": 8,
        "long": 4,
        "pointer": 4,
    }
    
    var_name = stmt.get("var_name")
    var_type = stmt.get("var_type", "int")
    init_value = stmt.get("init_value")
    
    if var_type not in DEVICE_SIZES:
        raise ValueError(f"Unsupported variable type: {var_type}")
    
    type_size = DEVICE_SIZES[var_type]
    current_offset = next_offset
    
    var_offsets[var_name] = current_offset
    
    if init_value is None:
        return "", current_offset + type_size
    
    expr_code, result_reg = generate_expression_code(
        init_value, func_name, label_counter, var_offsets
    )
    
    if type_size == 1:
        store_instr = f"STRB R{result_reg}, [SP, #{current_offset}]"
    elif type_size == 2:
        store_instr = f"STRH R{result_reg}, [SP, #{current_offset}]"
    elif type_size == 8:
        store_instr = f"STR R{result_reg}, [SP, #{current_offset}]\nSTR R{result_reg + 1}, [SP, #{current_offset + 4}]"
    else:
        store_instr = f"STR R{result_reg}, [SP, #{current_offset}]"
    
    if expr_code:
        full_code = f"{expr_code}\n{store_instr}"
    else:
        full_code = store_instr
    
    return full_code, current_offset + type_size

# === helper functions ===
# None

# === OOP compatibility layer ===
# None
