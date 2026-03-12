# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions - INLINE implementation

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
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理函数调用节点，验证函数声明和参数匹配。
    
    验证内容：
    1. 函数是否已声明
    2. 参数数量是否匹配
    3. 参数类型是否匹配
    
    错误记录到 symbol_table['errors']，不抛出异常。
    """
    func_name = node.get("value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    arg_nodes = node.get("children", [])
    
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 检查函数是否已声明
    functions = symbol_table.get("functions", {})
    if func_name not in functions:
        error_msg = f"未声明的函数 '{func_name}'"
        symbol_table["errors"].append({
            "type": "undeclared_function",
            "message": error_msg,
            "line": line,
            "column": column,
            "function_name": func_name
        })
        return
    
    # 获取函数声明信息
    func_decl = functions[func_name]
    declared_params = func_decl.get("params", [])
    
    # 验证参数数量
    if len(arg_nodes) != len(declared_params):
        error_msg = f"函数 '{func_name}' 参数数量不匹配：期望 {len(declared_params)} 个，实际 {len(arg_nodes)} 个"
        symbol_table["errors"].append({
            "type": "parameter_count_mismatch",
            "message": error_msg,
            "line": line,
            "column": column,
            "function_name": func_name,
            "expected_count": len(declared_params),
            "actual_count": len(arg_nodes)
        })
        return
    
    # 验证参数类型
    _validate_parameter_types(arg_nodes, declared_params, func_name, line, column, symbol_table)


# === helper functions ===
def _validate_parameter_types(
    arg_nodes: list,
    declared_params: list,
    func_name: str,
    line: int,
    column: int,
    symbol_table: SymbolTable
) -> None:
    """
    验证每个参数的类型是否与函数声明匹配。
    
    类型匹配规则：
    - 完全匹配：参数类型与声明类型相同
    - 不匹配时记录错误但不中断
    """
    for idx, (arg_node, param_decl) in enumerate(zip(arg_nodes, declared_params)):
        arg_type = arg_node.get("data_type")
        expected_type = param_decl.get("data_type") if isinstance(param_decl, dict) else param_decl
        
        if arg_type and expected_type and arg_type != expected_type:
            error_msg = f"函数 '{func_name}' 参数 {idx + 1} 类型不匹配：期望 '{expected_type}'，实际 '{arg_type}'"
            symbol_table["errors"].append({
                "type": "parameter_type_mismatch",
                "message": error_msg,
                "line": line,
                "column": column,
                "function_name": func_name,
                "parameter_index": idx,
                "expected_type": expected_type,
                "actual_type": arg_type
            })


# === OOP compatibility layer ===
# Not needed - this is a semantic analysis helper function, not a framework entry point
