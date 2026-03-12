# === std / third-party imports ===
# No imports needed

# === sub function imports ===
# No child functions

# === ADT defines ===
# No complex ADTs; using basic types only
# Input: func_name (str), stack_size (int)
# Output: str (assembly code with 4-space indent per line)

# === main function ===
def generate_prologue(func_name: str, stack_size: int) -> str:
    """Generate ARM64 function prologue assembly code.
    
    Args:
        func_name: Name of the function (not used in prologue generation)
        stack_size: Stack frame size in bytes (must be 16-byte aligned)
    
    Returns:
        Assembly code string with three instructions, each prefixed with 4 spaces
    """
    lines = [
        "    stp fp, lr, [sp, #-16]!",
        "    mov fp, sp",
        f"    sub sp, sp, #{stack_size}",
    ]
    return "\n".join(lines)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node
