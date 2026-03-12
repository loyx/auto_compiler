# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._traverse_node_src import _traverse_node

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
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点。
    
    检查同一作用域内的重复声明，记录变量信息到符号表，
    并递归处理初始化表达式。
    """
    var_name = node.get("value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    data_type = node.get("data_type", "int")
    current_scope = symbol_table.get("current_scope", 0)
    variables = symbol_table.setdefault("variables", {})
    errors = symbol_table.setdefault("errors", [])
    
    # 检查同一作用域内是否已声明
    if var_name in variables:
        if variables[var_name].get("scope_level") == current_scope:
            existing_line = variables[var_name].get("line", 0)
            errors.append(f"Variable '{var_name}' already declared at line {existing_line}")
            return
    
    # 记录变量信息
    variables[var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }
    
    # 处理初始化表达式
    init_expr = node.get("value") if isinstance(node.get("value"), dict) else None
    if init_expr is None and node.get("children"):
        children = node.get("children", [])
        if len(children) > 0 and isinstance(children[0], dict):
            init_expr = children[0]
    
    if init_expr is not None:
        _traverse_node(init_expr, symbol_table)


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
