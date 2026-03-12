# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub-functions for this module

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (必填，永不为空)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (可选)
#   "data_type": str,        # 类型信息 "int" 或 "char" (可选)
#   "line": int,             # 行号 (必填，最小为 0)
#   "column": int            # 列号 (必填，最小为 0)
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
    
    记录变量到 symbol_table['variables']，检查重复声明。
    副作用：修改 symbol_table 的变量信息和错误列表。
    """
    var_name = node.get("value")
    data_type = node.get("data_type", "int")
    line = node.get("line", 0)
    column = node.get("column", 0)
    scope_level = symbol_table.get("current_scope", 0)
    
    # 确保 variables 字典存在
    variables = symbol_table.setdefault("variables", {})
    
    # 检查是否已声明
    if var_name in variables:
        existing = variables[var_name]
        if existing.get("scope_level") == scope_level:
            # 同一作用域重复声明
            errors = symbol_table.setdefault("errors", [])
            errors.append({
                "type": "duplicate_declaration",
                "message": f"变量 '{var_name}' 重复声明",
                "line": line,
                "column": column
            })
            return
    
    # 记录变量
    variables[var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": scope_level
    }


# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed for this function node