# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_block_package._handle_block_src import _handle_block

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", "literal", "identifier", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "name": str,             # 名称 (function_call / identifier 节点使用)
#   "value": Any,            # 节点值 (literal 节点使用)
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
#   "errors": list                 # 错误列表 (保证已初始化为 [])
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    AST 遍历分发器。根据节点类型路由到对应的处理函数。
    
    Args:
        node: AST 节点，包含 type 字段标识节点类型
        symbol_table: 符号表，包含变量、函数声明信息和错误列表
    
    Side effects:
        可能向 symbol_table['errors'] 追加错误
        可能更新 symbol_table['variables'] 或作用域栈
    """
    node_type = node.get("type", "")
    
    # 分发到对应的处理函数
    if node_type == "function_call":
        _handle_function_call(node, symbol_table)
    elif node_type == "var_decl":
        _handle_var_decl(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "if":
        _handle_if(node, symbol_table)
    elif node_type == "while":
        _handle_while(node, symbol_table)
    elif node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type in ("literal", "identifier"):
        # 叶子节点，无需特殊处理
        pass
    else:
        # 未识别的节点类型，可选处理或忽略
        # 这里选择静默忽略，因为可能是语言扩展或内部节点
        pass

# === helper functions ===
# 无 helper 函数，所有逻辑已下沉到子函数

# === OOP compatibility layer ===
# 不需要 OOP wrapper，这是内部遍历函数