# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._verify_literal_package._verify_literal_src import _verify_literal
from ._verify_variable_ref_package._verify_variable_ref_src import _verify_variable_ref
from ._verify_binary_op_package._verify_binary_op_src import _verify_binary_op
from ._verify_assignment_package._verify_assignment_src import _verify_assignment
from ._verify_function_call_package._verify_function_call_src import _verify_function_call
from ._verify_return_stmt_package._verify_return_stmt_src import _verify_return_stmt
from ._verify_control_flow_stmt_package._verify_control_flow_stmt_src import _verify_control_flow_stmt
from ._verify_function_def_package._verify_function_def_src import _verify_function_def
from ._verify_loop_stmt_package._verify_loop_stmt_src import _verify_loop_stmt
from ._verify_if_stmt_package._verify_if_stmt_src import _verify_if_stmt
from ._verify_children_package._verify_children_src import _verify_children

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
#   "name": str,             # 变量/函数名
#   "left": dict,            # 二元操作左操作数
#   "right": dict,           # 二元操作右操作数
#   "args": list,            # 函数调用参数列表
#   "body": dict,            # 函数体/循环体
#   "then_branch": dict,     # if 的 then 分支
#   "else_branch": dict,     # if 的 else 分支
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list            # 作用域栈
# }

ContextStack = list
# ContextStack possible fields:
# [
#   {"type": "function", "name": str, "return_type": str},
#   {"type": "loop", "stmt_type": "while"|"for"}
# ]


# === main function ===
def _verify_node(node: dict, symbol_table: dict, context_stack: list, filename: str) -> None:
    """递归验证单个 AST 节点。根据 node['type'] 分发到具体验证逻辑。"""
    node_type = node.get("type", "")
    
    if node_type in ("int_literal", "char_literal"):
        _verify_literal(node, filename)
    elif node_type == "variable_ref":
        _verify_variable_ref(node, symbol_table, filename)
    elif node_type == "binary_op":
        _verify_binary_op(node, symbol_table, context_stack, filename)
    elif node_type == "assignment":
        _verify_assignment(node, symbol_table, context_stack, filename)
    elif node_type == "function_call":
        _verify_function_call(node, symbol_table, context_stack, filename)
    elif node_type == "return_stmt":
        _verify_return_stmt(node, symbol_table, context_stack, filename)
    elif node_type in ("break_stmt", "continue_stmt"):
        _verify_control_flow_stmt(node, context_stack, filename)
    elif node_type == "function_def":
        _verify_function_def(node, symbol_table, context_stack, filename)
    elif node_type in ("while_stmt", "for_stmt"):
        _verify_loop_stmt(node, symbol_table, context_stack, filename)
    elif node_type == "if_stmt":
        _verify_if_stmt(node, symbol_table, context_stack, filename)
    else:
        # 未知节点类型，递归验证子节点
        _verify_children(node, symbol_table, context_stack, filename)


# === helper functions ===


# === OOP compatibility layer ===
