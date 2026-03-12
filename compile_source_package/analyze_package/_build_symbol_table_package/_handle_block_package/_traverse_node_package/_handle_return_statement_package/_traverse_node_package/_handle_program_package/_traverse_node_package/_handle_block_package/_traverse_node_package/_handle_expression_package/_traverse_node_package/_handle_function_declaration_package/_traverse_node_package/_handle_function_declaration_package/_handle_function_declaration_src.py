# === std / third-party imports ===
from typing import Any, Dict, List, Optional

# === sub function imports ===
from ._extract_parameters_package._extract_parameters_src import _extract_parameters

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
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

FunctionParam = Dict[str, str]
# FunctionParam possible fields:
# {
#   "name": str,
#   "data_type": str
# }

# === main function ===
def _handle_function_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """处理 function_declaration 节点，注册函数声明到符号表。"""
    func_name_node = _find_identifier_node(node)
    
    if func_name_node is None:
        _add_error(symbol_table, "无法找到函数名", node.get("line"), node.get("column"))
        return
    
    func_name = func_name_node.get("value", "")
    
    if func_name in symbol_table.get("functions", {}):
        _add_error(symbol_table, f"函数 '{func_name}' 重复声明", node.get("line"), node.get("column"))
        return
    
    return_type = _extract_return_type(node)
    if return_type is None:
        _add_error(symbol_table, "无法确定函数返回类型", node.get("line"), node.get("column"))
        return
    
    params: List[FunctionParam] = _extract_parameters(node)
    
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    
    symbol_table["functions"][func_name] = {
        "return_type": return_type,
        "params": params,
        "line": node.get("line"),
        "column": node.get("column")
    }
    
    symbol_table["current_function"] = func_name
    symbol_table["current_scope"] = symbol_table.get("current_scope", 0) + 1


# === helper functions ===
def _find_identifier_node(node: AST) -> Optional[AST]:
    """在子节点中查找 identifier 节点（函数名）。"""
    for child in node.get("children", []):
        if child.get("type") == "identifier":
            return child
    return None


def _extract_return_type(node: AST) -> Optional[str]:
    """提取返回类型（"int" 或 "char"）。"""
    for child in node.get("children", []):
        if child.get("type") in ("int", "char"):
            return child.get("type")
        if child.get("data_type") in ("int", "char"):
            return child.get("data_type")
    
    if node.get("data_type") in ("int", "char"):
        return node.get("data_type")
    return None


def _add_error(symbol_table: SymbolTable, message: str, line: Optional[int], column: Optional[int]) -> None:
    """向 errors 列表添加错误信息。"""
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    error_entry = {"message": message}
    if line is not None:
        error_entry["line"] = line
    if column is not None:
        error_entry["column"] = column
    
    symbol_table["errors"].append(error_entry)