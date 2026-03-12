# === std / third-party imports ===
# No imports needed - this function uses primitive types only

# === sub function imports ===
# No sub functions needed for this simple utility

# === ADT defines ===
# No ADT needed - this function uses primitive types only
# Input: value_str (str)
# Output: str

# === main function ===
def _parse_string_value(value_str: str) -> str:
    """
    去除字符串字面量的引号，返回实际内容。
    
    支持双引号字符串 '"hello"' -> 'hello'
    支持单引号字符串 "'world'" -> 'world'
    
    注意：此函数不处理转义字符，仅简单去除首尾引号。
    """
    if len(value_str) >= 2:
        return value_str[1:-1]
    else:
        return value_str

# === helper functions ===
# No helper functions needed - logic is simple enough

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a simple utility function
