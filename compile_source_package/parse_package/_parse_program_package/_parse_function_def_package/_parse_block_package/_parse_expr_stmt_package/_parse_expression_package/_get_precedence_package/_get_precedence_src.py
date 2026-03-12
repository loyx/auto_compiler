# === std / third-party imports ===
# No imports needed - uses only primitive types

# === sub function imports ===
# No child functions needed for this simple lookup

# === ADT defines ===
# No ADT needed - uses primitive types only
# Input: token_type (str), token_value (str)
# Output: precedence (int)

# === main function ===
def _get_precedence(token_type: str, token_value: str) -> int:
    """
    获取运算符优先级。
    
    输入：token_type 和 token_value
    输出：整数优先级（0=最低，越高优先级越高）。非运算符返回 0。
    
    优先级规则（从低到高）：
    - 逻辑或 (||): 1
    - 逻辑与 (&&): 2
    - 相等运算符 (==, !=): 3
    - 关系运算符 (<, >, <=, >=): 4
    - 加减 (+, -): 5
    - 乘除 (*, /): 6
    """
    # 非运算符类型直接返回 0
    if token_type != "OPERATOR":
        return 0
    
    # 优先级查表（从低到高）
    precedence_table = {
        "||": 1,                    # 逻辑或
        "&&": 2,                    # 逻辑与
        "==": 3, "!=": 3,          # 相等运算符
        "<": 4, ">": 4,            # 关系运算符
        "<=": 4, ">=": 4,
        "+": 5, "-": 5,            # 加减
        "*": 6, "/": 6,            # 乘除
    }
    
    return precedence_table.get(token_value, 0)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed - this is a pure utility function