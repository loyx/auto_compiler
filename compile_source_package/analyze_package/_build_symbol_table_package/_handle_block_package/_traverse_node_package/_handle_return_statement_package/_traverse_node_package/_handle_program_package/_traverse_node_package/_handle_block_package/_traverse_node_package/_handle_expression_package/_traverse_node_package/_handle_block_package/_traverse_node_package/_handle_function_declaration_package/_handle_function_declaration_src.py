# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block" 等)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int,           # 列号
#   "name": str,             # 名称 (用于 function_declaration, parameter 等)
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
    """处理函数声明节点，注册函数到符号表并处理函数体。"""
    func_name = node["name"]
    return_type = node["data_type"]
    line = node["line"]
    column = node["column"]
    
    params = _extract_params(node)
    
    symbol_table["functions"][func_name] = {
        "return_type": return_type,
        "params": params,
        "line": line,
        "column": column
    }
    
    symbol_table["current_scope"] += 1
    symbol_table["scope_stack"].append(func_name)
    
    try:
        for child in node["children"]:
            if child["type"] == "block":
                for stmt in child["children"]:
                    _traverse_node(stmt, symbol_table)
    finally:
        symbol_table["current_scope"] -= 1
        symbol_table["scope_stack"].pop()

# === helper functions ===
def _extract_params(node: AST) -> list:
    """从 function_declaration 节点中提取参数详细信息列表。"""
    params = []
    for child in node["children"]:
        if child["type"] == "parameter_list":
            for param in child["children"]:
                if param["type"] == "parameter":
                    params.append({
                        "name": param["name"],
                        "data_type": param["data_type"]
                    })
            break
    return params

# === OOP compatibility layer ===
