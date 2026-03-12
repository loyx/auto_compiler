# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", "function_decl", "param_list", "param", etc.)
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
    """处理函数声明节点，将函数信息记录到符号表中并处理函数体。"""
    # 确保必要的字段已初始化
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 1. 提取函数元数据
    func_name = node.get("value")
    return_type = node.get("data_type", "int")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 2. 检查函数是否已存在
    if func_name in symbol_table["functions"]:
        # 3. 记录重复声明错误
        symbol_table["errors"].append({
            "type": "duplicate_function",
            "message": f"Function '{func_name}' is already declared",
            "line": line,
            "column": column
        })
        return
    
    # 4. 解析参数列表
    params = _parse_param_list(node.get("children", []))
    
    # 5. 将函数信息添加到符号表
    symbol_table["functions"][func_name] = {
        "return_type": return_type,
        "params": params,
        "line": line,
        "column": column
    }
    
    # 6. 设置当前函数上下文
    prev_function = symbol_table.get("current_function")
    symbol_table["current_function"] = func_name
    
    # 7. 递归处理函数体（通常是 block 节点）
    children = node.get("children", [])
    for child in children:
        if child.get("type") == "block":
            _traverse_node(child, symbol_table)
            break
    
    # 8. 恢复之前的函数上下文
    symbol_table["current_function"] = prev_function

# === helper functions ===
def _parse_param_list(children: list) -> list:
    """从函数声明节点的子节点中解析参数列表。"""
    params = []
    for child in children:
        if child.get("type") == "param_list":
            param_children = child.get("children", [])
            for param_node in param_children:
                if param_node.get("type") == "param":
                    params.append({
                        "name": param_node.get("value"),
                        "data_type": param_node.get("data_type", "int"),
                        "line": param_node.get("line", 0),
                        "column": param_node.get("column", 0)
                    })
            break
    return params

# === OOP compatibility layer ===
# Not needed for this helper function node
