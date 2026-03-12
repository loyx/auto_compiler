# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple handler

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("assignment", "identifier", "literal", etc.)
#   "target": AST,           # 赋值目标（通常是标识符节点）
#   "value": AST,            # 赋值表达式
#   "line": int,             # 行号
#   "column": int,           # 列号
#   "data_type": str,        # 节点类型推断结果（可选）
#   "name": str,             # 标识符名称（可选）
#   "literal_type": str,     # 字面量类型（可选）
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }


# === main function ===
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> str:
    """
    处理赋值节点，返回赋值表达式的类型。
    
    输入：assignment 类型的 AST 节点（包含 target, value）和符号表
    处理：递归处理右侧表达式，获取其类型
    副作用：无
    返回：赋值表达式的类型字符串
    """
    # 从 node 中获取 value（赋值表达式）
    value_node = node.get("value")
    
    # 如果 value 不存在，返回 void
    if value_node is None:
        return "void"
    
    # 如果 value 节点已经有 data_type 字段，直接返回
    if "data_type" in value_node:
        return value_node["data_type"]
    
    # 根据 value 节点类型推断类型
    value_type = value_node.get("type", "")
    
    if value_type == "literal":
        # 字面量节点，返回 literal_type
        return value_node.get("literal_type", "any")
    elif value_type == "identifier":
        # 标识符节点，需要从符号表查找变量类型
        var_name = value_node.get("name", "")
        variables = symbol_table.get("variables", {})
        if var_name in variables:
            return variables[var_name].get("type", "any")
        return "any"
    elif value_type == "binary_op":
        # 二元运算，简化处理返回 any
        return "any"
    elif value_type == "function_call":
        # 函数调用，简化处理返回 any
        return "any"
    else:
        # 未知类型，返回 any
        return "any"


# === helper functions ===
# No helper functions needed


# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
