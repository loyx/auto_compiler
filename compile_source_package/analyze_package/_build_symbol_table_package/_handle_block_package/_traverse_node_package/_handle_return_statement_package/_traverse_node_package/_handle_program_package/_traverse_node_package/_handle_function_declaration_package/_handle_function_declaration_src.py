# === std / third-party imports ===
from typing import Any, Dict, List, Optional

# === sub function imports ===
# No child functions needed for this module

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
    处理 function_declaration 类型节点。
    从 node 提取函数名、返回类型、参数信息，注册到 symbol_table['functions']。
    输入：function_declaration 类型的 AST 节点和符号表。
    处理：验证函数是否重复声明，注册函数信息。
    副作用：修改 symbol_table['functions']，可能添加错误到 symbol_table['errors']。
    异常：无。
    """
    # 提取函数名（可能在 "value" 或 "name" 字段）
    func_name: Optional[str] = node.get("value") or node.get("name")
    if not func_name:
        _add_error(symbol_table, "无法提取函数名", node.get("line", 0), node.get("column", 0))
        return
    
    # 提取返回类型（"data_type" 字段，值为 "int" 或 "char"）
    return_type: str = node.get("data_type", "int")
    if return_type not in ("int", "char"):
        _add_error(symbol_table, f"无效的返回类型: {return_type}", node.get("line", 0), node.get("column", 0))
        return_type = "int"  # 默认回退
    
    # 提取行号和列号
    line: int = node.get("line", 0)
    column: int = node.get("column", 0)
    
    # 提取参数列表（"params" 或 "parameters" 字段）
    params: List[Dict[str, Any]] = node.get("params") or node.get("parameters") or []
    
    # 获取当前作用域层级
    scope_level: int = symbol_table.get("current_scope", 0)
    
    # 检查函数是否已声明
    functions_dict: Dict[str, Dict] = symbol_table.setdefault("functions", {})
    
    if func_name in functions_dict:
        # 重复声明错误
        _add_error(symbol_table, f"函数 '{func_name}' 重复声明", line, column)
        return
    
    # 注册函数信息到 symbol_table["functions"]
    functions_dict[func_name] = {
        "return_type": return_type,
        "params": params,
        "line": line,
        "column": column,
        "scope_level": scope_level
    }
    
    # 设置 symbol_table["current_function"] 为当前函数名
    symbol_table["current_function"] = func_name
    
    # 处理函数体（如果有 "children" 或 "body" 字段）
    body: Optional[List[AST]] = node.get("children") or node.get("body")
    if body:
        _process_function_body(body, symbol_table)


# === helper functions ===
def _add_error(symbol_table: SymbolTable, message: str, line: int, column: int) -> None:
    """添加错误信息到符号表的 errors 列表。"""
    errors: List[Dict[str, Any]] = symbol_table.setdefault("errors", [])
    errors.append({
        "type": "declaration_error",
        "message": message,
        "line": line,
        "column": column
    })


def _process_function_body(body: List[AST], symbol_table: SymbolTable) -> None:
    """
    处理函数体中的子节点。
    注意：此函数仅作为占位，实际处理逻辑应由专门的节点处理函数负责。
    当前实现仅遍历节点，不执行具体处理。
    """
    # 函数体处理应委托给其他专门的节点处理函数
    # 此处仅作遍历，避免循环依赖
    for child_node in body:
        # 子节点处理应由调用方根据节点类型分派
        pass


# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function module
