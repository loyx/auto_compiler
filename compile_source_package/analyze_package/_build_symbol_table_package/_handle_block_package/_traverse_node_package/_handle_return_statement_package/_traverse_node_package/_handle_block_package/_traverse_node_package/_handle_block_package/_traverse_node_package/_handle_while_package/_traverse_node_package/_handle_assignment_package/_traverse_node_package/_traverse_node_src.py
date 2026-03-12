# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "binary_op", "literal", etc.)
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
#   "errors": list                 # 错误列表 (已初始化为 list)
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    AST 遍历分发器。根据节点类型调用相应的处理函数，并递归遍历子节点。
    
    副作用：可能修改 symbol_table（如添加错误、注册变量等）
    """
    node_type = node.get("type", "")
    
    # 根据节点类型分发到对应的处理函数
    if node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "var_decl":
        _handle_var_decl(node, symbol_table)
    elif node_type == "if":
        _handle_if(node, symbol_table)
    elif node_type == "while":
        _handle_while(node, symbol_table)
    elif node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "binary_op":
        _handle_binary_op(node, symbol_table)
    elif node_type == "literal":
        # 字面量无需特殊处理
        pass
    else:
        # 未知节点类型，记录警告
        line = node.get("line", "?")
        column = node.get("column", "?")
        symbol_table["errors"].append({
            "type": "warning",
            "message": f"Unknown node type: {node_type}",
            "line": line,
            "column": column
        })
    
    # 递归遍历子节点（对于包含子表达式的节点）
    children = node.get("children", [])
    for child in children:
        if isinstance(child, dict) and "type" in child:
            _traverse_node(child, symbol_table)

# === helper functions ===
# No helper functions needed - all logic delegated to child functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a utility function node