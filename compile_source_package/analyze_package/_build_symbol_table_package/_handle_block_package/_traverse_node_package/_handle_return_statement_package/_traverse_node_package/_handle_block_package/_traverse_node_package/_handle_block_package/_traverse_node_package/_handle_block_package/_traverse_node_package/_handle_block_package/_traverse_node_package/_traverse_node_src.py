# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_func_decl_package._handle_func_decl_src import _handle_func_decl
from ._handle_func_call_package._handle_func_call_src import _handle_func_call
from ._handle_return_package._handle_return_src import _handle_return

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
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    根据 AST 节点的 type 字段分发到对应的处理函数。
    这是一个分发器/路由器函数，本身不处理具体逻辑。
    """
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    node_type = node.get("type", "")
    
    # 分发逻辑
    if node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "var_decl":
        _handle_var_decl(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "if":
        _handle_if(node, symbol_table)
    elif node_type == "while":
        _handle_while(node, symbol_table)
    elif node_type == "func_decl":
        _handle_func_decl(node, symbol_table)
    elif node_type == "func_call":
        _handle_func_call(node, symbol_table)
    elif node_type == "return":
        _handle_return(node, symbol_table)
    else:
        # 未知类型，记录错误
        line = node.get("line", "?")
        column = node.get("column", "?")
        symbol_table["errors"].append({
            "error_type": "unknown_node_type",
            "message": f"Unknown AST node type: {node_type}",
            "line": line,
            "column": column
        })

# === helper functions ===
# No helper functions needed - this is a pure dispatcher

# === OOP compatibility layer ===
# Not needed for internal dispatcher function
