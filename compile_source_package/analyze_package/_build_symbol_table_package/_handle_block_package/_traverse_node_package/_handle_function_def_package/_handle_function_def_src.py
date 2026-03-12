# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions to import

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "value": str,            # 节点值（函数名、变量名等）
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
def _handle_function_def(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 function_def 类型节点，将函数信息注册到符号表中。
    
    从 node 中提取函数名、返回类型、参数列表、位置信息，
    并在 symbol_table['functions'] 中添加或覆盖函数记录。
    """
    func_name = node.get("value", "")
    return_type = node.get("data_type", "int")
    line = node.get("line", 0)
    column = node.get("column", 0)
    children = node.get("children", [])
    
    params = _extract_params(children)
    
    symbol_table["functions"][func_name] = {
        "return_type": return_type,
        "params": params,
        "line": line,
        "column": column
    }


# === helper functions ===
def _extract_params(children: list) -> Dict[str, str]:
    """
    从参数 AST 节点列表中提取参数名到参数类型的映射。
    
    输入：children 列表，每个元素是参数 AST 节点
    输出：{param_name: param_type} 字典
    """
    params = {}
    for child in children:
        param_name = child.get("value", "")
        param_type = child.get("data_type", "int")
        if param_name:
            params[param_name] = param_type
    return params


# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function