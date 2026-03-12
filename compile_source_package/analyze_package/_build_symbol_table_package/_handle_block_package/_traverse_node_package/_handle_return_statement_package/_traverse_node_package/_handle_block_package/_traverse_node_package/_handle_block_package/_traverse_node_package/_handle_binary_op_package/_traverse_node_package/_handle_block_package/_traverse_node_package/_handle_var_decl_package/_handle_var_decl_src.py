# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple logic

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "binary_op", "literal", "identifier", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (如操作符、变量名、字面量值等)
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
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点，验证并记录变量信息到符号表。
    
    处理逻辑：
    1. 从 node["value"] 获取变量名
    2. 从 node["data_type"] 获取数据类型（默认为 "int"）
    3. 检查变量是否已在 symbol_table["variables"] 中存在
    4. 如果已存在，记录"重复声明"错误
    5. 如果不存在，将变量信息添加到 symbol_table["variables"]
    """
    # 验证节点必要字段
    if "value" not in node:
        error_msg = f"变量声明节点缺少 'value' 字段 (line={node.get('line', '?')}, column={node.get('column', '?')})"
        symbol_table.setdefault("errors", []).append(error_msg)
        return
    
    var_name = node["value"]
    data_type = node.get("data_type", "int")
    line = node.get("line", -1)
    column = node.get("column", -1)
    
    # 确保 variables 字典存在
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 检查变量是否已声明
    if var_name in symbol_table["variables"]:
        error_msg = f"变量 '{var_name}' 重复声明 (line={line}, column={column})"
        symbol_table.setdefault("errors", []).append(error_msg)
        return
    
    # 记录变量信息到符号表
    current_scope = symbol_table.get("current_scope", 0)
    symbol_table["variables"][var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
