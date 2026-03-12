# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
# }

# === main function ===
def _verify_literal(node: dict, filename: str) -> None:
    """
    验证并设置字面量节点的类型信息。
    
    处理字面量节点：
    - 若 node['type'] == "int_literal"：设置 node['data_type'] = "int"
    - 若 node['type'] == "char_literal"：设置 node['data_type'] = "char"
    
    无错误抛出，仅修改 node 的 data_type 字段。
    """
    if node.get("type") == "int_literal":
        node["data_type"] = "int"
    elif node.get("type") == "char_literal":
        node["data_type"] = "char"

# === helper functions ===
# No helper functions

# === OOP compatibility layer ===
# Not needed for this helper function