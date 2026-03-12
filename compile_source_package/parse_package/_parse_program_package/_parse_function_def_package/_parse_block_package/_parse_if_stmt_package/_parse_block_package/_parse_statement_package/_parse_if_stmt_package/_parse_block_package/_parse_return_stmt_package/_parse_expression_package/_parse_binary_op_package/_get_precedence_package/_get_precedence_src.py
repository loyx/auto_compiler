# === std / third-party imports ===
from typing import Dict

# === sub function imports ===
# No sub functions needed

# === ADT defines ===
# No complex ADT needed - simple string to int mapping

# === main function ===
def _get_precedence(op_type: str) -> int:
    """
    Get operator precedence level.
    
    Args:
        op_type: Operator type string (e.g., "OR", "AND", "PLUS", "MUL", "POWER")
    
    Returns:
        Precedence level (1-6), or 0 for unknown operators.
        
    Precedence mapping (low to high):
        - OR: 1
        - AND: 2
        - EQ, NEQ, LT, LTE, GT, GTE: 3
        - PLUS, MINUS: 4
        - MUL, DIV, MOD: 5
        - POWER: 6
    """
    precedence_map: Dict[str, int] = {
        "OR": 1,
        "AND": 2,
        "EQ": 3,
        "NEQ": 3,
        "LT": 3,
        "LTE": 3,
        "GT": 3,
        "GTE": 3,
        "PLUS": 4,
        "MINUS": 4,
        "MUL": 5,
        "DIV": 5,
        "MOD": 5,
        "POWER": 6,
    }
    
    return precedence_map.get(op_type, 0)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed - this is a simple utility function
