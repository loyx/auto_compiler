# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", etc.)
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
def _handle_return(node: AST, symbol_table: SymbolTable) -> None:
    """处理 return 语句节点，验证返回类型与函数声明是否匹配。"""
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 检查是否在函数内部
    current_function = symbol_table.get("current_function")
    if current_function is None:
        error_msg = f"return statement outside function at line {line}"
        symbol_table.setdefault("errors", []).append(error_msg)
        return
    
    # 获取函数声明
    functions = symbol_table.get("functions", {})
    func_decl = functions.get(current_function)
    if func_decl is None:
        error_msg = f"function '{current_function}' not found in symbol table at line {line}"
        symbol_table.setdefault("errors", []).append(error_msg)
        return
    
    # 获取函数返回类型
    declared_return_type = func_decl.get("return_type", "void")
    
    # 检查是否有返回值表达式
    children = node.get("children", [])
    if children:
        # 有返回值，遍历表达式并获取类型
        return_type = _traverse_node(children[0], symbol_table)
        
        # 验证类型匹配
        if return_type != declared_return_type:
            error_msg = (
                f"type mismatch in return statement at line {line}, column {column}: "
                f"expected '{declared_return_type}', got '{return_type}'"
            )
            symbol_table.setdefault("errors", []).append(error_msg)
    else:
        # 无返回值，检查函数是否允许 void return
        if declared_return_type != "void":
            error_msg = (
                f"missing return value at line {line}, column {column}: "
                f"function '{current_function}' expects '{declared_return_type}'"
            )
            symbol_table.setdefault("errors", []).append(error_msg)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
