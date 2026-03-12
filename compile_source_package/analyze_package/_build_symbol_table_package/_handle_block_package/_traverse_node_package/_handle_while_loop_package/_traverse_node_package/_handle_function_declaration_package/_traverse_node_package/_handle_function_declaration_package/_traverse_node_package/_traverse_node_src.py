# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_statement_package._handle_if_statement_src import _handle_if_statement
from ._handle_loop_statement_package._handle_loop_statement_src import _handle_loop_statement
from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,           # 节点类型
#   "name": str,           # 名称（用于函数/变量声明）
#   "params": list,        # 参数列表（函数声明）
#   "body": AST,           # 函数体/循环体
#   "return_type": str,    # 返回类型
#   "line": int,           # 行号
#   "column": int,         # 列号
#   "value": Any,          # 初始值/赋值值
#   "var_type": str,       # 变量类型
#   "target": str,         # 赋值目标
#   "condition": AST,      # 条件表达式
#   "then_branch": AST,    # if 分支
#   "else_branch": AST,    # else 分支
#   "loop_type": str,      # 循环类型
#   "expression": Any      # 返回表达式
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # 变量表
#   "functions": Dict[str, Dict],  # 函数表
#   "current_scope": int,          # 当前作用域
#   "scope_stack": list            # 作用域栈
# }

HandlerFunc = Any  # Type alias for handler functions


# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    递归遍历 AST 节点树，根据节点类型分发到对应的处理函数。
    
    输入：任意 AST 节点和符号表
    处理：根据 node["type"] 调用相应的处理函数
    副作用：可能通过处理函数修改 symbol_table
    """
    node_type = node.get("type")
    
    if node_type is None:
        raise ValueError(f"AST node missing 'type' field at line {node.get('line', 'unknown')}")
    
    # 节点类型到处理函数的映射
    handler_map: Dict[str, HandlerFunc] = {
        "function_declaration": _handle_function_declaration,
        "variable_declaration": _handle_variable_declaration,
        "assignment": _handle_assignment,
        "if_statement": _handle_if_statement,
        "loop_statement": _handle_loop_statement,
        "return_statement": _handle_return_statement,
    }
    
    handler = handler_map.get(node_type)
    if handler is None:
        # 未知节点类型，记录警告但继续处理
        print(f"Warning: Unknown AST node type '{node_type}' at line {node.get('line', 'unknown')}")
        return
    
    handler(node, symbol_table)


# === helper functions ===
def _get_node_line(node: AST) -> str:
    """获取节点行号，用于错误信息。"""
    line = node.get("line")
    return str(line) if line is not None else "unknown"


# === OOP compatibility layer ===
# Not required for this function node (pure traversal logic)
