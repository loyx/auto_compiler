# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No child functions needed for this module

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block" 等)
#   "children": list,        # 子节点列表
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
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表
# }

# === main function ===
def _handle_variable_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 variable_declaration 节点，将变量声明注册到符号表中。
    
    处理逻辑：
    1. 从 node["children"] 中提取变量名节点（type 为 "identifier" 的节点），或从 node["value"] 获取
    2. 获取数据类型：优先使用 node["data_type"]，如不存在则从 children 中提取类型节点
    3. 将变量信息注册到 symbol_table["variables"]
    
    错误处理：
    - 如果找不到变量名：添加错误到 symbol_table["errors"]
    - 如果变量已在当前作用域声明：添加错误（重复声明）到 symbol_table["errors"]
    
    副作用：
    - 修改 symbol_table["variables"]
    - 可能添加错误到 symbol_table["errors"]
    """
    var_name = _extract_variable_name(node)
    
    if var_name is None:
        symbol_table["errors"].append({
            "type": "error",
            "message": "无法提取变量名",
            "line": node.get("line"),
            "column": node.get("column")
        })
        return
    
    data_type = _extract_data_type(node)
    
    current_scope = symbol_table.get("current_scope", 0)
    
    if var_name in symbol_table["variables"]:
        existing_var = symbol_table["variables"][var_name]
        if existing_var.get("scope_level") == current_scope:
            symbol_table["errors"].append({
                "type": "error",
                "message": f"变量 '{var_name}' 重复声明",
                "line": node.get("line"),
                "column": node.get("column")
            })
            return
    
    symbol_table["variables"][var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": node.get("line"),
        "column": node.get("column"),
        "scope_level": current_scope
    }

# === helper functions ===
def _extract_variable_name(node: AST) -> Optional[str]:
    """
    从 variable_declaration 节点中提取变量名。
    
    优先从 children 中查找 type 为 "identifier" 的节点，
    如果找不到则尝试从 node["value"] 获取。
    """
    children = node.get("children", [])
    
    for child in children:
        if isinstance(child, dict) and child.get("type") == "identifier":
            return child.get("value")
    
    value = node.get("value")
    if value is not None:
        return str(value)
    
    return None

def _extract_data_type(node: AST) -> str:
    """
    从 variable_declaration 节点中提取数据类型。
    
    优先使用 node["data_type"]，
    如果不存在则从 children 中提取类型节点。
    默认返回 "int"。
    """
    data_type = node.get("data_type")
    if data_type is not None:
        return data_type
    
    children = node.get("children", [])
    for child in children:
        if isinstance(child, dict):
            child_type = child.get("type")
            if child_type in ("int", "char"):
                return child_type
            if child.get("data_type") in ("int", "char"):
                return child["data_type"]
    
    return "int"

# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function node
