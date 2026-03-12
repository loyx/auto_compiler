# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this module

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
#   "errors": list                 # 错误列表 (可选)
# }


# === main function ===
def _handle_function_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 function_declaration 类型的 AST 节点，将函数信息注册到符号表。
    """
    # 提取函数名（优先从 "value" 字段，其次 "name" 字段）
    func_name = node.get("value") or node.get("name")
    if not func_name:
        symbol_table.setdefault("errors", []).append({
            "type": "missing_function_name",
            "line": node.get("line", 0),
            "column": node.get("column", 0)
        })
        return
    
    # 提取返回类型
    return_type = node.get("data_type", "int")
    if return_type not in ("int", "char"):
        symbol_table.setdefault("errors", []).append({
            "type": "invalid_return_type",
            "function": func_name,
            "return_type": return_type,
            "line": node.get("line", 0),
            "column": node.get("column", 0)
        })
        return_type = "int"  # 默认返回类型
    
    # 提取位置信息
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 提取参数列表（从 "children" 或 "params" 字段）
    params = node.get("params") or node.get("children", [])
    
    # 检查函数是否已存在
    functions = symbol_table.setdefault("functions", {})
    if func_name in functions:
        symbol_table.setdefault("errors", []).append({
            "type": "duplicate_function_declaration",
            "function": func_name,
            "line": line,
            "column": column
        })
    
    # 注册函数信息到符号表
    functions[func_name] = {
        "return_type": return_type,
        "params": params,
        "line": line,
        "column": column
    }
    
    # 设置当前函数名
    symbol_table["current_function"] = func_name


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
