# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
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
#   "scope_stack": list,           # 作用域栈 (存储旧 scope 值)
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _handle_while(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 while 循环节点：遍历条件表达式和循环体。
    
    Args:
        node: while 类型的 AST 节点，包含 condition 和 body 子节点
        symbol_table: 符号表，用于遍历时传递上下文
    """
    children = node.get("children", [])
    
    # while 节点结构：children[0] = 条件表达式，children[1] = 循环体 block
    if len(children) < 2:
        # 缺少必要的子节点，无法处理
        return
    
    condition_node = children[0]
    body_node = children[1]
    
    # 遍历条件表达式
    _traverse_node(condition_node, symbol_table)
    
    # 遍历循环体 block
    _traverse_node(body_node, symbol_table)

# === helper functions ===
# No helper functions needed for this simple traversal logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a semantic analysis helper function