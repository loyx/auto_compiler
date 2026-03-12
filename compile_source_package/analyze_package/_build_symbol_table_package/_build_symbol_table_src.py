# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
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
#   "scope_stack": list            # 作用域栈
# }


# === main function ===
def _build_symbol_table(ast: AST, symbol_table: SymbolTable) -> None:
    """
    第一遍遍历：收集所有函数定义和变量声明，填充 symbol_table。
    
    输入：AST 根节点和空 symbol_table
    输出：无返回值，副作用是修改 symbol_table
    不处理：使用验证（留到第二遍）
    """
    _traverse_node(ast, symbol_table)


# === helper functions ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """递归遍历 AST 节点，收集函数定义和变量声明。"""
    node_type = node.get("type", "")
    
    if node_type == "function_def":
        _handle_function_def(node, symbol_table)
    elif node_type == "variable_decl":
        _handle_variable_decl(node, symbol_table)
    elif node_type == "block":
        _handle_block(node, symbol_table)
    else:
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)


def _handle_function_def(node: AST, symbol_table: SymbolTable) -> None:
    """处理函数定义节点：记录函数信息，进入作用域，处理参数和函数体。"""
    func_name = node.get("value")
    return_type = node.get("data_type", "int")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    symbol_table["functions"][func_name] = {
        "return_type": return_type,
        "params": [],
        "line": line,
        "column": column,
    }
    
    symbol_table["current_scope"] += 1
    symbol_table["scope_stack"].append(func_name)
    
    for child in node.get("children", []):
        child_type = child.get("type", "")
        if child_type == "param_list":
            _handle_param_list(child, symbol_table, func_name)
        elif child_type == "block":
            _handle_block(child, symbol_table)
        else:
            _traverse_node(child, symbol_table)
    
    symbol_table["current_scope"] -= 1
    symbol_table["scope_stack"].pop()


def _handle_param_list(param_list: AST, symbol_table: SymbolTable, func_name: str) -> None:
    """处理参数列表：将参数作为局部变量加入符号表。"""
    params = []
    for param in param_list.get("children", []):
        if param.get("type") == "param":
            param_name = param.get("value")
            param_type = param.get("data_type", "int")
            params.append(param_name)
            
            symbol_table["variables"][param_name] = {
                "data_type": param_type,
                "is_declared": True,
                "line": param.get("line", 0),
                "column": param.get("column", 0),
                "scope_level": symbol_table["current_scope"],
            }
    
    if func_name in symbol_table["functions"]:
        symbol_table["functions"][func_name]["params"] = params


def _handle_variable_decl(node: AST, symbol_table: SymbolTable) -> None:
    """处理变量声明节点：记录变量信息。"""
    var_name = node.get("value")
    var_type = node.get("data_type", "int")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    if var_name not in symbol_table["variables"]:
        symbol_table["variables"][var_name] = {
            "data_type": var_type,
            "is_declared": True,
            "line": line,
            "column": column,
            "scope_level": symbol_table["current_scope"],
        }


# === OOP compatibility layer ===
# (not needed - this is a helper function node)
