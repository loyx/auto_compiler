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
#   "errors": list                 # 错误列表
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """递归遍历 AST 节点，根据节点类型分发到对应的处理函数。"""
    # 初始化 errors 列表（如果不存在）
    symbol_table.setdefault('errors', [])
    
    # 获取节点类型
    node_type = node.get('type', '')
    
    # 根据类型分发到对应的 handler
    if node_type == 'block':
        _handle_block(node, symbol_table)
    elif node_type == 'var_decl':
        _handle_var_decl(node, symbol_table)
    elif node_type == 'assignment':
        _handle_assignment(node, symbol_table)
    elif node_type == 'if':
        _handle_if(node, symbol_table)
    elif node_type == 'while':
        _handle_while(node, symbol_table)
    elif node_type == 'func_decl':
        _handle_func_decl(node, symbol_table)
    elif node_type == 'func_call':
        _handle_func_call(node, symbol_table)
    elif node_type == 'return':
        _handle_return(node, symbol_table)
    else:
        # 未知节点类型，记录错误
        _record_unknown_type_error(node, symbol_table)

# === helper functions ===
def _record_unknown_type_error(node: AST, symbol_table: SymbolTable) -> None:
    """记录未知节点类型错误到 symbol_table['errors']。"""
    error_entry = {
        "message": f"Unknown node type: {node.get('type', 'N/A')}",
        "line": node.get('line', 0),
        "column": node.get('column', 0),
        "node_type": node.get('type', 'N/A'),
        "severity": "error"
    }
    symbol_table['errors'].append(error_entry)

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
