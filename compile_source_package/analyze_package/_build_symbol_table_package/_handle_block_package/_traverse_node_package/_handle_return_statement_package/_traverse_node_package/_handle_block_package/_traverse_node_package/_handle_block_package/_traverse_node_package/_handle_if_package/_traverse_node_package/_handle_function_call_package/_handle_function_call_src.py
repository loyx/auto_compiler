# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "data_type": str,
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }


# === main function ===
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 function_call 类型节点。
    验证被调用函数是否已声明，并检查实参数量是否与形参数量匹配。
    副作用：可能向 symbol_table["errors"] 添加错误记录。
    """
    # 提取行列号
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 提取被调用函数名
    func_name = _extract_function_name(node)
    
    # 提取实参列表
    actual_args = _extract_arguments(node)
    
    # 检查函数是否已声明
    if func_name not in symbol_table.get("functions", {}):
        error = {
            "type": "error",
            "message": f"Undefined function: {func_name}",
            "line": line,
            "column": column
        }
        symbol_table.setdefault("errors", []).append(error)
        return
    
    # 获取函数声明信息
    func_info = symbol_table["functions"][func_name]
    expected_param_count = len(func_info.get("params", []))
    actual_arg_count = len(actual_args)
    
    # 验证参数数量
    if actual_arg_count != expected_param_count:
        error = {
            "type": "error",
            "message": f"Argument count mismatch for {func_name}",
            "line": line,
            "column": column
        }
        symbol_table["errors"].append(error)


# === helper functions ===
def _extract_function_name(node: AST) -> str:
    """
    从 AST 节点中提取被调用函数名。
    优先从 "value" 字段获取，若不存在则从 "children"[0] 获取。
    """
    if "value" in node:
        return str(node["value"])
    elif "children" in node and len(node["children"]) > 0:
        first_child = node["children"][0]
        if isinstance(first_child, dict) and "value" in first_child:
            return str(first_child["value"])
        return str(first_child)
    return ""


def _extract_arguments(node: AST) -> list:
    """
    从 AST 节点中提取实参列表。
    若存在 "arguments" 字段则直接使用，否则从 "children"[1:] 获取。
    """
    if "arguments" in node:
        return node["arguments"]
    elif "children" in node and len(node["children"]) > 1:
        return node["children"][1:]
    return []


# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function node
