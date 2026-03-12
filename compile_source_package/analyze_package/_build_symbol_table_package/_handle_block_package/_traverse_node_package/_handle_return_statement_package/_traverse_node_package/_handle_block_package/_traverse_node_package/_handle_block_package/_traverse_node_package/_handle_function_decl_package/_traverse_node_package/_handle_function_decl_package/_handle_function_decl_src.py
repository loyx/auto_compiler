# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

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
def _handle_function_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理函数声明节点，将函数信息注册到符号表。
    
    处理逻辑：
    1. 从 node["value"] 获取函数名
    2. 从 node["data_type"] 获取返回类型
    3. 从 node["children"] 中提取参数列表（param_list 类型的子节点）
    4. 解析参数列表，构建参数信息（参数名、类型）
    5. 将函数信息注册到 symbol_table["functions"][func_name]
    6. 如果函数已存在，记录"重复函数声明"错误
    7. 更新 symbol_table["current_function"] 为当前函数名
    """
    # 验证必要字段
    if "value" not in node:
        _record_error(symbol_table, "函数声明缺少函数名", node.get("line", 0), node.get("column", 0))
        return
    
    if "data_type" not in node:
        _record_error(symbol_table, "函数声明缺少返回类型", node.get("line", 0), node.get("column", 0))
        return
    
    func_name = node["value"]
    return_type = node["data_type"]
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 检查函数是否已存在
    if func_name in symbol_table.get("functions", {}):
        _record_error(symbol_table, f"重复函数声明：{func_name}", line, column)
        return
    
    # 解析参数列表
    params = _extract_params(node.get("children", []))
    
    # 初始化 functions 字典（如果不存在）
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    
    # 注册函数信息
    symbol_table["functions"][func_name] = {
        "return_type": return_type,
        "params": params,
        "line": line,
        "column": column
    }
    
    # 更新当前函数名
    symbol_table["current_function"] = func_name

# === helper functions ===
def _extract_params(children: list) -> list:
    """
    从 AST 子节点列表中提取参数列表。
    
    参数列表是 param_list 类型的节点，包含多个 param 类型的子节点。
    每个 param 节点包含 "value"(参数名) 和 "data_type"(参数类型)。
    
    返回：[{name: str, data_type: str}, ...]
    """
    params = []
    
    for child in children:
        if child.get("type") == "param_list":
            # 遍历 param_list 的子节点
            for param_node in child.get("children", []):
                if param_node.get("type") == "param":
                    param_name = param_node.get("value")
                    param_type = param_node.get("data_type", "int")  # 默认为 int
                    
                    if param_name:
                        params.append({
                            "name": param_name,
                            "data_type": param_type
                        })
            break
    
    return params

def _record_error(symbol_table: SymbolTable, message: str, line: int, column: int) -> None:
    """
    记录错误到符号表的 errors 列表中。
    
    错误格式：{"message": str, "line": int, "column": int}
    """
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    symbol_table["errors"].append({
        "message": message,
        "line": line,
        "column": column
    })

# === OOP compatibility layer ===
# Not needed for this utility function