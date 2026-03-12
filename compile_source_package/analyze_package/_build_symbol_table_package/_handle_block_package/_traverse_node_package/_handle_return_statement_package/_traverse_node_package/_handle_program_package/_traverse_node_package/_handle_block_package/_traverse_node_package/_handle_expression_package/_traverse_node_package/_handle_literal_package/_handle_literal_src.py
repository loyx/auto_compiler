# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple handler

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "literal", "identifier", "binary_op" 等)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值 (对于 literal 节点，这是字面量的实际值)
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
#   "errors": list                 # 错误列表 (可选) [{"message": str, "line": int, "column": int}]
# }


# === main function ===
def _handle_literal(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 literal 类型的 AST 节点。
    
    字面量是叶子节点，通常不需要语义检查。本函数执行可选的格式验证和类型一致性检查。
    
    Args:
        node: literal 类型的 AST 节点
        symbol_table: 符号表（如发现错误会追加到 errors 列表）
    """
    # 字面量是叶子节点，通常不需要特殊处理
    # 执行可选的验证检查
    
    value = node.get("value")
    data_type = node.get("data_type")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 验证 data_type 字段是否存在
    if data_type is None:
        _report_error(symbol_table, "Literal node missing data_type", line, column)
        return
    
    # 验证 data_type 是否为合法类型
    if data_type not in ("int", "char"):
        _report_error(symbol_table, f"Invalid data_type '{data_type}' for literal", line, column)
        return
    
    # 验证 value 与 data_type 的一致性
    _validate_literal_value(value, data_type, symbol_table, line, column)


# === helper functions ===
def _validate_literal_value(
    value: Any,
    data_type: str,
    symbol_table: SymbolTable,
    line: int,
    column: int
) -> None:
    """
    验证字面量值与声明的类型是否匹配。
    
    Args:
        value: 字面量的实际值
        data_type: 声明的类型 ("int" 或 "char")
        symbol_table: 符号表（用于记录错误）
        line: 行号
        column: 列号
    """
    if value is None:
        _report_error(symbol_table, "Literal node missing value", line, column)
        return
    
    if data_type == "int":
        if not isinstance(value, int):
            _report_error(symbol_table, f"Expected int value but got {type(value).__name__}", line, column)
    elif data_type == "char":
        if not isinstance(value, str) or len(value) != 1:
            _report_error(symbol_table, f"Expected single char value but got '{value}'", line, column)


def _report_error(
    symbol_table: SymbolTable,
    message: str,
    line: int,
    column: int
) -> None:
    """
    向符号表添加错误信息。
    
    Args:
        symbol_table: 符号表
        message: 错误消息
        line: 行号
        column: 列号
    """
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    symbol_table["errors"].append({
        "message": message,
        "line": line,
        "column": column
    })


# === OOP compatibility layer ===
# Not needed for this internal handler function
