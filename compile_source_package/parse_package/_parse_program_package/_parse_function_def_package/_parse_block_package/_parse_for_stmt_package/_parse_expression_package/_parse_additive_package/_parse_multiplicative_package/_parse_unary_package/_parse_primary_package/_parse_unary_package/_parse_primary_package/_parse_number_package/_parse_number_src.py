# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple parser

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (LITERAL 或 ERROR)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值 (int/float 或错误消息)
#   "line": int,             # 行号
#   "column": int            # 列号
# }


# === main function ===
def _parse_number(token_value: str, line: int, column: int) -> AST:
    """
    解析数字 token 字符串为 AST 节点。
    
    若包含 '.', 'e', 'E' → 转换为 float
    否则 → 转换为 int
    转换成功 → LITERAL 节点
    转换失败 → ERROR 节点
    """
    # 判断是否需要转换为 float
    needs_float = any(c in token_value for c in ['.', 'e', 'E'])
    
    try:
        if needs_float:
            parsed_value = float(token_value)
        else:
            parsed_value = int(token_value)
        
        # 返回 LITERAL 节点
        return {
            "type": "LITERAL",
            "value": parsed_value,
            "children": [],
            "line": line,
            "column": column
        }
    except ValueError:
        # 返回 ERROR 节点
        return {
            "type": "ERROR",
            "value": f"Invalid number literal: {token_value}",
            "children": [],
            "line": line,
            "column": column
        }


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function