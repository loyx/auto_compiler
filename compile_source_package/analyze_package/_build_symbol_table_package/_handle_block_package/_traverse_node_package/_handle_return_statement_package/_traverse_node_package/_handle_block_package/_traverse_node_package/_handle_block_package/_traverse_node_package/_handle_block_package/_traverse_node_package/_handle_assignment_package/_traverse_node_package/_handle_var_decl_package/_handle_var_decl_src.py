# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "var_decl", "assignment", etc.)
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
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }


# === main function ===
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点。
    
    在 symbol_table["variables"] 中注册变量，检查重复声明。
    副作用：修改 symbol_table["variables"]，可能在 errors 中添加错误。
    """
    # 1. 提取变量名（可能在 node["value"] 或 children[0]）
    var_name = _extract_var_name(node)
    
    # 2. 提取数据类型
    data_type = node.get("data_type", "int")
    
    # 3. 提取行号和列号
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 4. 检查变量是否已声明
    variables = symbol_table.get("variables", {})
    
    if var_name in variables:
        # 5. 已声明，添加错误
        errors = symbol_table.get("errors", [])
        errors.append(f"Duplicate declaration: {var_name}")
        symbol_table["errors"] = errors
    else:
        # 6. 未声明，注册变量
        variables[var_name] = {
            "data_type": data_type,
            "is_declared": True,
            "line": line,
            "column": column,
            "scope_level": symbol_table.get("current_scope", 0)
        }
        symbol_table["variables"] = variables
        
        # 7. 如果有初始值表达式，递归遍历其 children
        children = node.get("children", [])
        for child in children:
            if isinstance(child, dict) and child.get("type") == "expression":
                _traverse_expression(child, symbol_table)


# === helper functions ===
def _extract_var_name(node: AST) -> str:
    """从 AST 节点中提取变量名。"""
    # 优先从 node["value"] 获取
    if "value" in node and isinstance(node["value"], str):
        return node["value"]
    
    # 否则从 children[0] 获取
    children = node.get("children", [])
    if len(children) > 0:
        first_child = children[0]
        if isinstance(first_child, str):
            return first_child
        elif isinstance(first_child, dict) and "value" in first_child:
            return str(first_child["value"])
    
    # 默认返回空字符串
    return ""


def _traverse_expression(node: AST, symbol_table: SymbolTable) -> None:
    """递归遍历表达式节点，处理其中的变量引用。"""
    # 如果是变量引用节点，可以在这里处理（例如检查变量是否已声明）
    # 当前实现仅遍历，不做额外检查
    children = node.get("children", [])
    for child in children:
        if isinstance(child, dict):
            _traverse_expression(child, symbol_table)


# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function
