# === std / third-party imports ===
from typing import Any

# === sub function imports ===
# No sub functions needed - INLINE implementation

# === ADT defines ===
# No ADT needed - using simple str -> Any conversion
# Input: value (str) - raw string from LITERAL token
# Output: Any - converted Python value (int, float, or str)

# === main function ===
def convert_literal_value(value: str) -> Any:
    """
    Convert LITERAL token's raw string value to Python type.
    
    Args:
        value: Raw string value from LITERAL token
        
    Returns:
        Converted Python value (int, float, or str)
        
    Conversion Rules:
        1. String literal: if value starts and ends with ", strip quotes
        2. Float: if value contains '.' or 'e'/'E', convert to float
        3. Int: otherwise convert to int
    """
    # Check if it's a string literal (quoted)
    if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    
    # Check if it's a float (contains '.' or 'e'/'E')
    if '.' in value or 'e' in value.lower():
        return float(value)
    
    # Default to int
    return int(value)

# === helper functions ===
# No helper functions needed - logic is simple and self-contained

# === OOP compatibility layer ===
# Not needed - this is a utility function, not a framework entry point
