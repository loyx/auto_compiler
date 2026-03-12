# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "binary_op", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (对于 binary_op 是运算符字符串)
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
def _handle_binary_op(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理二元操作节点：递归遍历左右操作数。
    
    输入：binary_op 类型 AST 节点和符号表
    处理：遍历 left (children[0]) 和 right (children[1]) 操作数
    副作用：可能通过 _traverse_node 修改 symbol_table
    """
    # 获取左右操作数
    left_operand = node["children"][0]
    right_operand = node["children"][1]
    
    # 递归遍历左右操作数
    _traverse_node(left_operand, symbol_table)
    _traverse_node(right_operand, symbol_table)
    
    # 可选：类型验证（根据需求为可选功能，此处暂不实现）
    # 如需验证，可检查 node["value"] 运算符与操作数类型是否匹配

# === helper functions ===
# 无额外 helper 函数

# === OOP compatibility layer ===
# 不需要，此为普通函数节点