# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", etc.)
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
    """
    处理函数声明节点：记录函数信息到 symbol_table['functions']。
    
    处理步骤：
    1. 提取函数名、返回类型、位置信息
    2. 解析参数列表
    3. 记录函数信息到符号表
    4. 设置 current_function 上下文
    5. 遍历函数体
    6. 恢复 current_function
    """
    func_name = node.get("value")
    return_type = node.get("data_type", "void")
    line = node.get("line", 0)
    column = node.get("column", 0)
    children = node.get("children", [])
    
    # 解析参数列表（第一个子节点通常是参数列表）
    params = []
    if len(children) > 0 and children[0].get("type") == "param_list":
        param_nodes = children[0].get("children", [])
        for param_node in param_nodes:
            param_info = {
                "name": param_node.get("value"),
                "data_type": param_node.get("data_type", "int"),
                "line": param_node.get("line", 0),
                "column": param_node.get("column", 0)
            }
            params.append(param_info)
    
    # 记录函数信息到符号表
    symbol_table["functions"][func_name] = {
        "return_type": return_type,
        "params": params,
        "line": line,
        "column": column
    }
    
    # 保存旧的 current_function 并设置新的
    old_function = symbol_table.get("current_function")
    symbol_table["current_function"] = func_name
    
    # 处理函数体（寻找 block 类型的子节点）
    for child in children:
        if child.get("type") == "block":
            _traverse_node(child, symbol_table)
            break
    
    # 恢复 current_function
    symbol_table["current_function"] = old_function

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node