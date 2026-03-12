# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "return", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int", "char", "void", etc.)
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
def _handle_return(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 return 语句节点，验证返回值类型与当前函数返回类型匹配。
    
    处理逻辑：
    1. 检查是否在全局作用域（无 current_function）
    2. 获取当前函数的返回类型声明
    3. 提取 return 语句中的返回值表达式
    4. 验证返回值类型与函数声明是否匹配
    5. 记录类型错误到 symbol_table["errors"]
    """
    # 初始化错误列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 步骤 1: 检查是否在全局作用域
    current_function = symbol_table.get("current_function")
    if current_function is None:
        error_msg = (
            f"Error: return statement outside function at "
            f"line {node.get('line', '?')}, column {node.get('column', '?')}"
        )
        symbol_table["errors"].append(error_msg)
        return
    
    # 步骤 2: 获取当前函数的返回类型声明
    functions = symbol_table.get("functions", {})
    func_info = functions.get(current_function)
    
    if func_info is None:
        error_msg = f"Error: function '{current_function}' not found in symbol table"
        symbol_table["errors"].append(error_msg)
        return
    
    declared_return_type = func_info.get("return_type")
    
    # 步骤 3: 提取 return 语句中的返回值表达式
    children = node.get("children", [])
    
    # 步骤 4: 验证返回值类型与函数声明是否匹配
    if len(children) == 0:
        # 没有返回值
        if declared_return_type and declared_return_type.lower() != "void":
            error_msg = (
                f"Error: missing return value in function '{current_function}' "
                f"which should return {declared_return_type}"
            )
            symbol_table["errors"].append(error_msg)
    else:
        # 有返回值，检查类型
        return_value_node = children[0]
        actual_return_type = return_value_node.get("data_type")
        
        if actual_return_type is None:
            error_msg = (
                f"Error: cannot determine return value type at "
                f"line {node.get('line', '?')}, column {node.get('column', '?')}"
            )
            symbol_table["errors"].append(error_msg)
        elif declared_return_type is None or declared_return_type.lower() == "void":
            error_msg = (
                f"Error: return value provided in void function '{current_function}' at "
                f"line {node.get('line', '?')}, column {node.get('column', '?')}"
            )
            symbol_table["errors"].append(error_msg)
        elif actual_return_type != declared_return_type:
            error_msg = (
                f"Error: return type mismatch in function '{current_function}'. "
                f"Expected {declared_return_type}, got {actual_return_type} at "
                f"line {node.get('line', '?')}, column {node.get('column', '?')}"
            )
            symbol_table["errors"].append(error_msg)

# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# Not needed for this function node
