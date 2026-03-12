# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this helper

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("assignment")
#   "children": list,        # 子节点列表 (可选，包含目标变量和值表达式)
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "target": str,           # 赋值目标变量名 (可选)
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
    """
    处理赋值语句节点。
    
    检查赋值目标变量是否已声明，如果未声明则记录错误。
    可选验证赋值类型与声明类型是否兼容。
    
    Args:
        node: assignment 类型的 AST 节点
        symbol_table: 符号表，用于检查变量声明状态
    
    Side Effects:
        可能添加错误信息到 symbol_table["errors"]
    """
    # 提取赋值目标变量名
    target_var = _extract_target_variable(node)
    if not target_var:
        return
    
    # 提取位置信息
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 检查变量是否已声明
    variables = symbol_table.get("variables", {})
    
    if target_var not in variables:
        # 变量未声明，记录错误
        error_msg = f"Variable '{target_var}' used before declaration at line {line}, column {column}"
        errors = symbol_table.setdefault("errors", [])
        errors.append(error_msg)
    else:
        # 变量已声明，可选：验证类型兼容性
        _verify_type_compatibility(node, variables[target_var], symbol_table)

# === helper functions ===
def _extract_target_variable(node: AST) -> str:
    """
    从 AST 节点中提取赋值目标变量名。
    
    Args:
        node: AST 节点
    
    Returns:
        变量名，如果无法提取则返回空字符串
    """
    # 优先从 "target" 字段获取
    target = node.get("target")
    if target and isinstance(target, str):
        return target
    
    # 尝试从 "value" 字段获取（某些 AST 结构可能这样存储）
    value = node.get("value")
    if value and isinstance(value, str):
        return value
    
    # 尝试从 children 中获取（第一个子节点可能是目标变量）
    children = node.get("children", [])
    if children and isinstance(children, list) and len(children) > 0:
        first_child = children[0]
        if isinstance(first_child, dict):
            child_target = first_child.get("value")
            if child_target and isinstance(child_target, str):
                return child_target
    
    return ""

def _verify_type_compatibility(node: AST, var_info: Dict, symbol_table: SymbolTable) -> None:
    """
    验证赋值类型与变量声明类型是否兼容。
    
    Args:
        node: AST 节点（包含赋值的值）
        var_info: 变量声明信息
        symbol_table: 符号表
    
    Side Effects:
        如果类型不兼容，可能添加错误到 symbol_table["errors"]
    """
    # 获取变量声明的类型
    declared_type = var_info.get("data_type")
    if not declared_type:
        return
    
    # 获取赋值的类型（从 node 的 data_type 字段）
    assigned_type = node.get("data_type")
    if not assigned_type:
        # 如果没有显式类型信息，跳过类型检查
        return
    
    # 简单类型兼容性检查（int 和 char 不兼容）
    if declared_type != assigned_type:
        line = node.get("line", 0)
        column = node.get("column", 0)
        target_var = _extract_target_variable(node)
        
        error_msg = f"Type mismatch for variable '{target_var}': expected {declared_type}, got {assigned_type} at line {line}, column {column}"
        errors = symbol_table.setdefault("errors", [])
        errors.append(error_msg)

# === OOP compatibility layer ===
# Not needed for this helper function