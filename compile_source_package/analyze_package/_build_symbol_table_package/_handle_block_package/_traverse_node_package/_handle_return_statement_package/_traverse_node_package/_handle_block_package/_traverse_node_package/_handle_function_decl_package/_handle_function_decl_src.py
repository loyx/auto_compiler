# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
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
#   "scope_stack": list,           # 作用域栈 (存储旧 scope 值)
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }


# === main function ===
def _handle_function_decl(node: AST, symbol_table: SymbolTable) -> None:
    """处理函数声明节点，记录函数信息到符号表并处理函数体。"""
    func_name = node["value"]
    return_type = node["data_type"]
    line = node["line"]
    column = node["column"]
    
    # 检查函数是否已声明
    if func_name in symbol_table["functions"]:
        symbol_table["errors"].append(
            f"Function '{func_name}' already declared at line {line}, column {column}"
        )
        return
    
    # 解析参数列表 (children[0] 是参数列表)
    params_list = []
    if node.get("children") and len(node["children"]) > 0:
        param_list_node = node["children"][0]
        if param_list_node.get("type") == "param_list":
            for param in param_list_node.get("children", []):
                params_list.append({
                    "name": param.get("value"),
                    "data_type": param.get("data_type", "int")
                })
    
    # 记录函数信息
    symbol_table["functions"][func_name] = {
        "return_type": return_type,
        "params": params_list,
        "line": line,
        "column": column
    }
    
    # 设置当前函数上下文
    old_function = symbol_table.get("current_function")
    symbol_table["current_function"] = func_name
    
    # 处理函数体 (children[1] 是函数体块)
    if node.get("children") and len(node["children"]) > 1:
        body_node = node["children"][1]
        _traverse_node(body_node, symbol_table)
    
    # 恢复当前函数上下文
    symbol_table["current_function"] = old_function


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this semantic analysis function