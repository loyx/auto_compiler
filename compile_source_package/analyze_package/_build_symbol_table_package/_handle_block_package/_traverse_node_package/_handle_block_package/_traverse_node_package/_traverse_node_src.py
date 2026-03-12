# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Handler functions are independent modules, not child functions of _traverse_node
# They are imported as sibling modules in the function dependency tree
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_declaration_package._handle_declaration_src import _handle_declaration
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_expression_package._handle_expression_src import _handle_expression

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (必填): "block", "declaration", "assignment", "expression" 等
#   "children": list,        # 子节点列表 (可选)，block 类型必有此字段
#   "value": Any,            # 节点值 (可选)，字面量节点使用
#   "data_type": str,        # 类型信息 (可选): "int" 或 "char"
#   "line": int,             # 行号 (可选)
#   "column": int            # 列号 (可选)
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list            # 作用域栈
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    递归遍历 AST 节点，分发到对应的 handler 函数。
    
    输入：AST node 和 symbol_table
    处理行为：根据 node["type"] 分发到对应的 handler 函数
    副作用：可能通过 handler 修改 symbol_table
    异常或失败边界：对空节点、未知类型节点静默跳过，不抛出异常
    """
    # 空节点处理：静默跳过
    if node is None or not node:
        return
    
    # 类型字段检查
    node_type = node.get("type")
    if not node_type or not isinstance(node_type, str):
        return
    
    # 分发到对应的 handler
    handler_map = {
        "block": _handle_block,
        "declaration": _handle_declaration,
        "assignment": _handle_assignment,
        "expression": _handle_expression,
    }
    
    handler = handler_map.get(node_type)
    if handler:
        handler(node, symbol_table)
    else:
        # 未知节点类型：静默跳过，但尝试遍历 children 以处理可能的已知子节点
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)

# === helper functions ===
# No helper functions needed for this dispatcher

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
