# === std / third-party imports ===
# No imports needed for this simple calculation

# === sub function imports ===
# No sub functions needed for this simple calculation

# === ADT defines ===
# No complex ADT needed; using primitive int types
# Input: param_count (int), local_var_count (int)
# Output: stack_size (int) - 16-byte aligned stack frame size in bytes

# === main function ===
def calculate_stack_size(param_count: int, local_var_count: int) -> int:
    """
    Calculate function stack frame size with 16-byte alignment.
    
    Args:
        param_count: Number of function parameters
        local_var_count: Number of local variables (VAR_DECL statements)
    
    Returns:
        Stack frame size in bytes, aligned to 16-byte boundary
    """
    total_slots = _calculate_total_slots(param_count, local_var_count)
    raw_size = _calculate_raw_size(total_slots)
    aligned_size = _align_to_16_bytes(raw_size)
    return aligned_size

# === helper functions ===
def _calculate_total_slots(param_count: int, local_var_count: int) -> int:
    """Calculate total slot count (params + local vars)."""
    return param_count + local_var_count

def _calculate_raw_size(total_slots: int) -> int:
    """Calculate raw size in bytes (8 bytes per slot)."""
    return total_slots * 8

def _align_to_16_bytes(raw_size: int) -> int:
    """
    Align size to 16-byte boundary.
    If already aligned, return as-is; otherwise round up to next 16-byte multiple.
    """
    if raw_size % 16 == 0:
        return raw_size
    else:
        return raw_size + 8

# === OOP compatibility layer ===
# Not needed for this utility function