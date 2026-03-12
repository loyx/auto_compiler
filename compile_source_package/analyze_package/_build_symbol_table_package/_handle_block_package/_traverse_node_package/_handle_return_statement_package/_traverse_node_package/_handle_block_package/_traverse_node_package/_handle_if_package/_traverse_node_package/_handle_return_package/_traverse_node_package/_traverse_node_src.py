# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_literal_package._handle_literal_src import _handle_literal
from ._handle_identifier_package._handle_identifier_src import _handle_identifier
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_block_package._handle_block_src import _handle_block

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int,           # 列号
#   "left": AST,             # 左操作数 (binary_op)
#   "right": AST,            # 右操作数 (binary_op)
#   "operator": str,         # 运算符 (binary_op)
#   "function_name": str,    # 函数名 (function_call)
#   "target": AST,           # 赋值目标 (assignment)
#   "value": AST             # 赋值值 (assignment)
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
def _traverse_node(node: AST, symbol_table: SymbolTable) -> str:
    """递归遍历 AST 节点并推断表达式的类型。"""
    node_type = node.get("type", "")
    line = node.get("line", 0)
    
    # 字面量处理
    if node_type in ("literal_int", "int_literal"):
        return _handle_literal(node, symbol_table)
    elif node_type in ("literal_char", "char_literal"):
        return _handle_literal(node, symbol_table)
    
    # 标识符/变量处理
    elif node_type in ("identifier", "variable"):
        return _handle_identifier(node, symbol_table)
    
    # 二元运算符处理
    elif node_type in ("binary_op", "operation"):
        return _handle_binary_op(node, symbol_table)
    
    # 函数调用处理
    elif node_type == "function_call":
        return _handle_function_call(node, symbol_table)
    
    # 赋值处理
    elif node_type == "assignment":
        return _handle_assignment(node, symbol_table)
    
    # 代码块处理
    elif node_type == "block":
        return _handle_block(node, symbol_table)
    
    # 变量声明处理
    elif node_type == "var_decl":
        return node.get("data_type", "void")
    
    # 条件语句处理
    elif node_type == "if":
        return _handle_block(node.get("then_branch", {}), symbol_table)
    
    # 循环语句处理
    elif node_type == "while":
        return _handle_block(node.get("body", {}), symbol_table)
    
    # 返回语句处理
    elif node_type == "return":
        return "void"
    
    # 未知节点类型
    else:
        error_msg = f"unknown node type '{node_type}' at line {line}"
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append(error_msg)
        return "void"

# === helper functions ===
# Helper functions are delegated to sub-function modules

# === OOP compatibility layer ===
# Not needed for this function node
