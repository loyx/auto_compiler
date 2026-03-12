# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple scope management logic

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "data_type": str,
#   "line": int,
#   "column": int
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
def _handle_if_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理条件语句节点，进入新作用域。
    
    处理逻辑：
    1. if 语句引入新的作用域（块级作用域）
    2. 进入新作用域：current_scope += 1
    3. 将新作用域压入 scope_stack
    4. 可选：验证条件表达式的类型是否为布尔类型
    
    注意：
    - 不需要递归处理子节点，_traverse_node 会自动处理
    - 作用域退出由遍历逻辑处理
    """
    # 进入新作用域（块级作用域）
    symbol_table["current_scope"] += 1
    symbol_table["scope_stack"].append(symbol_table["current_scope"])
    
    # 可选：验证条件表达式类型（如果语言支持类型检查）
    _validate_condition_type(node, symbol_table)


# === helper functions ===
def _validate_condition_type(node: AST, symbol_table: SymbolTable) -> None:
    """
    验证 if 语句条件表达式的类型是否为布尔类型。
    
    如果条件表达式不是布尔类型，记录错误到 symbol_table["errors"]。
    """
    children = node.get("children", [])
    if not children:
        return
    
    # 第一个子节点通常是条件表达式
    condition_node = children[0]
    condition_type = condition_node.get("data_type")
    
    # 如果节点有明确的类型信息，验证是否为布尔类型
    if condition_type and condition_type != "bool":
        line = node.get("line", "unknown")
        error_msg = f"Line {line}: Condition expression must be of type 'bool', got '{condition_type}'"
        symbol_table["errors"].append(error_msg)


# === OOP compatibility layer ===
# No OOP wrapper needed - this is a helper function for AST traversal
