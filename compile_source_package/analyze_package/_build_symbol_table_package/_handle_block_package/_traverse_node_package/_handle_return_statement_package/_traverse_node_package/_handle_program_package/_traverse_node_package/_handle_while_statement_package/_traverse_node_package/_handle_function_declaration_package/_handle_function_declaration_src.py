# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
# 无子函数，此函数为叶子节点

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
    处理 function_declaration 类型 AST 节点。
    
    从节点中提取函数名、返回类型、参数列表，并注册到符号表。
    
    Args:
        node: AST 节点，类型为 "function_declaration"
        symbol_table: 符号表，将被修改以添加函数信息
    
    Returns:
        None
    """
    # 0. 确保符号表字段已初始化
    symbol_table.setdefault("errors", [])
    symbol_table.setdefault("functions", {})
    
    # 1. 提取函数名
    func_name = node.get("value")
    if not func_name:
        # 如果函数名为空，记录错误并返回
        symbol_table["errors"].append("函数声明缺少函数名")
        return
    
    # 2. 检查重复声明
    functions = symbol_table["functions"]
    if func_name in functions:
        error_msg = f"函数 '{func_name}' 重复声明"
        symbol_table["errors"].append(error_msg)
        return
    
    # 3. 提取返回类型
    return_type = node.get("data_type", "void")
    
    # 4. 提取行号和列号
    line = node.get("line", -1)
    column = node.get("column", -1)
    
    # 5. 提取参数列表
    param_list = _extract_parameters(node.get("children", []))
    
    # 6. 注册函数信息
    functions[func_name] = {
        "return_type": return_type,
        "params": param_list,
        "line": line,
        "column": column
    }
    
    # 7. 设置当前函数
    symbol_table["current_function"] = func_name

# === helper functions ===
def _extract_parameters(children: List[AST]) -> List[Dict[str, Any]]:
    """
    从子节点列表中提取参数信息。
    
    Args:
        children: AST 子节点列表
        
    Returns:
        参数列表，每个参数为字典：{"name": str, "data_type": str, "line": int, "column": int}
    """
    params = []
    
    for child in children:
        if child.get("type") == "variable_declaration":
            param_name = child.get("value")
            param_type = child.get("data_type", "int")
            param_line = child.get("line", -1)
            param_column = child.get("column", -1)
            
            if param_name:
                params.append({
                    "name": param_name,
                    "data_type": param_type,
                    "line": param_line,
                    "column": param_column
                })
    
    return params

# === OOP compatibility layer ===
# 无框架要求，省略此部分