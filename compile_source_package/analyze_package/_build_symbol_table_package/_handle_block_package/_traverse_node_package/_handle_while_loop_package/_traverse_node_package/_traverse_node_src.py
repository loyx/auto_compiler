# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_function_def_package._handle_function_def_src import _handle_function_def
from ._handle_variable_decl_package._handle_variable_decl_src import _handle_variable_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_statement_package._handle_if_statement_src import _handle_if_statement
from ._handle_while_loop_package._handle_while_loop_src import _handle_while_loop
from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "condition": AST,        # while_loop 条件节点
#   "body": AST,             # while_loop 循环体节点
#   "name": str,             # 变量/函数名
#   "target": AST,           # 赋值目标
#   "left": AST,             # 二元运算左操作数
#   "right": AST,            # 二元运算右操作数
#   "operator": str,         # 二元运算符
#   "arguments": list,       # 函数调用参数列表
#   "params": list,          # 函数参数列表
#   "return_type": str,      # 函数返回类型
#   "then_branch": AST,      # if 语句 then 分支
#   "else_branch": AST       # if 语句 else 分支
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
    根据 AST 节点的 type 字段分发到对应的 handler 函数。
    
    输入：AST node 和 symbol_table
    处理：根据 node type 调用对应的 handler
    副作用：handler 可能修改 symbol_table
    未知类型：静默跳过
    """
    node_type = node.get("type")
    
    if node_type is None:
        return
    
    # 分发到对应的 handler
    if node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "function_def":
        _handle_function_def(node, symbol_table)
    elif node_type == "variable_decl":
        _handle_variable_decl(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "if_statement":
        _handle_if_statement(node, symbol_table)
    elif node_type == "while_loop":
        _handle_while_loop(node, symbol_table)
    elif node_type == "return_statement":
        _handle_return_statement(node, symbol_table)
    # 未知类型静默跳过

# === helper functions ===
# No helper functions needed - all logic delegated to child functions

# === OOP compatibility layer ===
# Not needed for this module - it's a helper function module