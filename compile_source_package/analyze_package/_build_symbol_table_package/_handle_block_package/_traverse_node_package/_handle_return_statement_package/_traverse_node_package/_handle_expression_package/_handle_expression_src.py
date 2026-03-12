# === std / third-party imports ===
from typing import Any, Dict, Set

# === sub function imports ===
# No sub functions needed

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "expression")
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值（运算符）
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
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
def _handle_expression(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 expression 类型节点，进行类型检查。
    输入：表达式 AST 节点和符号表
    处理：验证运算符与操作数类型匹配性
    副作用：可能向 symbol_table["errors"] 追加错误消息
    异常：无
    """
    children = node.get("children", [])
    op = node.get("value", "")
    line = node.get("line")
    column = node.get("column")

    # 获取位置信息
    if line is None or column is None:
        if children:
            line = children[0].get("line", line)
            column = children[0].get("column", column)
        line = line if line is not None else 0
        column = column if column is not None else 0

    # 确保 errors 列表存在
    errors = symbol_table.setdefault("errors", [])

    # 定义运算符分类
    arithmetic_ops: Set[str] = {"+", "-", "*", "/", "%"}
    comparison_ops: Set[str] = {"==", "!=", "<", ">", "<=", ">="}
    logical_ops: Set[str] = {"&&", "||", "!"}

    # 检查操作数数量
    if op in logical_ops and op == "!":
        expected_count = 1
    elif op in logical_ops or op in arithmetic_ops or op in comparison_ops:
        expected_count = 2 if op != "!" else 1
    else:
        expected_count = 2  # 默认二元运算

    if len(children) != expected_count:
        errors.append(
            f"Syntax error at line {line}, column {column}: "
            f"operator '{op}' expects {expected_count} operands, got {len(children)}"
        )
        return

    # 获取操作数类型
    def get_operand_types() -> list:
        return [child.get("data_type", "unknown") for child in children]

    operand_types = get_operand_types()

    # 算术运算检查
    if op in arithmetic_ops:
        for i, child in enumerate(children):
            dtype = child.get("data_type", "unknown")
            if dtype != "int":
                errors.append(
                    f"Type error at line {line}, column {column}: "
                    f"arithmetic operations require int operands, got {dtype}"
                )

    # 关系运算检查
    elif op in comparison_ops:
        if len(children) >= 2:
            left_type = operand_types[0]
            right_type = operand_types[1]
            if left_type != right_type:
                errors.append(
                    f"Type mismatch in expression at line {line}, column {column}: "
                    f"left is {left_type} but right is {right_type}"
                )

    # 逻辑运算检查
    elif op in logical_ops:
        for i, child in enumerate(children):
            dtype = child.get("data_type", "unknown")
            if dtype != "int":
                errors.append(
                    f"Type error at line {line}, column {column}: "
                    f"logical operations require int operands, got {dtype}"
                )

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
