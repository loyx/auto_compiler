# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this module

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "data_type": str,
#   "line": int,
#   "column": int
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
    
    从 AST 节点中提取变量名、数据类型、行列号，
    在符号表中注册变量或记录重复声明错误。
    """
    # 提取行列号（用于错误报告）
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 提取数据类型
    data_type = node.get("data_type", "")
    
    # 验证数据类型合法性
    if data_type not in ("int", "char"):
        error = {
            "type": "error",
            "message": f"Invalid data type '{data_type}'. Only 'int' or 'char' allowed.",
            "line": line,
            "column": column
        }
        symbol_table["errors"].append(error)
        return
    
    # 提取变量名（可能在 value 或 children 中）
    var_name = _extract_var_name(node)
    
    if not var_name:
        error = {
            "type": "error",
            "message": "Variable name not found in declaration node.",
            "line": line,
            "column": column
        }
        symbol_table["errors"].append(error)
        return
    
    # 获取当前作用域层级
    current_scope = symbol_table.get("current_scope", 0)
    
    # 检查变量是否已声明
    if var_name in symbol_table.get("variables", {}):
        # 记录重复声明错误
        error = {
            "type": "error",
            "message": f"Variable '{var_name}' already declared.",
            "line": line,
            "column": column
        }
        symbol_table["errors"].append(error)
    else:
        # 注册新变量
        if "variables" not in symbol_table:
            symbol_table["variables"] = {}
        
        symbol_table["variables"][var_name] = {
            "data_type": data_type,
            "is_declared": True,
            "line": line,
            "column": column,
            "scope_level": current_scope
        }


# === helper functions ===
def _extract_var_name(node: AST) -> str:
    """
    从 AST 节点中提取变量名。
    
    尝试从 value 字段或 children 中获取变量名。
    """
    # 优先从 value 字段获取
    value = node.get("value")
    if value and isinstance(value, str):
        return value
    
    # 从 children 中查找标识符节点
    children = node.get("children", [])
    for child in children:
        if isinstance(child, dict):
            child_type = child.get("type", "")
            child_value = child.get("value", "")
            
            # 查找 identifier 类型的子节点
            if child_type == "identifier" and child_value:
                return child_value
            
            # 或者直接返回 string 类型的 value
            if child_type == "string" and child_value:
                return child_value
    
    # 如果 children 第一个元素是字符串，直接使用
    if children and isinstance(children[0], str):
        return children[0]
    
    return ""


# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function
