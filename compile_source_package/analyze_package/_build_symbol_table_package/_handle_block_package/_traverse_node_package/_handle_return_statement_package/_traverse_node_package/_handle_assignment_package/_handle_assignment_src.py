# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No child functions needed for this module

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "assignment")
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "variable": str,         # 被赋值的变量名
#   "expression": Any        # 赋值的表达式
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (纯字符串)
# }


# === main function ===
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 assignment 类型节点（赋值语句）。
    
    验证变量是否已声明，检查类型匹配，记录错误到 symbol_table["errors"]。
    不返回值，所有副作用通过修改 symbol_table 实现。
    """
    errors = symbol_table.setdefault("errors", [])
    variables = symbol_table.get("variables", {})
    
    # 提取位置信息
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 提取变量名：优先使用 node.get("variable")，降级从 children 查找
    var_name = _extract_variable_name(node)
    
    if not var_name:
        errors.append(f"Error: Cannot determine variable name in assignment at line {line}, column {column}")
        return
    
    # 检查变量是否已声明
    var_info = variables.get(var_name)
    if not var_info or not var_info.get("is_declared", False):
        errors.append(f"Error: Variable '{var_name}' not declared at line {line}, column {column}")
        return
    
    # 获取变量声明的类型
    declared_type = var_info.get("data_type")
    
    # 获取表达式类型：优先使用 node.get("data_type")，降级推断
    expr_type = _get_expression_type(node, variables)
    
    # 类型匹配检查
    if declared_type and expr_type and declared_type != expr_type:
        errors.append(
            f"Error: Type mismatch in assignment: variable '{var_name}' is '{declared_type}' "
            f"but expression is '{expr_type}' at line {line}, column {column}"
        )


# === helper functions ===
def _extract_variable_name(node: AST) -> Optional[str]:
    """
    从 assignment 节点提取变量名。
    
    优先使用 node.get("variable")，如果不存在则遍历 children 查找 identifier 节点。
    """
    # 优先使用显式 variable 字段
    var_name = node.get("variable")
    if var_name:
        return var_name
    
    # 降级：从 children 中查找 identifier 节点
    children = node.get("children", [])
    for child in children:
        if isinstance(child, dict) and child.get("type") == "identifier":
            return child.get("value")
    
    return None


def _get_expression_type(node: AST, variables: Dict[str, Any]) -> Optional[str]:
    """
    获取赋值表达式的类型。
    
    优先使用 node.get("data_type")，如果不存在则尝试从 children 推断。
    """
    # 优先使用显式 data_type 字段
    expr_type = node.get("data_type")
    if expr_type:
        return expr_type
    
    # 降级：从 children 推断类型
    children = node.get("children", [])
    for child in children:
        if not isinstance(child, dict):
            continue
        
        child_type = child.get("type")
        
        # 从 literal 节点获取类型
        if child_type == "literal":
            return child.get("data_type")
        
        # 从 identifier 节点查询变量类型
        if child_type == "identifier":
            var_name = child.get("value")
            if var_name and var_name in variables:
                var_info = variables[var_name]
                return var_info.get("data_type")
    
    return None


# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
