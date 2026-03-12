# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_declaration_package._handle_declaration_src import _handle_declaration
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_expression_package._handle_expression_src import _handle_expression

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (必填，永不为空)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (可选)
#   "data_type": str,        # 类型信息 "int" 或 "char" (可选)
#   "line": int,             # 行号 (必填，最小为 0)
#   "column": int            # 列号 (必填，最小为 0)
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list,           # 作用域栈 (存储旧 scope 值)
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    递归遍历 AST 节点并根据节点类型分发到对应的处理函数。
    
    处理逻辑：
    1. 获取 node.type 判断节点类型
    2. 根据类型调用相应的 handler 函数
    3. handler 函数自行负责遍历其子节点
    
    未知类型静默跳过。
    """
    node_type = node.get("type", "")
    
    if node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "declaration":
        _handle_declaration(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "expression":
        _handle_expression(node, symbol_table)
    # 未知类型静默跳过（无 else 分支）

# === helper functions ===
# No helper functions needed for this simple dispatcher

# === OOP compatibility layer ===
# No OOP wrapper needed for internal AST traversal function
