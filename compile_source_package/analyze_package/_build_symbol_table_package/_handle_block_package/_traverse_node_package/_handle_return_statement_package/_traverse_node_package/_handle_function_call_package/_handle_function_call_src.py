# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
# No sub functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "function_call")
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "name": str,             # 被调用的函数名
#   "arguments": list        # 参数列表
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
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 function_call 类型节点（函数调用）。
    验证被调用函数是否已声明、参数数量是否匹配、参数类型是否兼容。
    副作用：可能向 symbol_table['errors'] 添加错误信息。
    """
    # 提取位置信息
    line = _get_line_column(node, "line")
    column = _get_line_column(node, "column")
    
    # 提取被调用的函数名
    func_name = node.get("name")
    if not func_name and node.get("children"):
        func_name = node["children"][0].get("value") if node["children"] else None
    
    if not func_name:
        return
    
    # 确保 errors 列表存在
    errors = symbol_table.setdefault("errors", [])
    
    # 检查函数是否已声明
    functions = symbol_table.get("functions", {})
    if func_name not in functions:
        errors.append(f"Error: Function '{func_name}' not declared at line {line}, column {column}")
        return
    
    # 获取函数定义
    func_def = functions[func_name]
    expected_params = func_def.get("params", [])
    expected_count = len(expected_params)
    
    # 提取实参列表
    arguments = _extract_arguments(node)
    actual_count = len(arguments)
    
    # 检查参数数量
    if actual_count != expected_count:
        errors.append(
            f"Error: Function '{func_name}' expects {expected_count} arguments "
            f"but got {actual_count} at line {line}, column {column}"
        )
        return
    
    # 类型检查（如果实参有 data_type 信息）
    for i, arg in enumerate(arguments):
        if i >= len(expected_params):
            break
        arg_type = arg.get("data_type")
        expected_type = expected_params[i].get("data_type")
        
        if arg_type and expected_type and arg_type != expected_type:
            errors.append(
                f"Error: Type mismatch in argument {i + 1} for function '{func_name}': "
                f"expected '{expected_type}', got '{arg_type}' at line {line}, column {column}"
            )


# === helper functions ===
def _get_line_column(node: AST, field: str) -> Any:
    """
    从节点中提取 line 或 column 字段。
    优先使用 node 自身的字段，如果没有则从 children[0] 获取。
    """
    value = node.get(field)
    if value is not None:
        return value
    
    children = node.get("children", [])
    if children and len(children) > 0:
        value = children[0].get(field)
        if value is not None:
            return value
    
    return "?"


def _extract_arguments(node: AST) -> List[AST]:
    """
    从 function_call 节点中提取实参列表。
    优先使用 arguments 字段，否则使用 children[1:]。
    """
    if "arguments" in node and isinstance(node["arguments"], list):
        return node["arguments"]
    
    children = node.get("children", [])
    if len(children) > 1:
        return children[1:]
    
    return []


# === OOP compatibility layer ===
# Not needed for this handler function
