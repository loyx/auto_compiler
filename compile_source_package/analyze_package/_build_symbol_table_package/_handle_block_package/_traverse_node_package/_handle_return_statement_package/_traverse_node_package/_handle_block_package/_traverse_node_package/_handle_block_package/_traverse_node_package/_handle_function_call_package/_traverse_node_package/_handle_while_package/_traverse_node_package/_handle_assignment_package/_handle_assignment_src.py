# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

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
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """处理赋值节点：检查变量是否已声明，验证类型兼容性。"""
    # 步骤 1: 从 node["children"] 获取左值 (lvalue) 和右值 (rvalue)
    children = node.get("children", [])
    if len(children) < 2:
        symbol_table.setdefault("errors", []).append({
            "message": "Assignment node must have lvalue and rvalue",
            "line": node.get("line", 0),
            "column": node.get("column", 0)
        })
        return
    
    lvalue = children[0]
    rvalue = children[1]
    
    # 步骤 2: 从左值标识符节点获取变量名
    var_name = lvalue.get("value")
    var_line = lvalue.get("line", node.get("line", 0))
    var_column = lvalue.get("column", node.get("column", 0))
    
    # 步骤 3: 检查变量名是否在 symbol_table["variables"] 中且 is_declared=True
    variables = symbol_table.get("variables", {})
    
    if var_name not in variables:
        # 步骤 4: 如果变量未声明，记录错误
        symbol_table.setdefault("errors", []).append({
            "message": f"Undefined variable '{var_name}'",
            "line": var_line,
            "column": var_column
        })
        return
    
    var_info = variables[var_name]
    if not var_info.get("is_declared", False):
        symbol_table.setdefault("errors", []).append({
            "message": f"Variable '{var_name}' is not declared",
            "line": var_line,
            "column": var_column
        })
        return
    
    # 步骤 5: 递归遍历右值表达式
    _traverse_node(rvalue, symbol_table)
    
    # 步骤 6 (可选): 验证右值类型与变量声明类型是否兼容
    declared_type = var_info.get("data_type")
    rvalue_type = rvalue.get("data_type")
    
    if declared_type and rvalue_type and declared_type != rvalue_type:
        symbol_table.setdefault("errors", []).append({
            "message": f"Type mismatch: cannot assign '{rvalue_type}' to '{declared_type}' variable '{var_name}'",
            "line": var_line,
            "column": var_column
        })

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
