# === std / third-party imports ===
from typing import Dict

# === sub function imports ===

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
#   "if_end": int,
#   "if_else": int,
#   "and": int,
#   "or": int,
# }

# === main function ===
def generate_binop(op: str, label_counter: LabelCounter) -> str:
    """
    Generate ARM32 assembly code for binary operations.
    Assumes left operand in r1, right operand in r0. Result placed in r0.
    """
    # Arithmetic operators
    if op == "+":
        return "add r0, r1, r0"
    elif op == "-":
        return "sub r0, r1, r0"
    elif op == "*":
        return "mul r0, r1, r0"
    elif op == "/":
        return "sdiv r0, r1, r0"
    
    # Comparison operators
    elif op == "==":
        return (
            "cmp r1, r0\n"
            "moveq r0, #1\n"
            "movne r0, #0"
        )
    elif op == "!=":
        return (
            "cmp r1, r0\n"
            "movne r0, #1\n"
            "moveq r0, #0"
        )
    elif op == "<":
        return (
            "cmp r1, r0\n"
            "movlt r0, #1\n"
            "movge r0, #0"
        )
    elif op == ">":
        return (
            "cmp r1, r0\n"
            "movgt r0, #1\n"
            "movle r0, #0"
        )
    elif op == "<=":
        return (
            "cmp r1, r0\n"
            "movle r0, #1\n"
            "movgt r0, #0"
        )
    elif op == ">=":
        return (
            "cmp r1, r0\n"
            "movge r0, #1\n"
            "movlt r0, #0"
        )
    
    # Logical operators with short-circuit evaluation
    elif op == "and":
        counter = label_counter.get("and", 0)
        label_counter["and"] = counter + 1
        false_label = f"_and_false_{counter}"
        end_label = f"_and_end_{counter}"
        return (
            f"cmp r1, #0\n"
            f"beq {false_label}\n"
            f"cmp r0, #0\n"
            f"beq {false_label}\n"
            f"mov r0, #1\n"
            f"b {end_label}\n"
            f"{false_label}:\n"
            f"mov r0, #0\n"
            f"{end_label}:"
        )
    elif op == "or":
        counter = label_counter.get("or", 0)
        label_counter["or"] = counter + 1
        true_label = f"_or_true_{counter}"
        end_label = f"_or_end_{counter}"
        return (
            f"cmp r1, #0\n"
            f"bne {true_label}\n"
            f"cmp r0, #0\n"
            f"bne {true_label}\n"
            f"mov r0, #0\n"
            f"b {end_label}\n"
            f"{true_label}:\n"
            f"mov r0, #1\n"
            f"{end_label}:"
        )
    
    # Unknown operator
    else:
        raise ValueError(f"Unknown binary operator: {op}")

# === helper functions ===

# === OOP compatibility layer ===
