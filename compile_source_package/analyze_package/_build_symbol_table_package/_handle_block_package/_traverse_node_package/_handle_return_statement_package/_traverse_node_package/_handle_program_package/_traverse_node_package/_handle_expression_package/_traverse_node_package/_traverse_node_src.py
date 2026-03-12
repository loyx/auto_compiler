# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_expression_package._handle_expression_src import _handle_expression

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block", "expression", "variable", "function_call" 等)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int,           # 列号
#   "operator": str,         # 操作符 (对于 expression 节点)
#   "operands": list,        # 操作数列表 (对于 expression 节点)
#   "left": AST,             # 左操作数 (对于二元表达式)
#   "right": AST,            # 右操作数 (对于二元表达式)
#   "name": str              # 变量名或函数名
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 [{"message": str, "line": int, "column": int, "type": str}]
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    遍历 AST 节点并分发到对应的处理函数。
    
    根据 node["type"] 调用相应的 handler：
    - "expression", "variable", "identifier", "function_call", "call" -> _handle_expression
    - 其他已知类型 -> 调用对应的 handler（如有）
    - 未知类型 -> 仅递归处理 children
    
    副作用：可能通过 handler 向 symbol_table['errors'] 添加错误。
    """
    node_type = node.get("type", "")
    
    # 根据类型分发到对应的 handler
    if node_type in ("expression", "variable", "identifier", "function_call", "call"):
        _handle_expression(node, symbol_table)
    # 其他已知类型可在此扩展，目前仅递归 children
    else:
        # 未知类型或无需特殊处理的类型，仅递归 children
        pass
    
    # 递归处理所有子节点
    children = node.get("children", [])
    for child in children:
        _traverse_node(child, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
