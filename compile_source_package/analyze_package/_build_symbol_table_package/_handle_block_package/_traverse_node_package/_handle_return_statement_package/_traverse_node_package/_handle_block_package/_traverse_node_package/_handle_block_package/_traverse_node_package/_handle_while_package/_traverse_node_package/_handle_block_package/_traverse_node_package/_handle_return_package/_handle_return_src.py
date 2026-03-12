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
#   "errors": list                 # 错误列表 [{message, line, column, type}]
# }

# === main function ===
def _handle_return(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理返回语句节点，验证返回值类型与函数声明是否匹配。
    
    处理逻辑：
    1. 从 node 中提取返回值表达式（如果有）
    2. 检查 symbol_table['current_function'] 是否存在
    3. 如果存在，获取函数的返回类型声明
    4. 验证返回值类型是否与函数声明的返回类型匹配
    5. 如果 return 在函数外部使用，记录错误
    """
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 获取节点位置信息
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 提取返回值表达式
    children = node.get("children", [])
    if len(children) > 0:
        return_expr = children[0]
        has_return_value = True
    else:
        return_expr = None
        has_return_value = False
    
    # 获取当前函数名
    current_function = symbol_table.get("current_function", "")
    
    # 检查是否在函数外部使用 return
    if not current_function:
        symbol_table["errors"].append({
            "message": "Return statement outside of function",
            "line": line,
            "column": column,
            "type": "return_outside_function"
        })
        return
    
    # 获取函数信息
    functions = symbol_table.get("functions", {})
    func_info = functions.get(current_function, {})
    
    # 检查函数是否存在于符号表中
    if not func_info:
        # 函数未声明，记录错误
        symbol_table["errors"].append({
            "message": f"Return in undeclared function '{current_function}'",
            "line": line,
            "column": column,
            "type": "return_outside_function"
        })
        return
    
    # 获取函数返回类型
    expected_type = func_info.get("return_type", "")
    
    # 处理 void 函数
    if expected_type == "void":
        if has_return_value:
            symbol_table["errors"].append({
                "message": "Void function cannot return a value",
                "line": line,
                "column": column,
                "type": "void_function_return_value"
            })
        return
    
    # 处理有返回值的 return 语句
    if has_return_value:
        return_type = return_expr.get("data_type", "")
        
        # 严格字符串比较类型
        if return_type != expected_type:
            symbol_table["errors"].append({
                "message": f"Return type '{return_type}' does not match function return type '{expected_type}'",
                "line": line,
                "column": column,
                "type": "return_type_mismatch"
            })
    else:
        # 非 void 函数但没有返回值
        symbol_table["errors"].append({
            "message": f"Non-void function '{current_function}' must return a value",
            "line": line,
            "column": column,
            "type": "return_type_mismatch"
        })

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this semantic analysis function
