# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_function_decl_package._handle_function_decl_src import _handle_function_decl
from ._handle_return_package._handle_return_src import _handle_return
from ._handle_expression_package._handle_expression_src import _handle_expression

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
    递归遍历 AST 节点的调度函数。
    
    根据 node["type"] 字段值，分发到对应的处理函数。
    所有错误记录到 symbol_table["errors"]，不抛出异常。
    """
    node_type = node.get("type", "")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 节点类型分发
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
    elif node_type == "function_decl":
        _handle_function_decl(node, symbol_table)
    elif node_type == "return":
        _handle_return(node, symbol_table)
    elif node_type in ("binary_op", "literal", "identifier", "unary_op", "call"):
        _handle_expression(node, symbol_table)
    elif node_type == "":
        # 空类型，可能是叶子节点或无效节点，跳过
        pass
    else:
        # 未知节点类型，记录错误
        error_msg = f"Unknown node type '{node_type}' at line {line}, column {column}"
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append({
            "message": error_msg,
            "line": line,
            "column": column,
            "type": "unknown_node_type"
        })
    
    # 处理子节点（如果存在且未被 handler 处理）
    # 注意：block/if/while/function_decl 等 handler 内部已处理子节点
    # 这里只处理没有专门 handler 的节点类型的子节点
    if node_type not in ("block", "if", "while", "function_decl") and "children" in node:
        for child in node["children"]:
            _traverse_node(child, symbol_table)

# === helper functions ===
# No helper functions needed - all logic delegated to child handlers

# === OOP compatibility layer ===
# Not needed - this is a helper function node, not a framework entry point
