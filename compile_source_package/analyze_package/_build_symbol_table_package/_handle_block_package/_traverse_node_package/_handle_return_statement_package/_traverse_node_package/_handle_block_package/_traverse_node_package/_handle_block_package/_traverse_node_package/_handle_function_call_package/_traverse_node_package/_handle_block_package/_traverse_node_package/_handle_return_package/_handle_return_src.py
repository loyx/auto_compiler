# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this utility handler

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "return", etc.)
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
def _handle_return(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 return 语句节点，验证返回值类型与函数声明匹配。
    
    验证逻辑：
    1. 检查是否在函数内部
    2. 验证返回值类型与函数声明的返回类型是否一致
    3. 记录类型错误到 symbol_table["errors"]
    """
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 1. 检查是否在函数内部
    current_function = symbol_table.get("current_function", "")
    if not current_function:
        symbol_table["errors"].append({
            "type": "return_outside_function",
            "message": "return 语句在函数外使用",
            "line": node.get("line", 0),
            "column": node.get("column", 0)
        })
        return
    
    # 2. 获取函数声明信息
    functions = symbol_table.get("functions", {})
    func_info = functions.get(current_function, {})
    declared_return_type = func_info.get("return_type", "void")
    
    # 3. 检查返回值
    children = node.get("children", [])
    
    if not children:
        # 无返回值的 return 语句
        if declared_return_type != "void":
            symbol_table["errors"].append({
                "type": "return_type_mismatch",
                "message": f"函数声明返回类型为 '{declared_return_type}'，但 return 无返回值",
                "line": node.get("line", 0),
                "column": node.get("column", 0)
            })
    else:
        # 有返回值的 return 语句
        return_expr = children[0]
        actual_return_type = return_expr.get("data_type", "void")
        
        if declared_return_type != "void" and actual_return_type != declared_return_type:
            symbol_table["errors"].append({
                "type": "return_type_mismatch",
                "message": f"返回值类型 '{actual_return_type}' 与函数声明返回类型 '{declared_return_type}' 不匹配",
                "line": node.get("line", 0),
                "column": node.get("column", 0)
            })


# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# Not needed - this is a utility function for internal AST processing
