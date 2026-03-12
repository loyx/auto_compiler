# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# _traverse_node is a parent function, import from parent directory
from .._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "binary_op", "identifier", "literal", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (操作符或变量名)
#   "data_type": str,        # 类型信息 ("int" 或 "char", 可选)
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
def _handle_binary_op(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理二元操作节点，验证操作数类型兼容性。
    
    处理逻辑：
    1. 先递归调用 _traverse_node 处理左右操作数子节点
    2. 获取运算符和左右操作数类型
    3. 检查类型兼容性，不兼容时记录错误到 symbol_table["errors"]
    
    副作用：可能向 symbol_table["errors"] 追加错误记录
    """
    # 1. 先递归处理左右操作数子节点
    children = node.get("children", [])
    if len(children) >= 2:
        _traverse_node(children[0], symbol_table)  # 左操作数
        _traverse_node(children[1], symbol_table)  # 右操作数
    
    # 2. 获取运算符
    op = node.get("value", "")
    
    # 3. 获取左右操作数类型
    left_type = _get_operand_type(children[0], symbol_table) if len(children) >= 1 else None
    right_type = _get_operand_type(children[1], symbol_table) if len(children) >= 2 else None
    
    # 4. 类型兼容性检查
    if left_type and right_type:
        if not _check_type_compatibility(op, left_type, right_type):
            # 记录错误
            if "errors" not in symbol_table:
                symbol_table["errors"] = []
            symbol_table["errors"].append({
                "line": node.get("line", 0),
                "column": node.get("column", 0),
                "message": f"Cannot apply '{op}' to types '{left_type}' and '{right_type}'"
            })


# === helper functions ===
def _get_operand_type(operand_node: AST, symbol_table: SymbolTable) -> str | None:
    """
    获取操作数的数据类型。
    
    优先级：
    1. 节点自身有 data_type 字段（字面量、已类型标注的表达式）
    2. 如果操作数是变量引用（type == "identifier"），从符号表查找
    3. 递归检查子节点（如二元操作嵌套）
    
    返回：类型字符串 ("int" 或 "char")，无法确定时返回 None
    """
    # 优先级 1: 节点自身有 data_type 字段
    if operand_node.get("data_type"):
        return operand_node["data_type"]
    
    # 优先级 2: 如果操作数是变量引用，从符号表查找
    if operand_node.get("type") == "identifier":
        var_name = operand_node.get("value")
        if var_name in symbol_table.get("variables", {}):
            return symbol_table["variables"][var_name].get("data_type")
    
    # 优先级 3: 递归检查子节点（如嵌套的二元操作）
    children = operand_node.get("children", [])
    if len(children) >= 2:
        return _get_operand_type(children[0], symbol_table)
    
    return None


def _check_type_compatibility(op: str, left_type: str, right_type: str) -> bool:
    """
    检查运算符与操作数类型的兼容性。
    
    规则：
    - 算术运算 (+, -, *, /)：必须都是 int
    - 比较运算 (==, !=, <, >, <=, >=)：必须同类型
    - 逻辑运算 (&&, ||)：必须都是 int（作为布尔值）
    
    返回：True 表示兼容，False 表示不兼容
    """
    ARITHMETIC_OPS = {"+", "-", "*", "/"}
    COMPARISON_OPS = {"==", "!=", "<", ">", "<=", ">="}
    LOGICAL_OPS = {"&&", "||"}
    
    if op in ARITHMETIC_OPS:
        return left_type == "int" and right_type == "int"
    elif op in COMPARISON_OPS:
        return left_type == right_type
    elif op in LOGICAL_OPS:
        return left_type == "int" and right_type == "int"
    return True  # 未知运算符不报错

# === OOP compatibility layer ===
# 不需要 OOP wrapper，这是普通 helper 函数
