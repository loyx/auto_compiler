# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this handler

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值
#   "name": str,             # 变量名 (可能字段)
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
    处理变量声明节点，将变量记录到符号表中。
    
    处理逻辑：
    1. 从 node 中提取变量名和数据类型
    2. 确保 symbol_table["variables"] 和 ["errors"] 存在
    3. 检查是否重复声明
    4. 记录变量信息到符号表
    """
    # 提取变量名：优先尝试 "name"，其次 "value"
    var_name = node.get("name") or node.get("value")
    if var_name is None:
        # 尝试从 children 中提取
        children = node.get("children", [])
        if children and isinstance(children[0], dict):
            var_name = children[0].get("value") or children[0].get("name")
    
    if var_name is None:
        # 无法提取变量名，记录错误
        errors = symbol_table.setdefault("errors", [])
        line = node.get("line", 0)
        column = node.get("column", 0)
        errors.append({
            "type": "invalid_var_decl",
            "message": "无法提取变量名",
            "line": line,
            "column": column
        })
        return
    
    # 提取数据类型
    data_type = node.get("data_type", "int")
    if data_type not in ("int", "char"):
        data_type = "int"  # 默认类型
    
    # 提取位置信息
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 确保 variables 和 errors 存在
    variables = symbol_table.setdefault("variables", {})
    errors = symbol_table.setdefault("errors", [])
    
    # 获取当前作用域层级
    current_scope = symbol_table.get("current_scope", 0)
    
    # 检查是否已在当前作用域声明过
    if var_name in variables:
        existing = variables[var_name]
        if existing.get("scope_level") == current_scope:
            # 重复声明错误
            errors.append({
                "type": "duplicate_declaration",
                "message": f"变量 '{var_name}' 已在当前作用域声明",
                "line": line,
                "column": column,
                "variable": var_name
            })
            return
    
    # 记录变量到符号表
    variables[var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this handler function
