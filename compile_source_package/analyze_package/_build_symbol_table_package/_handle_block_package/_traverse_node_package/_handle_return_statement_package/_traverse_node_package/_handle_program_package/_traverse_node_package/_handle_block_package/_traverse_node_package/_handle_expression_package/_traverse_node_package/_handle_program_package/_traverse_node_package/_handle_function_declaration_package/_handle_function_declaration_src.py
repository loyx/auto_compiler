# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions delegated

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


# === main function ===
def _handle_function_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理函数声明节点，注册函数到符号表。
    
    处理逻辑：
    1. 从 node 中提取函数名、返回类型、参数列表
    2. 检查函数是否已存在，已存在则记录错误
    3. 不存在则注册函数信息
    4. 更新 current_function，进入新作用域
    """
    # 提取函数名（children[0] 是 identifier 节点）
    func_name = node["children"][0]["value"]
    line = node.get("line")
    column = node.get("column")
    
    # 提取返回类型（默认为 "void"）
    return_type = node.get("data_type", "void")
    
    # 提取参数列表（children[1] 是 parameter_list 节点，如果存在）
    params = []
    if len(node.get("children", [])) > 1 and node["children"][1].get("type") == "parameter_list":
        param_list_node = node["children"][1]
        for param_node in param_list_node.get("children", []):
            if param_node.get("type") == "parameter":
                param_name = param_node["children"][0]["value"]
                param_type = param_node.get("data_type", "void")
                params.append({"name": param_name, "type": param_type})
    
    # 检查函数是否已存在
    if func_name in symbol_table.get("functions", {}):
        # 记录重定义错误
        error = {
            "type": "function_redefined",
            "message": f"Function '{func_name}' redefined at line {line}",
            "line": line,
            "column": column
        }
        symbol_table.setdefault("errors", []).append(error)
    else:
        # 注册函数到符号表
        symbol_table.setdefault("functions", {})[func_name] = {
            "return_type": return_type,
            "params": params,
            "line": line,
            "column": column
        }
    
    # 更新 current_function
    symbol_table["current_function"] = func_name
    
    # 进入新作用域
    symbol_table["current_scope"] = symbol_table.get("current_scope", 0) + 1
    symbol_table.setdefault("scope_stack", []).append(symbol_table["current_scope"])


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
