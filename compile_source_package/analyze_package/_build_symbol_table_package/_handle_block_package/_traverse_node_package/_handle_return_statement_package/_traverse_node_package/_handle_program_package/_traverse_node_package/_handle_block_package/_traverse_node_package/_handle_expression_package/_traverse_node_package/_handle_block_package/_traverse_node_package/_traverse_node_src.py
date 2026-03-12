# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_statement_package._handle_if_statement_src import _handle_if_statement
from ._handle_while_loop_package._handle_while_loop_src import _handle_while_loop
from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block" 等)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }


# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    递归遍历 AST 节点并根据节点类型分发到对应的处理函数。
    
    输入：AST 节点和符号表。
    处理：根据 node["type"] 分发到 handler，未知类型递归处理 children。
    副作用：可能通过 handler 原地修改 symbol_table。
    异常：无。
    """
    node_type = node.get("type", "")
    
    # 已知节点类型 -> 分发到对应 handler
    handlers = {
        "block": _handle_block,
        "function_declaration": _handle_function_declaration,
        "variable_declaration": _handle_variable_declaration,
        "assignment": _handle_assignment,
        "if_statement": _handle_if_statement,
        "while_loop": _handle_while_loop,
        "return_statement": _handle_return_statement,
    }
    
    if node_type in handlers:
        handlers[node_type](node, symbol_table)
    else:
        # 未知类型或表达式节点：递归遍历 children
        children = node.get("children", [])
        for child in children:
            _traverse_node(child, symbol_table)


# === helper functions ===
def _traverse_children(node: AST, symbol_table: SymbolTable) -> None:
    """
    辅助函数：递归遍历节点的所有子节点。
    用于表达式节点或未知节点类型的默认处理。
    """
    children = node.get("children", [])
    for child in children:
        _traverse_node(child, symbol_table)


# === OOP compatibility layer ===
# 不需要 OOP wrapper，此为普通函数节点
