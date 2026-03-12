# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }


# === main function ===
def _handle_function_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理函数声明节点，将函数信息注册到符号表。
    
    副作用：原地修改 symbol_table['functions'] 和 'current_function'
    """
    # 确保 functions 字典存在
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    
    # 提取函数基本信息
    func_name = node.get("value", "")
    return_type = node.get("data_type", "void")
    line = node.get("line", -1)
    column = node.get("column", -1)
    
    # 提取参数列表
    params = []
    for child in node.get("children", []):
        if child.get("type") == "parameter":
            params.append({
                "name": child.get("value", ""),
                "data_type": child.get("data_type", "void")
            })
    
    # 检查函数名冲突
    if func_name in symbol_table["functions"]:
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append({
            "type": "duplicate_function",
            "name": func_name,
            "line": line,
            "column": column
        })
    else:
        # 注册函数信息
        symbol_table["functions"][func_name] = {
            "return_type": return_type,
            "params": params,
            "line": line,
            "column": column
        }
    
    # 设置当前函数上下文
    symbol_table["current_function"] = func_name


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
