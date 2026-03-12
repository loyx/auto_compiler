# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this module

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "data_type": str,
#   "line": int,
#   "column": int,
#   "name": str,
#   "init_value": Any
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_variable_def(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量定义节点。
    
    将变量注册到符号表，处理初始值表达式，记录错误。
    不实际执行赋值，只进行符号表注册和 AST 遍历。
    """
    # 获取变量名（优先 value，其次 name）
    var_name = node.get("value") or node.get("name")
    
    if not var_name or not isinstance(var_name, str):
        error_msg = f"Invalid variable name at line {node.get('line', '?')}, column {node.get('column', '?')}"
        symbol_table.setdefault("errors", []).append(error_msg)
        return
    
    # 获取变量类型（可选）
    var_type = node.get("data_type")
    
    # 获取当前作用域
    current_scope = symbol_table.get("current_scope", 0)
    
    # 检查变量是否已定义（重复定义检查）
    variables = symbol_table.setdefault("variables", {})
    if var_name in variables:
        existing_var = variables[var_name]
        if existing_var.get("scope", -1) == current_scope:
            error_msg = f"Duplicate variable definition '{var_name}' at line {node.get('line', '?')}"
            symbol_table.setdefault("errors", []).append(error_msg)
            # 根据语言语义，这里选择覆盖（可调整为报错后返回）
    
    # 构建变量元数据
    var_metadata = {
        "name": var_name,
        "data_type": var_type,
        "scope": current_scope,
        "initialized": False,
        "line": node.get("line"),
        "column": node.get("column"),
        "current_function": symbol_table.get("current_function")
    }
    
    # 检查是否存在初始值
    init_value = None
    children = node.get("children", [])
    
    if children and len(children) > 0:
        init_value = children[0]
        var_metadata["initialized"] = True
    elif node.get("init_value") is not None:
        init_value = node.get("init_value")
        var_metadata["initialized"] = True
    
    # 注册变量到符号表
    variables[var_name] = var_metadata
    
    # 如果存在初始值表达式，遍历该表达式（递归处理 AST）
    if init_value is not None and isinstance(init_value, dict):
        _traverse_expression(init_value, symbol_table)

# === helper functions ===
def _traverse_expression(expr_node: AST, symbol_table: SymbolTable) -> None:
    """
    遍历表达式 AST 节点，检查变量引用是否合法。
    
    此函数用于在变量初始化时验证表达式中使用的变量是否已定义。
    """
    if not isinstance(expr_node, dict):
        return
    
    node_type = expr_node.get("type", "")
    
    # 如果是变量引用节点，检查变量是否已定义
    if node_type == "variable_ref":
        ref_name = expr_node.get("value") or expr_node.get("name")
        if ref_name and isinstance(ref_name, str):
            variables = symbol_table.get("variables", {})
            if ref_name not in variables:
                error_msg = f"Undefined variable '{ref_name}' at line {expr_node.get('line', '?')}"
                symbol_table.setdefault("errors", []).append(error_msg)
    
    # 递归遍历子节点
    children = expr_node.get("children", [])
    if children and isinstance(children, list):
        for child in children:
            _traverse_expression(child, symbol_table)

# === OOP compatibility layer ===
# Not needed for this helper function node
