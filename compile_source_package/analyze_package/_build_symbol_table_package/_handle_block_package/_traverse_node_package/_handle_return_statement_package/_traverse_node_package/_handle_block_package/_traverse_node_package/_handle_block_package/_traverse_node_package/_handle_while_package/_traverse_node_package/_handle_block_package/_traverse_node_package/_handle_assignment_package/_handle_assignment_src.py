# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this implementation

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
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理赋值语句节点，验证变量是否已声明及类型匹配。
    
    处理逻辑：
    1. 从 node 中提取被赋值的变量名（children[0].value）
    2. 检查该变量是否在 symbol_table['variables'] 中已声明
    3. 如果未声明，记录"未声明变量"错误
    4. 如果已声明，验证赋值表达式的类型与变量类型是否匹配
    
    副作用：可能向 symbol_table['errors'] 添加错误记录
    """
    # 初始化 errors 列表（如果不存在）
    if 'errors' not in symbol_table:
        symbol_table['errors'] = []
    
    # 提取变量名节点和表达式节点
    if 'children' not in node or len(node['children']) < 2:
        _record_error(symbol_table, node, "赋值语句格式错误：缺少变量名或表达式")
        return
    
    var_name_node = node['children'][0]
    expr_node = node['children'][1]
    
    # 提取变量名
    var_name = var_name_node.get('value')
    if not var_name or not isinstance(var_name, str):
        _record_error(symbol_table, var_name_node, "赋值语句变量名无效")
        return
    
    # 检查变量是否已声明
    variables = symbol_table.get('variables', {})
    if var_name not in variables:
        _record_error(symbol_table, node, f"未声明变量：'{var_name}'")
        return
    
    # 变量已声明，验证类型匹配
    var_info = variables[var_name]
    var_type = var_info.get('data_type')
    expr_type = expr_node.get('data_type')
    
    # 如果两边都有类型信息，进行类型检查
    if var_type and expr_type and var_type != expr_type:
        _record_error(
            symbol_table, 
            node, 
            f"类型不匹配：变量 '{var_name}' 类型为 '{var_type}'，但赋值表达式类型为 '{expr_type}'"
        )

# === helper functions ===
def _record_error(symbol_table: SymbolTable, node: AST, message: str) -> None:
    """
    向符号表记录错误信息。
    
    参数：
    - symbol_table: 符号表，必须包含 'errors' 列表
    - node: 相关 AST 节点，用于提取位置信息
    - message: 错误消息
    """
    error_entry = {
        'message': message,
        'line': node.get('line', -1),
        'column': node.get('column', -1),
        'node_type': node.get('type', 'unknown')
    }
    symbol_table['errors'].append(error_entry)

# === OOP compatibility layer ===
# Not needed for this utility function