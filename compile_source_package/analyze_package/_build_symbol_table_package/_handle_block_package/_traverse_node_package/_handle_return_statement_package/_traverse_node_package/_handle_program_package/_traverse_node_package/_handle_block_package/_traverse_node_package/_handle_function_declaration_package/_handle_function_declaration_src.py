# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
# _traverse_node is a parent-level dependency, not a direct child
from .. import _traverse_node

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
    处理 'function_declaration' 类型节点。
    注册函数到符号表，处理参数和函数体。
    """
    # 1. 提取函数名
    func_name = node.get("value", "")
    if not func_name:
        return
    
    # 2. 提取返回类型、行号、列号
    return_type = node.get("data_type", "void")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 3. 检查函数是否已存在
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    
    if func_name in symbol_table["functions"]:
        # 记录重复定义错误
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append({
            "message": f"Duplicate function name '{func_name}'",
            "line": line,
            "column": column,
            "type": "duplicate_function"
        })
        return
    
    # 4. 提取参数列表
    params = _extract_params(node)
    
    # 5. 注册函数信息
    symbol_table["functions"][func_name] = {
        "return_type": return_type,
        "params": params,
        "line": line,
        "column": column
    }
    
    # 6. 设置当前函数上下文
    previous_function = symbol_table.get("current_function")
    symbol_table["current_function"] = func_name
    
    # 7. 遍历子节点
    for child in node.get("children", []):
        _traverse_node(child, symbol_table)
    
    # 8. 恢复当前函数上下文
    symbol_table["current_function"] = previous_function

# === helper functions ===
def _extract_params(node: AST) -> List[Dict[str, str]]:
    """
    从 function_declaration 节点中提取参数列表。
    查找 type 为 "parameter_list" 的子节点，提取其中的 "parameter" 节点。
    """
    params = []
    for child in node.get("children", []):
        if child.get("type") == "parameter_list":
            for param_node in child.get("children", []):
                if param_node.get("type") == "parameter":
                    param_name = param_node.get("value", "")
                    param_type = param_node.get("data_type", "void")
                    params.append({
                        "name": param_name,
                        "data_type": param_type
                    })
            break
    return params

# === OOP compatibility layer ===
# Not required for this function node
